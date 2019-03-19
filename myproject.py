
import  sys, os, logging
sys.path.insert(0, '/~/myproject/')
from flask import Flask, redirect,render_template, url_for,request,jsonify
from werkzeug.utils import secure_filename
from io import StringIO
import numpy as np
import cv2
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
    return "Hello, World!"

@app.route("/api/Graph-Disease",methods=['GET'])
def graph():

	sehat=Db.selectData(5)
	early=Db.selectData(1)
	late=Db.selectData(3)
	dataX = []
	dataY = []
	img = StringIO()
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
	regularPath = 'static/images/'
	app.logger.info(app.config['UPLOAD_FOLDER'])
	img = request.files['image']
	img_name = secure_filename(img.filename)
	create_new_folder(app.config['UPLOAD_FOLDER'])
	saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
	app.logger.info("saving {}".format(saved_path))
	img.save(saved_path)
	os.chmod(saved_path, 0o755)

	img = cv2.imread(saved_path,0)
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

	# maximum = Db.selectMaxValue()

	# maxMean = []
	# maxMedian = []
	# maxsDeviasi = []
	
	# for maximum in maxs:
	# 	maxs = FeatureExtraction() 
	# 	maxsDeviasi.append(float(maxs.getStDeviasi()))
	# 	maxMedian.append(float(maxs.getMedian()))
	# 	maxMean.append(float(maxs.getMean()))

	return jsonify(
		saved_path = saved_path,
		mean = mean,
		standart_deviasi = stDev,
		median = median,
		penyakit = hasil,
		# maxsDeviasi = maximum[0].getStDeviasi(),
		# maxMedian = maximum[0].getMedian(),
		# maxMean = maximum[0].getMean(),
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
	dataTraining = kernel.naiveBayesData(data)
	dataTest = []
	dataTest.append(kernel.clasifierMean(mean))
	dataTest.append(kernel.clasifierMedian(median))
	dataTest.append(kernel.clasifierStDeviasi(stDev))
	hasil = kernel.naiveBayes(dataTest,dataTraining)

	# maximum = Db.selectMaxValue()

	# maxMean = []
	# maxMedian = []
	# maxsDeviasi = []
	
	# for maximum in maxs:
	# 	maxs = FeatureExtraction() 
	# 	maxsDeviasi.append(float(maxs.getStDeviasi()))
	# 	maxMedian.append(float(maxs.getMedian()))
	# 	maxMean.append(float(maxs.getMean()))

	return jsonify(
		saved_path = saved_path,
		mean = mean,
		standart_deviasi = stDev,
		median = median,
		penyakit = hasil,
		# maxsDeviasi = maximum[0].getStDeviasi(),
		# maxMedian = maximum[0].getMedian(),
		# maxMean = maximum[0].getMean(),
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
