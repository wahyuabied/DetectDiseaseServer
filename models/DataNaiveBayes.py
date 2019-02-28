class DataNaiveBayes:

    def __init__(self,st_deviasi,mean,median,status):
        self.__st_deviasi = st_deviasi
        self.__mean = mean
        self.__median = median
        self.__status = status

    # def __init__(self):
    #     self.__st_deviasi = ""
    #     self.__mean = ""
    #     self.__median = ""
    #     self.__status = ""

    def setStDeviasi(self,st_deviasi):
    	self.__st_deviasi = st_deviasi

    def getStDeviasi(self):
    	return self.__st_deviasi

    def setMean(self,mean):
    	self.__mean = mean

    def getMean(self):
    	return self.__mean

    def setMedian(self,median):
        self.__median = median

    def getMedian(self):
        return self.__median

    def setStatus(self,status):
    	self.__status = status

    def getStatus(self):
    	return self.__status