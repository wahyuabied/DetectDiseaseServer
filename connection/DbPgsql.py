from sqlalchemy import create_engine,text
from model.Data import Data
from model.FeatureExtraction import FeatureExtraction

class DbPgsql:
	def getConnection():
	return create_engine("postgresql://yesvhtxmhpggfa:fb61e607ec6b7e38aa5f2c30466f60f48b806288800efb8f5d6dda0f65a827c3@ec2-184-72-234-230.compute-1.amazonaws.com/df2dpfgrti796s")

	def insert_crop(paths,id_kondisi,r,st_deviasi,median,mean):
	conn = getConnection()
	conn.execute(text("INSERT INTO DATA_CROP(name,id_kondisi,r,st_deviasi,median,mean) VALUES (:paths,:id_kondisi,:r,:st_deviasi,:median,:mean)"),{"paths":paths,"id_kondisi":id_kondisi,"r":r,"st_deviasi":st_deviasi,"median":median,"mean":mean})

	def insert_max_value(mean,median,st_deviasi):
	conn = getConnection()
	conn.execute(text("INSERT INTO MAXIMUM_VALUE(mean,median,st_deviasi) VALUES(:mean,:median,:st_deviasi)"),{"mean":mean,"median":median,"st_deviasi":st_deviasi,})