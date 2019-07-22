import  sys, os, logging,json
sys.path.insert(0, '/~/myproject/')
from flask import Flask, redirect,render_template, url_for,request,jsonify
from werkzeug.utils import secure_filename
from io import StringIO
import numpy as np
import cv2
from models.Penyakit import Penyakit
from connection.Db import Db
from helper.kernel import kernel
from helper.crop import crop
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

#import matplotlib.pyplot as plt


app = Flask(__name__)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/static/images/'.format(PROJECT_HOME)
UPLOAD_GRAPH = '{}/static/graph/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_GRAPH'] = UPLOAD_GRAPH

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api/get-penyakit")
def penyakit():
	penyakit = Db.getPenyakit()
	return jsonify(penyakit)

@app.route("/api/get-pestisida")
def pestisida():
	pestisida = Db.getPestisida()
	return jsonify(pestisida)

@app.route("/api/Graph-Disease",methods=['GET'])
def graph():

	sehat=Db.selectData(5)
	early=Db.selectData(1)
	late=Db.selectData(3)
	dataX = []
	dataY = []
	dataZ = []
	for ear in early:
		dataX.append(float(ear.getStDeviasi()))
		dataY.append(float(ear.getMean()))
		dataZ.append(float(ear.getMedian()))
	dataXS = []
	dataYS = []
	dataZS = []
	for sht in sehat:
		dataXS.append(float(sht.getStDeviasi()))
		dataYS.append(float(sht.getMean()))
		dataZS.append(float(sht.getMedian()))
	dataXL = []
	dataYL = []
	dataZL = []
	for lte in late:
		dataXL.append(float(lte.getStDeviasi()))
		dataYL.append(float(lte.getMean()))
		dataZL.append(float(lte.getMedian()))


	return jsonify(
		sehat_x = dataXS,
		sehat_y = dataYS,
		early_x = dataX,
		early_y = dataY,
		late_x = dataXL,
		late_y = dataYL
    )


def create_new_folder(local_dir):
	newpath = local_dir
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

@app.route("/api/feature-extraction-tembakau",methods=['POST'])
def featureDetectionTembakau():
	app.logger.info(app.config['UPLOAD_FOLDER'])
	img = request.files['image']
	img_name = secure_filename(img.filename)
	create_new_folder(app.config['UPLOAD_FOLDER'])
	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
	app.logger.info("saving {}".format(saved_path))
	img.save(saved_path)
	os.chmod(saved_path, 0o755)
	resize = cv2.resize(cv2.imread(saved_path),(512,512))
	cv2.imwrite(saved_path,resize)

	img = cv2.imread(saved_path)
	filters = kernel.getKernelTembakau()#119
	res1 = kernel.gaborFiltering(img, filters)
	mean = kernel.getMean(res1)/112.05
	stDev = kernel.getSDeviate(res1)/112.81
	median = kernel.getMedian(res1)/94

	#data training
	training=Db.selectDataTembakau()
	dataTrain = []
	for datum in training:    
	    dataTrain.append([datum.getStDeviasi(),datum.getMean(),datum.getMedian(),datum.getLabel()])
	dataTrain_df = pd.DataFrame(dataTrain,columns=["st_dev", "r", "median","label"]) 
	trainX = dataTrain_df[["st_dev","r","median"]]
	trainY = dataTrain_df["label"]
	#data testing
	dataTest = []
	dataTest.append([stDev,mean,median,-1])

	dataTest_df = pd.DataFrame(dataTest,columns=["st_dev", "r", "median","label"]) 
	testX = dataTest_df[["st_dev","r","median"]]
	testY = dataTest_df["label"]


	knn3 = KNeighborsClassifier(n_neighbors = 5)

	knn3.fit(trainX,trainY)
	list_pickle_path = 'tembakau_data.pkl'
	list_pickle = open(list_pickle_path, 'wb')
	pickle.dump(knn3, list_pickle)
	list_pickle.close()
	list_unpickle = open(list_pickle_path, 'rb')
	knn3 = pickle.load(list_unpickle)
	predicting = knn3.predict(testX)

	return jsonify(
		hasil_prediksi = predicting[0]
    )


