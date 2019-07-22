class Tembakau:
    def _init_(self):
        self.__id = ""
        self.__nama = ""
        self.__label = ""
        self.__median = ""
        self.__standartDeviasi = ""
        self.__mean = ""

    def setId(self,id):
        self.__id = id

    def getId(self):
        return self.__id

    def setName(self,nama):
        self.__nama = nama

    def getName(self):
        return self.__nama

    def setLabel(self,label):
        self.label = label

    def getLabel(self):
        return self.label

    def setMean(self,mean):
        self.__mean = mean

    def getMean(self):
        return self.__mean
    
    def setMedian(self,median):
        self.__median = median

    def getMedian(self):
        return self.__median

    def setStDeviasi(self,standarDeviasi):
        self.__standartDeviasi = standartDeviasi

    def getStDeviasi(self):
        return self.__standartDeviasi