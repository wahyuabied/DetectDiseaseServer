import numpy as np
import cv2

class kernel:

	def degree(x):
		return (x*(np.pi/180))

	def frequency_to_lamda(x):
		return (1/x)

	# def get_gabor_kernel(kernel_size_x, kernel_size_y,sigma_x, sigma_y, theta, frequency, psi):
	# 	sigma_x = sigma_x
	# 	sigma_y = float(sigma_x) / sigma_y
	# 	nstds = 3 # Number of standard deviation sigma
	# 	xmax = max(abs(nstds * sigma_x * np.cos(theta)), abs(nstds * sigma_y * np.sin(theta)))
	# 	xmax = np.ceil(max(1, xmax))
	# 	ymax = max(abs(nstds * sigma_x * np.sin(theta)), abs(nstds * sigma_y * np.cos(theta)))
	# 	ymax = np.ceil(max(1, ymax))
	# 	xmin = -xmax
	# 	ymin = -ymax
	# 	(y, x) = np.meshgrid(np.arange(ymin, ymax + 1), np.arange(xmin, xmax + 1))
	#     #Rotasi
	# 	x_theta = x * np.cos(theta) + y * np.sin(theta)
	# 	y_theta = -x * np.sin(theta) + y * np.cos(theta)
	#     #Calculate the gabor kernel according the formula
	# 	gb = np.exp(-.5*(x_theta ** 2.0 / sigma_x ** 2.0 + y_theta ** 2.0 / sigma_y ** 2.0)) * np.cos(2 * np.pi * frequency * x_theta + psi)
	# 	return gb

	def getKernel():
		filters = []
		ksize = 31  #31
		scale  = [kernel.frequency_to_lamda(0.06),kernel.frequency_to_lamda(0.09),kernel.frequency_to_lamda(0.13),kernel.frequency_to_lamda(0.18),kernel.frequency_to_lamda(0.25)]#frequency
		theta = [kernel.degree(0),kernel.degree(30),kernel.degree(45),kernel.degree(60),kernel.degree(90),kernel.degree(120),kernel.degree(135),kernel.degree(150)]
		for i in np.arange(0, len(theta),1):
			for j in np.arange(0,len(scale),1):
			 	kern = cv2.getGaborKernel((ksize, ksize), 3.0,theta[i], scale[j], 0.5, 0, ktype=cv2.CV_32F)
			 	# resized_image = cv2.resize(kern, (200, 200))
			 	# cv2.imshow('kernel'+str(i)+str(j), resized_image)
			 	# cv2.imshow('kernel'+str(i), kern)
		 		kern /= 1.5*kern.sum()
		 		filters.append(kern)
		return filters
	 
	def gaborFiltering(img, filters):
		all_accum=[]
		for i,kern in enumerate(filters):
			accum = np.zeros_like(img)
			fimg = cv2.filter2D(img, cv2.CV_16UC3, kern)
			np.maximum(accum, fimg, accum)
			# cv2.imshow('filter'+str(i), accum)
			all_accum.append(accum)		
		return all_accum

	def getMean(var):
		jumlah = np.mean(var)
		# print(jumlah)
		return jumlah	

	def getSDeviate(var):
		hasil = np.std(var)
		# print(hasil)
		return hasil

	def getMedian(var):
		hasil = np.median(var)
		# print(hasil)
		return hasil

	def normalize(data):
		temp = data[0][0]
		value = np.zeros((len(data),len(data[0])))
		for j in range(0,len(data)):
			for i in range(0, len(data[0])):
				if temp>data[j][i]:
					temp = temp
				else:
					temp = data[j][i]
		
		for j in range(0,len(data)):
			for i in range(0, len(data[0])):
				value[j][i] = data[j][i]/temp

		return value

	def getMaximum(data):
		temp = data[0][0]
		value = np.zeros((len(data),len(data[0])))
		for j in range(0,len(data)):
			for i in range(0, len(data[0])):
				if temp>data[j][i]:
					temp = temp
				else:
					temp = data[j][i]
		return temp