import numpy as np
import cv2
from connection.Db import Db
from helper.kernel import kernel
from helper.crop import crop
import matplotlib.pyplot as plt

# cv2.getGaborKernel(ksize, sigma, theta, lambda, gamma, psi, ktype)
# ksize - size of gabor filter (n, n)
# sigma - standard deviation of the gaussian function(Diameter kernel)
# theta - orientation of the normal to the parallel stripes
# lambda - wavelength of the sunusoidal factor
# gamma - spatial aspect ratio
# psi - phase offset(Keberangkatan gelombang)
# ktype - type and range of values that each pixel in the gabor kernel can hold


if __name__ == '__main__': 
	##getData from DB
	id_kondisi=-1
	path=[]
	# path.append('early/')
	path.append('late/')
	# path.append('sehat/')
	image = cv2.imread('541.jpg',0)
	result = crop.segment(image)
	cv2.imshow('result.jpg', result)


	# mean = np.zeros((len(path),40))
	# median = np.zeros((len(path),40))
	# sDeviation = np.zeros((len(path),40))

	# for y in range(0,len(path)):
	# 	for x in range(0,1):
	# 		img = cv2.imread('('+str(541)+').JPG',0)
	# 		#Cropping
	# 		# location = crop.cropping(path[0],'('+str(x+1)+').JPG')
	# 		# img = cv2.imread(location,0)
	# 		cv2.imshow('imageReal', img)
	# 		filters = kernel.getKernel()
	# 		res1 = kernel.gaborFiltering(img, filters)
	# 		mean[y][x]=kernel.getMean(res1)
	# 		sDeviation[y][x]=kernel.getSDeviate(res1)
	# 		median[y][x]=kernel.getMedian(res1)
			
	# for y in range(0,len(path)):
	# 	for x in range(0,40):
	# 		Db.insert_crop_tomat('cropTomat/'+path[y]+'('+str(x+1)+').jpg',3,1.5,sDeviation[y][x],median[y][x],mean[y][x])
			

<<<<<<< HEAD
	sehat=Db.selectData(5)
	early=Db.selectData(1)
	late=Db.selectData(3)
	outlier=Db.selectData(6)

	data = [early,sehat,late]
	# print(data[0][0].getMedian())
	dataTraining = kernel.naiveBayesData(data)

	for y in range(0,len(path)):
		for x in range (0,46):
			dataTest = []
			dataTest.append(kernel.clasifierMean(mean[y][x]))
			dataTest.append(kernel.clasifierMedian(median[y][x]))
			dataTest.append(kernel.clasifierStDeviasi(sDeviation[y][x]))
			print(str(mean[y][x])+str(median[y][x])+str(sDeviation[y][x]))
			print(kernel.naiveBayes(dataTest,dataTraining))
=======
	# sehat=Db.selectDataTomat(5)
	# early=Db.selectDataTomat(1)
	# late=Db.selectDataTomat(3)
	# outlier=Db.selectData(6)

	# data = [early,sehat,late]
	# # print(data[0][0].getMedian())
	# dataTraining = kernel.naiveBayesData(data)

	# for y in range(0,len(path)):
	# 	for x in range (0,46):
	# 		dataTest = []
	# 		dataTest.append(kernel.clasifierMean(mean[y][x]))
	# 		dataTest.append(kernel.clasifierMedian(median[y][x]))
	# 		dataTest.append(kernel.clasifierStDeviasi(sDeviation[y][x]))
	# 		print(str(mean[y][x])+str(median[y][x])+str(sDeviation[y][x]))
	# 		print(kernel.naiveBayes(dataTest,dataTraining))
>>>>>>> 4c4544ce7133edb6512412b2d2427bba022cb85c
			# print(mean[y][x])
			# print(median[y][x])
			# print(sDeviation[y][x])

	# location = crop.cropping('late/','(26).jpg')
	# # print(location)
	# img = cv2.imread(location,0)
	# cv2.imshow('imageReal', img)
	# filters = kernel.getKernel()
	# res1 = kernel.gaborFiltering(img, filters)
	# mean[0][0]=kernel.getMean(res1)
	# sDeviation[0][0]=kernel.getSDeviate(res1)
	# median[0][0]=kernel.getMedian(res1)

	# print(mean[0][0])
	# print(median[0][0])
	# print(sDeviation[0][0])

	##normalize data to under 1
	# mean = kernel.normalize(mean)
	# sDeviation = kernel.normalize(sDeviation)
	# median = kernel.normalize(median)
	
	##insert database
	# for y in range(0,len(path)):
	# 	id_kondisi=id_kondisi+2
	# 	for x in range(0,40):
	# 		Db.insert_crop_tomat('cropTomat/'+path[y]+'('+str(x+1)+').jpg',id_kondisi,1.5,sDeviation[y][x],median[y][x],mean[y][x])



	##Menentukan outlier
	# outlierEarly = kernel.removeOutlier(early)
	# deleteEarlyId=[]
	# outlierLate = kernel.removeOutlier(late)
	# deleteLateId=[]
	# outlierSehat = kernel.removeOutlier(sehat)
	# deleteSehatId=[]

	# for z in range(0, len(early)):
	# 	if float(early[z].getMedian()) < outlierEarly[0] or float(early[z].getMedian()) > outlierEarly[1]:
	# 		deleteEarlyId.append(early[z].getId())
	# 	if float(late[z].getMedian()) < outlierLate[0] or float(late[z].getMedian()) > outlierLate[1]:
	# 		deleteLateId.append(late[z].getId())
	# 	if float(sehat[z].getMedian()) < outlierSehat[0] or float(sehat[z].getMedian()) > outlierSehat[1]:
	# 		deleteSehatId.append(sehat[z].getId())			

	# for a in range(0, len(deleteEarlyId)):
	# 	Db.editData(deleteEarlyId[a])
	# 	Db.editData(deleteLateId[a])
	# 	Db.editData(deleteSehatId[a])


	# Menampilkan grafik
	# dataX = []
	# dataY = []
	# for ear in early:
	# 	dataX.append(float(ear.getStDeviasi()))
	# 	dataY.append(float(ear.getMedian()))
	# dataXS = []
	# dataYS = []
	# for sht in sehat:
	# 	dataXS.append(float(sht.getStDeviasi()))
	# 	dataYS.append(float(sht.getMedian()))
	# dataXL = []
	# dataYL = []
	# for lte in late:
	# 	dataXL.append(float(lte.getStDeviasi()))
	# 	dataYL.append(float(lte.getMedian()))
	# # dataOX = []
	# # dataOY = []
	# # for out in outlier:
	# # 	dataOX.append(float(out.getStDeviasi()))
	# # 	dataOY.append(float(out.getMean()))
	
	# plt.plot(dataX, dataY, 'ro',dataXS,dataYS,'go',dataXL,dataYL,'bo')
	# plt.plot(dataX, dataY, 'ro',dataXS,dataYS,'go',dataXL,dataYL,'bo',dataOX,dataOY,'ko')
	plt.show()

	

	cv2.waitKey(0)
	cv2.destroyAllWindows()