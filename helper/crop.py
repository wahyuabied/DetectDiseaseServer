import cv2
import numpy as np
import random as rng
from skimage import color
from PIL import Image
import os


class crop:
	
	def cropping(path):

		img = cv2.imread(path,1)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		th, threshed = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

		## (2) remove noise
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
		morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

		## (3) Max area
		#sekarang findCountour hanya mengembalikan contour dan hierarcy cnts, _ = 
		# _, cnts, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) windows
		cnts, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #linux
		cnt = sorted(cnts, key=cv2.contourArea)[-1]

		## (4) Crop and save
		x,y,w,h = cv2.boundingRect(cnt)
		dst = img[y:y+h, x:x+w]
		resize = cv2.resize(dst,(256,256))
		cv2.imwrite(path,resize)
		return path

	def removeBackground(imgo):
	    img = cv2.imread(imgo,1)
	    height, width = img.shape[:2]

	    mask = np.zeros(img.shape[:2],np.uint8)

	    bgdModel = np.zeros((1,65),np.float64)
	    fgdModel = np.zeros((1,65),np.float64)

	   #Hard Coding the Rect The object must lie within this rect.
	    rect = (15,15,width-30,height-30)
	    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
	    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	    img1 = img*mask[:,:,np.newaxis]
	    newmask = color.rgb2gray(img)

	    mask[newmask == 0] = 0
	    mask[newmask == 255] = 1
	    mask, bgdModel, fgdModel = cv2.grabCut(img1,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
	    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	    img1 = img1*mask[:,:,np.newaxis]

	    #crop background
	    background = img - img1
	    background[np.where((background > [0,0,0]).all(axis = 2))] = [255,255,255]

	    final = background + img1
	    cv2.imwrite(imgo+".png",final)

	    return imgo+".png"

	def removeBackgroundTraining(path,name,imgo):
	    # cv2.imshow('awal', imgo)
	    height, width = imgo.shape[:2]

	    mask = np.zeros(imgo.shape[:2],np.uint8)

	    bgdModel = np.zeros((1,65),np.float64)
	    fgdModel = np.zeros((1,65),np.float64)

		#Hard Coding the Rect The object must lie within this rect.
	    rect = (15,15,width-30,height-30)
	    cv2.grabCut(imgo,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
	    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	    img1 = imgo*mask[:,:,np.newaxis]
	    newmask = color.rgb2gray(imgo)

	    mask[newmask == 0] = 0
	    mask[newmask == 255] = 1
	    mask, bgdModel, fgdModel = cv2.grabCut(img1,mask,None,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_MASK)
	    mask = np.where((mask==2)|(mask==0),0,1).astype('uint8')
	    img1 = img1*mask[:,:,np.newaxis]

	    #crop background
	    background = imgo - img1
	    background[np.where((background > [0,0,0]).all(axis = 2))] = [255,255,255]
	    # cv2.imshow('background', background)
	    # background2 = crop.removeNoisy(background)

	    final = background + img1
	    # # dst = final[y:y+h, x:x+w]
	    cv2.imwrite("noBackground/"+path+name+".jpg",final)
	    crop.convertPNG("noBackground/"+path,name)

	    return "noBackground/"+path+name


	#Harus JPG ,background putih akan di buat transparent
	def convertPNG(path,nameFile):
	    img = Image.open(path+nameFile+".jpg")
	    img = img.convert("RGBA")
	    pixdata = img.load()

	    width, height = img.size
	    for y in range(height):
	        for x in range(width):
	            if pixdata[x, y] == (255, 255, 255, 255):
	                pixdata[x, y] = (255, 255, 255, 0)

	    os.remove(path+nameFile+".jpg")
	    img.save(path+nameFile+".png", "PNG")
		
	    # dst = final[y:y+h, x:x+w]
	    # cv2.imwrite("noBack/"+path+name,final)

	    # return final
