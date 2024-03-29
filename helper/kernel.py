import numpy as np
import cv2
from helper.crop import crop
import matplotlib.pyplot as plt
from models.DataNaiveBayes import DataNaiveBayes

class kernel:

	def degree(x):
		return (x*(np.pi/180))

	def frequency_to_lamda(x):
		return (1/x)

	def getKernel():
		filters = []
		ksize = 49
		scale  = [kernel.frequency_to_lamda(0.06),kernel.frequency_to_lamda(0.09),kernel.frequency_to_lamda(0.13),kernel.frequency_to_lamda(0.18),kernel.frequency_to_lamda(0.25)] #skalanya ditambah lagi
		theta = [kernel.degree(0),kernel.degree(30),kernel.degree(45),kernel.degree(60),kernel.degree(90),kernel.degree(120),kernel.degree(135),kernel.degree(150)]
		for i in np.arange(0, len(theta),1):
			for j in np.arange(0,len(scale),1):
			 	kern = cv2.getGaborKernel((ksize, ksize), 3.0,theta[i], scale[j], 0.5, 0, ktype=cv2.CV_32F)
		 		kern /= 1.5*kern.sum()
		 		filters.append(kern)
		return filters

	def getKernelTembakau():
		filters = []
		ksize = 31
		scale  = [kernel.frequency_to_lamda(10),kernel.frequency_to_lamda(13),kernel.frequency_to_lamda(15),kernel.frequency_to_lamda(18),kernel.frequency_to_lamda(20),kernel.frequency_to_lamda(21),kernel.frequency_to_lamda(23),kernel.frequency_to_lamda(24)] #skalanya ditambah lagi
		theta = [kernel.degree(0),kernel.degree(30),kernel.degree(45),kernel.degree(57),kernel.degree(60),kernel.degree(90),kernel.degree(115),kernel.degree(120),kernel.degree(135),kernel.degree(150),kernel.degree(160),kernel.degree(175)]
		for i in np.arange(0, len(theta),1):
			for j in np.arange(0,len(scale),1):
			 	kern = cv2.getGaborKernel((ksize, ksize), 3.0,theta[i], scale[j], 0.5, 0, ktype=cv2.CV_32F)
		 		kern /= 1.5*kern.sum()
		 		filters.append(kern)
		return filters		


#dokumentasi
#jika jarak scale diperkecil maka gambar semakin geser kekiri dan jarak biru semakin menadekat ke hjau
	def getKernelTomat():
		filters = []
		ksize = 49  #31 == dicoba ke 49(ukuran yang palingn banyak dipakai) => semakin besar size 
		scale  = [kernel.frequency_to_lamda(0.06),kernel.frequency_to_lamda(0.09),kernel.frequency_to_lamda(0.13),kernel.frequency_to_lamda(0.18),kernel.frequency_to_lamda(0.21),kernel.frequency_to_lamda(0.25)]
		#ini 0.06 nya ini adalah 6/100 nya
		# theta = [kernel.degree(0),kernel.degree(10),kernel.degree(20),kernel.degree(30),kernel.degree(40),kernel.degree(50),kernel.degree(60),kernel.degree(70)
		# ,kernel.degree(80),kernel.degree(90),kernel.degree(100),kernel.degree(110),kernel.degree(120),kernel.degree(130),kernel.degree(140),kernel.degree(150)
		# ,kernel.degree(160),kernel.degree(170)]
		theta = [kernel.degree(0),kernel.degree(30),kernel.degree(45),kernel.degree(57),kernel.degree(60),kernel.degree(90),kernel.degree(114),kernel.degree(120),kernel.degree(135),kernel.degree(150)]
		# theta = [kernel.degree(0),kernel.degree(23),kernel.degree(45),kernel.degree(68),kernel.degree(90),kernel.degree(113),kernel.degree(135),kernel.degree(158)]
		# orientasi dimainnkan untuk memperbaiki nilainya(paling baik 1 radint (57 derajat) atau 1/3 radiant atau phi radiant)
		# untuk tomat memakai 7 scala dan 15 orientasi atau menggunakan kelipatan 10 untuk thetanya
		for i in np.arange(0, len(theta),1):
			for j in np.arange(0,len(scale),1):
			 	kern = cv2.getGaborKernel((ksize, ksize), 3.0,theta[i], scale[j], 0.5, 0, ktype=cv2.CV_32F)
			 	#untuk menentukan angka tinggi sedang dan rendah nya kita pakai kuartil atau fuzzy
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
		medianEarly = len(earlyData[1])/len(kelasEarly)#masalah terkadang 0
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

		return (str(sehat) +" "+str(early)+" "+str(late))

	def faseKentang(penyakit,data):
		path = cv2.imread(data,1)
		rgb = np.average(path,axis=0)
		rgb = np.average(rgb,axis=0)
		if penyakit=="early":
			if rgb[1]-rgb[0]>28:
				if rgb[2]>rgb[1]:
					fase = "Parah"
				else:
					fase = "Awal Penyakit"
			else:
				fase = "Awal Penyakit"
		elif penyakit == "late":
			if rgb[1]-rgb[2]<5 or rgb[1]<173:
				fase = "Parah"
			else:
				fase = "Awal Penyakit"
		else :
			fase = "-"

		return fase

	def faseTomat(penyakit,data):
		path = cv2.imread(data,1)
		rgb = np.average(path,axis=0)
		rgb = np.average(rgb,axis=0)
		if penyakit=="early":
			if rgb[1]-rgb[0]>8:
				if rgb[1]-rgb[2]>5:
					fase = "Parah"
				else:
					fase = "Awal Penyakit"
			else:
				fase = "Awal Penyakit"
		elif penyakit == "late":
			if rgb[1]-rgb[2]>10:
				fase = "Awal  Penyakit"
			else:
				fase = "Parah"
		else :
			fase = "-"

		return fase

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

	def autoLevel(data):
		equ = cv2.equalizeHist(data)
		res = np.hstack((data,equ))
		return res
