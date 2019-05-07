import numpy as np
import cv2
import matplotlib.pyplot as plt
import operator
import os
from connection.Db import Db
from helper.kernel import kernel
from helper.crop import crop
from skimage.filters.rank import autolevel
from mpl_toolkits import mplot3d
from skimage.morphology import disk


# cv2.getGaborKernel(ksize, sigma, theta, lambda, gamma, psi, ktype)
# ksize - size of gabor filter (n, n)
# sigma - standard deviation of the gaussian function(Diameter kernel)
# theta - orientation of the normal to the parallel stripes
# lambda - wavelength of the sunusoidal factor
# gamma - spatial aspect ratio
# psi - phase offset(Keberangkatan gelombang)
# ktype - type and range of values that each pixel in the gabor kernel can hold


if __name__ == '__main__': 

	# im = cv2.imread("1.jpg",0)
	# cv2.imshow("before",im)
	# im2 = kernel.autoLevel(im)
	# cv2.imshow("after",im2)
	# print(len(im))
	# h = im.convert("L").histogram()
	# lut = []
	# for b in range(0, len(h), 256):        
	# 	step = reduce(operator.add, h[b:b+256]) / 255
	# 	n = 0
	# 	for i in range(256):
	# 		lut.append(n / step)
	# 		n = n + h[i+b]
	# print(im.point(lut*im.layers))
	# #getData from DB
	# id_kondisi=-1
	# path=[]
	# path.append('tomat/early/')
	# path.append('tomat/late/')
	# # path.append('tomat/sehat/')
	# # for y in range(0,8):
	# # 	image = kernel.faseKentang('('+str(y+1)+').jpg')

	# ##for getting data training
	# mean = np.zeros((len(path),len(os.listdir(path[1]))))
	# median = np.zeros((len(path),len(os.listdir(path[1]))))
	# sDeviation = np.zeros((len(path),len(os.listdir(path[1]))))

	# for y in range(0,len(path)):
	# 	for x in range(0,len(os.listdir(path[y]))):
	# 		imgs = cv2.imread(path[y]+'('+str(x+1)+').jpg')
	# 		img = crop.removeBackgroundTraining(path[y],'('+str(x+1)+')',imgs)
	# 		readyImages = cv2.imread('noBackground/'+path[y]+'('+str(x+1)+').PNG',0)
	# 		#Cropping
	# 		# location = crop.cropping(path[y],'('+str(x+1)+').jpg')
	# 		# img = cv2.imread(location,0)
	# 		# cv2.imshow('imageReal', img)
	# 		filters = kernel.getKernelTomat()
	# 		res1 = kernel.gaborFiltering(readyImages, filters)
	# 		mean[y][x]=kernel.getMean(res1)
	# 		sDeviation[y][x]=kernel.getSDeviate(res1)
	# 		median[y][x]=kernel.getMedian(res1)
			
	# for y in range(0,len(path)):
	# 	id_kondisi=id_kondisi+2
	# 	for x in range(0,len(os.listdir(path[y]))):
	# 		Db.insert_crop_tomat(path[y]+'('+str(x+1)+').jpg',id_kondisi,1.5,sDeviation[y][x],median[y][x],mean[y][x])
			

	sehat=Db.selectData(5)
	early=Db.selectData(1)
	late=Db.selectData(3)
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


#	Menampilkan grafik
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
	# dataOX = []
	# dataOY = []
	# for out in outlier:
	# 	dataOX.append(float(out.getStDeviasi()))
	# 	dataOY.append(float(out.getMean()))
	
	# plt.plot(dataX, dataY, 'ro',dataXS,dataYS,'go',dataXL,dataYL,'bo')
	ax = plt.axes(projection='3d')
	ax.scatter3D(dataX, dataY, dataZ, c=dataZ, cmap='Reds');
	ax.scatter3D(dataXS, dataYS, dataZS, c=dataZS, cmap='Greens');
	ax.scatter3D(dataXL, dataYL, dataZL, c=dataZL, cmap='Blues');
	# plt.plot(dataX, dataY, 'ro',dataXS,dataYS,'go',dataXL,dataYL,'bo',dataOX,dataOY,'ko')
	plt.show()

	

	cv2.waitKey(0)
	cv2.destroyAllWindows()