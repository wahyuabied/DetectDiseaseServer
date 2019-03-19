class Penyakit():
    def __init__(self):
        self.__id = ""
        self.__name = ""
        self.__deskripsi = ""
        self.__gejala = ""
        self.__solusi = ""
        self.__gambar = ""

    def setId(self,id):
        self.__id = id

    def getId(self):
        return self.__id

    def setName(self,name):
    	self.__name = name

    def getName(self):
        return self.__name

    def setDeskripsi(self,deskripsi):
        self.__deskripsi = deskripsi

    def getDeskripsi(self):
    	return self.__deskripsi

    def setGejala(self,gejala):
        self.__gejala = gejala

    def getGejala(self):
        return self.__gejala

    def setSolusi(self,solusi):
        self.__solusi = solusi

    def getSolusi(self):
        return self.__solusi

    def setGambar(self,gambar):
        self.__gambar = gambar

    def getGambar(self):
        return self.__gambar


