class Data:
    def __init__(self):
        self.__id = ""
        self.__name = ""
        self.__st_deviasi = ""
        self.__mean = ""
        self.__id_kondisi = ""
        self.__r = ""

    def setId(self,id):
        self.__id = id

    def getId(self):
        return self.__id

    def setName(self,name):
    	self.__name = name

    def getName(self):
    	return self.__name

    def setStDeviasi(self,st_deviasi):
    	self.__st_deviasi = st_deviasi

    def getStDeviasi(self):
    	return self.__st_deviasi

    def setMean(self,mean):
    	self.__mean = mean

    def getMean(self):
    	return self.__mean

    def setIdKondisi(self,id_kondisi):
    	self.__id_kondisi = id_kondisi

    def getIdKondisi(self):
    	return self.__id_kondisi

    def setR(self,r):
    	self.__r = r

    def getR(self):
    	return self.__r