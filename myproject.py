
import  sys, os, logging,json
sys.path.insert(0, '/~/myproject/')
from flask import Flask, redirect,render_template, url_for,request,jsonify
from werkzeug.utils import secure_filename
from io import StringIO
import numpy as np
import cv2
from models.Penyakit import Penyakit
from connection.Db import Db
from helper import stat as stat
from helper.kernel import kernel
from helper.crop import crop
#import matplotlib.pyplot as plt


app = Flask(__name__)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/static/images/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
	for ear in early:
		dataX.append(float(ear.getStDeviasi()))
		dataY.append(float(ear.getMean()))
	dataXS = []
	dataYS = []
	for sht in sehat:
		dataXS.append(float(sht.getStDeviasi()))
		dataYS.append(float(sht.getMean()))
	dataXL = []
	dataYL = []
	for lte in late:
		dataXL.append(float(lte.getStDeviasi()))
		dataYL.append(float(lte.getMean()))

	return jsonify(
		sehat_x = dataXS,
		sehat_y = dataYS,
		early_x = dataX,
		early_y = dataY,
		late_x = dataXL,
		late_y = dataYL
    )

	# plt.plot(dataX, dataY, 'ro',dataXS,dataYS,'go',dataXL,dataYL,'bo')
	# plt.savefig("static/"+images_fname)

	# return render_template('graph.html', plot_url=images_fname)

def create_new_folder(local_dir):
	newpath = local_dir
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

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

	location = crop.cropping(saved_path)
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
	os.remove(saved_path+".png")

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

	img = crop.removeBackground(saved_path)
	img = cv2.imread(saved_path,0)
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

	return jsonify(
		saved_path = saved_path,
		mean = mean,
		standart_deviasi = stDev,
		median = median,
		penyakit = hasil,
    )

if __name__ == "__main__":
    app.run(debug=True,host='127.0.0.1',port = 5000)
