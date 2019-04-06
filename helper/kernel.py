import numpy as np
import cv2
from models.DataNaiveBayes import DataNaiveBayes

class kernel:

	def degree(x):
		return (x*(np.pi/180))

	def frequency_to_lamda(x):
		return (1/x)

	def getKernel():
		filters = []
		ksize = 31  #31
		scale  = [kernel.frequency_to_lamda(0.06),kernel.frequency_to_lamda(0.09),kernel.frequency_to_lamda(0.13),kernel.frequency_to_lamda(0.18),kernel.frequency_to_lamda(0.25)]#frequency
		theta = [kernel.degree(0),kernel.degree(30),kernel.degree(45),kernel.degree(60),kernel.degree(90),kernel.degree(120),kernel.degree(135),kernel.degree(150)]
		for i in np.arange(0, len(theta),1):
			for j in np.arange(0,len(scale),1):
			 	kern = cv2.getGaborKernel((ksize, ksize), 3.0,theta[i], scale[j], 0.5, 0, ktype=cv2.CV_32F)
			 	# resized_image = cv2.resize(kern, (200, 200))
			 	# cv2.imshow('kernel'+str(i)+str(j), kern)
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
		print(jumlah)
		return jumlah	

	def getSDeviate(var):
		hasil = np.std(var)
		print(hasil)
		return hasil

	def getMedian(var):
		hasil = np.median(var)
		print(hasil)
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

	def removeOutlier(data):
		datas = []
		for values in data:
			datas.append(float(values.getMedian()))
		datas = np.sort(datas,axis=0)
		n_quartil_bawah = 1/4*len(datas)
		n_quartil_atas = 3/4*len(datas)
		minor_outlier = []

		pagar_bawah_inter_kuartil = 1.5*(datas[int(n_quartil_atas-1)] - datas[int(n_quartil_bawah-1)])
		minor_outlier.append(datas[int(n_quartil_bawah-1)] - pagar_bawah_inter_kuartil)
		minor_outlier.append(datas[int(n_quartil_atas-1)] + pagar_bawah_inter_kuartil)

		return minor_outlier

	def naiveBayesData(data):
		status = ["early","sehat","late"]
		dataNaiveBayes = []
		
		for i in range(0,len(status)):
			for j in range (0,len(data[i])):
				dataNaiveBayes.append(DataNaiveBayes(kernel.clasifierStDeviasi(data[i][j].getStDeviasi()),kernel.clasifierMean(data[i][j].getMean()),kernel.clasifierMedian(data[i][j].getMedian()),data[i][j].getIdKondisi()))

		return dataNaiveBayes

	def naiveBayesDataTomat(data):
		status = ["early","sehat","late"]
		dataNaiveBayes = []
		
		for i in range(0,len(status)):
			for j in range (0,len(data[i])):
				dataNaiveBayes.append(DataNaiveBayes(kernel.clasifierStDeviasiTomat(data[i][j].getStDeviasi()),kernel.clasifierMeanTomat(data[i][j].getMean()),kernel.clasifierMedianTomat(data[i][j].getMedian()),data[i][j].getIdKondisi()))

		return dataNaiveBayes


	def naiveBayes(dataTest, dataTraining):	

		kelasSehat = [] #kelasEarly[0].getMean()
		kelasEarly = []
		kelasLate = []

		sehatData = [] #print(len(kelasEarly[0]) -> kelasEarly[0].getStDeviasi()
		earlyData = []
		lateData = []

		for i in range(3):
			sehatData.append([])
			lateData.append([])
			earlyData.append([])

		for obj in dataTraining:
			if obj.getStatus()==5:
				kelasSehat.append(obj)
			elif obj.getStatus()==3:
				kelasLate.append(obj)
			elif obj.getStatus()==1:
				kelasEarly.append(obj)

		# print(kelasEarly[0].getMean())
			
		for sehat in kelasSehat:
			if dataTest[0]==sehat.getMean():
				sehatData[0].append(sehat)
			if dataTest[1]==sehat.getMedian():
				sehatData[1].append(sehat)
			if dataTest[2]==sehat.getStDeviasi():
				sehatData[2].append(sehat)

		for early in kelasEarly:
			if dataTest[0]==early.getMean():
				earlyData[0].append(early)
			if dataTest[1]==early.getMedian():
				earlyData[1].append(early)
			if dataTest[2]==early.getStDeviasi():
				earlyData[2].append(early)

		for late in kelasLate:
			if dataTest[0]==late.getMean() :
				lateData[0].append(late)
			if dataTest[1]==late.getMedian():
				lateData[1].append(late)
			if dataTest[2]==late.getStDeviasi():
				lateData[2].append(late)
		
		# [0] mean. [1] median. [2]stDeviasi
		meanSehat = len(sehatData[0])/len(kelasSehat)
		medianSehat = len(sehatData[1])/len(kelasSehat)
		stdSehat = len(sehatData[2])/len(kelasSehat)

		meanEarly = len(earlyData[0])/len(kelasEarly)
		medianEarly = len(earlyData[1])/len(kelasEarly)
		stdEarly = len(earlyData[2])/len(kelasEarly)


		meanLate = len(lateData[0])/len(kelasLate)
		medianLate = len(lateData[1])/len(kelasLate)
		stdLate = len(lateData[2])/len(kelasLate)

		sehat = meanSehat * medianSehat * stdSehat * (len(kelasSehat)/len(dataTraining))
		early = meanEarly * medianEarly * stdEarly * (len(kelasEarly)/len(dataTraining))
		late = meanLate * medianLate * stdLate * (len(kelasLate)/len(dataTraining))


		if(sehat > early and sehat >late):
			return "sehat"
		elif (early > late and early >sehat):
			return "early"
		elif (late > early and late >sehat):
			return "late"
		else:
			return(str(sehat) +" "+str(early)+" "+str(late))

		return (str(sehat) +" "+str(early)+" "+str(late))

	def clasifierStDeviasi(nilai):
		nilai = float (nilai)
		if nilai<56:
			stDeviasi = "rendah"
		elif nilai>60:
			stDeviasi = "tinggi"
		else:
			stDeviasi = "sedang"

		return stDeviasi

	def clasifierMean(nilai):
		nilai = float (nilai)
		if nilai < 74:
			stDeviasi = "rendah"
		elif nilai>81:
			stDeviasi = "tinggi"
		else:
			stDeviasi = "sedang"

		return stDeviasi

	def clasifierMedian(nilai):
		nilai = float (nilai)
		if nilai<73:
			stDeviasi = "rendah"
		elif nilai>82:
			stDeviasi = "tinggi"
		else:
			stDeviasi = "sedang"

		return stDeviasi

	def clasifierStDeviasiTomat(nilai):
		nilai = float (nilai)
		if nilai<64:
			stDeviasi = "rendah"
		elif nilai>70:
			stDeviasi = "tinggi"
		else:
			stDeviasi = "sedang"

		return stDeviasi


	def clasifierMeanTomat(nilai):
		nilai = float (nilai)
		if nilai < 108:
			stDeviasi = "rendah"
		elif nilai>119:
			stDeviasi = "tinggi"
		else:
			stDeviasi = "sedang"

		return stDeviasi

	def clasifierMedianTomat(nilai):
		nilai = float (nilai)
		if nilai < 133:
			stDeviasi = "rendah"
		elif nilai>154:
			stDeviasi = "tinggi"
		else:
			stDeviasi = "sedang"

		return stDeviasi