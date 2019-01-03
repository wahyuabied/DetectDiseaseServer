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
	# sehat=Db.selectData(5)
	# early=Db.selectData(1)
	# late=Db.selectData(3)
	id_kondisi=-1
	path=[]
	path.append('early/')
	path.append('late/')
	path.append('sehat/')

	mean = np.zeros((len(path),40))
	median = np.zeros((len(path),40))
	sDeviation = np.zeros((len(path),40))

	# location = crop.cropping(path[0],'('+str(0+1)+').jpg')
	# print(location)
	# img = cv2.imread(location,0)
	# print(type(img))

	for y in range(0,len(path)):
		for x in range(0,40):
			# img = cv2.imread(path[y]+'('+str(x)+').jpg',0)
			#Cropping
			location = crop.cropping(path[y],'('+str(x+1)+').jpg')
			print(location)
			img = cv2.imread(location,0)
			cv2.imshow('imageReal', img)
			filters = kernel.getKernel()
			res1 = kernel.gaborFiltering(img, filters)
			mean[y][x]=kernel.getMean(res1)
			sDeviation[y][x]=kernel.getSDeviate(res1)
			median[y][x]=kernel.getMedian(res1)

	maxMean = kernel.getMaximum(mean)
	maxsDeviation = kernel.getMaximum(sDeviation)
	maxMedian = kernel.getMaximum(median)

	Db.insert_max_value(maxMean,maxMedian,maxsDeviation)

	mean = kernel.normalize(mean)
	sDeviation = kernel.normalize(sDeviation)
	median = kernel.normalize(median)
	
	for y in range(0,len(path)):
		id_kondisi=id_kondisi+2
		for x in range(0,40):
			Db.insert_crop('crop/'+path[y]+'('+str(x+1)+').jpg',id_kondisi,1.5,sDeviation[y][x],median[y][x],mean[y][x])



	#Get Graph
	# dataX = []
	# dataY = []
	# for ear in early:
	# 	dataX.append(float(ear.getStDeviasi()))
	# 	dataY.append(float(ear.getMean()))
	# dataXS = []
	# dataYS = []
	# for sht in sehat:
	# 	dataXS.append(float(sht.getStDeviasi()))
	# 	dataYS.append(float(sht.getMean()))
	# dataXL = []
	# dataYL = []
	# for lte in late:
	# 	dataXL.append(float(lte.getStDeviasi()))
	# 	dataYL.append(float(lte.getMean()))
	
	# plt.plot(dataX, dataY, 'ro',dataXS,dataYS,'go',dataXL,dataYL,'bo')
	# plt.show()

	#Interseksi
	#Histogram proyeksi
	#Region of interest(ROI)

	cv2.waitKey(0)
	cv2.destroyAllWindows()