@app.route("/api/feature-extraction-kentang",methods=['POST'])
def featureDetection():
	# regularPath = 'static/images/'
	app.logger.info(app.config['UPLOAD_FOLDER'])
	img = request.files['image']
	img_name = secure_filename(img.filename)
	create_new_folder(app.config['UPLOAD_FOLDER'])
	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
	app.logger.info("saving {}".format(saved_path))
	img.save(saved_path)
	os.chmod(saved_path, 0o755)
	resize = cv2.resize(cv2.imread(saved_path),(256,256))
	cv2.imwrite(saved_path,resize)

	if request.form['autoLevel']=="yes":
		location = crop.removeBackground(saved_path)
		img = kernel.autoLevel(cv2.imread(saved_path,0))
	else:
		location = crop.crop(saved_path)
		img = cv2.imread(location,0)

	filters = kernel.getKernel()
	res1 = kernel.gaborFiltering(img, filters)
	mean = kernel.getMean(res1)
	stDev = kernel.getSDeviate(res1)
	median = kernel.getMedian(res1)

	sehat=Db.selectData(5)
	early=Db.selectData(1)
	late=Db.selectData(3)

	data = [early,sehat,late]
	dataTraining = kernel.naiveBayesData(data)

	dataTest = []
	dataTest.append(kernel.clasifierMean(mean))
	dataTest.append(kernel.clasifierMedian(median))
	dataTest.append(kernel.clasifierStDeviasi(stDev))
	hasil = kernel.naiveBayes(dataTest,dataTraining)

	fase = kernel.faseKentang(hasil,saved_path)
	# os.remove(saved_path+".png")

	return jsonify(
		saved_path = saved_path,
		mean = mean,
		standart_deviasi = stDev,
		median = median,
		penyakit = hasil,
		fase = fase,
    )

@app.route("/api/feature-extraction-tomat",methods=['POST'])
def featureDetectionTomat():
	regularPath = 'static/images/'
	app.logger.info(app.config['UPLOAD_FOLDER'])
	img = request.files['image']
	img_name = secure_filename(img.filename)
	create_new_folder(app.config['UPLOAD_FOLDER'])
	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
	app.logger.info("saving {}".format(saved_path))
	img.save(saved_path)
	os.chmod(saved_path, 0o755)
	resize = cv2.resize(cv2.imread(saved_path),(256,256))
	cv2.imwrite(saved_path,resize)

	if request.form['autoLevel']=="yes":
		location = crop.removeBackground(saved_path)
		img = kernel.autoLevel(cv2.imread(location,0))
	else:
		location = crop.removeBackground(saved_path)
		img = cv2.imread(location,0)
		
	filters = kernel.getKernel()
	res1 = kernel.gaborFiltering(img, filters)
	mean = kernel.getMean(res1)
	stDev = kernel.getSDeviate(res1)
	median = kernel.getMedian(res1)

	sehat=Db.selectDataTomat(5)
	early=Db.selectDataTomat(1)
	late=Db.selectDataTomat(3)

	data = [early,sehat,late]
	dataTraining = kernel.naiveBayesDataTomat(data)
	dataTest = []
	dataTest.append(kernel.clasifierMeanTomat(mean))
	dataTest.append(kernel.clasifierMedianTomat(median))
	dataTest.append(kernel.clasifierStDeviasiTomat(stDev))
	hasil = kernel.naiveBayes(dataTest,dataTraining)

	fase = kernel.faseTomat(hasil,saved_path)

	return jsonify(
		saved_path = saved_path,
		mean = mean,
		standart_deviasi = stDev,
		median = median,
		penyakit = hasil,
		fase = fase,
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
