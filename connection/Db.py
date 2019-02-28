import pymysql.cursors
from models.Data import Data
from models.FeatureExtraction import FeatureExtraction

class Db:

	# def getConnection():
	    # return pymysql.connect(host='35.185.118.181',user='wahyuabied',password='wahyuabied',db='ta',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

	def getConnection():
	    return pymysql.connect(host='127.0.0.1',user='root',password='',db='ta',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

	def insert_crop(paths,id_kondisi,r,st_deviasi,median,mean):
		conn = Db.getConnection()
		myCursor = conn.cursor()
		sql = "INSERT INTO data_crop(name,id_kondisi,r,st_deviasi,median,mean) VALUES(%s,%s,%s,%s,%s,%s)"
		val = (str(paths),id_kondisi,str(r),str(st_deviasi),str(median),str(mean))
		myCursor.execute(sql,val) 
		conn.commit()
		conn.close()

	def insert_crop_tomat(paths,id_kondisi,r,st_deviasi,median,mean):
		conn = Db.getConnection()
		myCursor = conn.cursor()
		sql = "INSERT INTO data_crop_tomat(name,id_kondisi,r,st_deviasi,median,mean) VALUES(%s,%s,%s,%s,%s,%s)"
		val = (str(paths),id_kondisi,str(r),str(st_deviasi),str(median),str(mean))
		myCursor.execute(sql,val) 
		conn.commit()
		conn.close()

	def insert_max_value(mean,median,st_deviasi):
		conn = Db.getConnection()
		myCursor = conn.cursor()
		sql = "INSERT INTO maximum_value(mean,median,st_deviasi) VALUES(%s,%s,%s)"
		val = (str(mean),str(median),str(st_deviasi))
		myCursor.execute(sql,val) 
		conn.commit()
		conn.close()

	def selectData(kondisi):
		conn = Db.getConnection()
		myCursor = conn.cursor()
		sql = 'SELECT * from data_crop WHERE id_kondisi=%s'
		myCursor.execute(sql,kondisi) 
		result = myCursor.fetchall()
		conn.commit()
		conn.close()
		allData = []
		for x in range(0, len(result)):
			data = Data()
			data.setId(result[x]['id'])
			data.setName(result[x]['name'])
			data.setStDeviasi(result[x]['st_deviasi'])
			data.setMean(result[x]['mean'])
			data.setMedian(result[x]['median'])
			data.setIdKondisi(result[x]['id_kondisi'])
			data.setR(result[x]['r'])
			allData.append(data)
		return allData;

	def selectDataTomat(kondisi):
		conn = Db.getConnection()
		myCursor = conn.cursor()
		sql = 'SELECT * from data_crop_tomat WHERE id_kondisi=%s'
		myCursor.execute(sql,kondisi) 
		result = myCursor.fetchall()
		conn.commit()
		conn.close()
		allData = []
		for x in range(0, len(result)):
			data = Data()
			data.setId(result[x]['id'])
			data.setName(result[x]['name'])
			data.setStDeviasi(result[x]['st_deviasi'])
			data.setMean(result[x]['mean'])
			data.setMedian(result[x]['median'])
			data.setIdKondisi(result[x]['id_kondisi'])
			data.setR(result[x]['r'])
			allData.append(data)
		return allData;

	def getMaxValue():
		conn = Db.getConnection()
		myCursor = conn.cursor()
		sql = 'SELECT MAX(CAST(st_deviasi as DECIMAL(9,2))) as st_deviasi,MAX(CAST(mean as DECIMAL(9,2))) as mean, MAX(CAST(median as DECIMAL(9,2))) as median from data_crop where id_kondisi != 6 '
		myCursor.execute(sql)
		result = myCursor.fetchall()
		conn.commit()
		conn.close()
		extractionData = []
		extractionData.append(result[0]['st_deviasi'])
		extractionData.append(result[0]['mean'])
		extractionData.append(result[0]['median'])
		return extractionData

	def selectMaxValue():
		conn = Db.getConnection()
		myCursor = conn.cursor()
		sql = 'SELECT * from maximum_value '
		myCursor.execute(sql) 
		result = myCursor.fetchall()
		conn.commit()
		conn.close()
		extractionData = []
		for x in range(0, len(result)):
			data = FeatureExtraction()
			data.setId(result[x]['id'])
			data.setMedian(result[x]['median'])
			data.setStDeviasi(result[x]['st_deviasi'])
			data.setMean(result[x]['mean'])
			extractionData.append(data)
		return extractionData;
