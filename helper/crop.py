import cv2
import numpy as np
import random as rng

class crop:
	
	def cropping(temp,path):

		img = cv2.imread(temp+path)
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		th, threshed = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

		## (2) remove noise
		kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11,11))
		morphed = cv2.morphologyEx(threshed, cv2.MORPH_CLOSE, kernel)

		## (3) Max area
		_, cnts, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		cnt = sorted(cnts, key=cv2.contourArea)[-1]

		## (4) Crop and save
		x,y,w,h = cv2.boundingRect(cnt)
		dst = img[y:y+h, x:x+w]
		# cv2.imshow('show',dst)
		# location = str(temp)+path
		location = 'cropTomat/'+str(temp)+path
		# location = 'cropTesting/'+str(temp)+path
		cv2.imwrite(location,dst)
		return location

	def segment(image):
	    """
	    Object Segmentation in Uniform Background using Edge Detection
	    """
	 
	    # convert BGR image to grayscale
	    # image_gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
	    image_gray = cv2.GaussianBlur(image, (5, 5), 0)
	 
	    # get contours
	    edges = cv2.Canny(image_gray, 20, 60)
	    _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	    drawing = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)
	    for i in range(len(contours)):
	    	color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
	    	cv2.drawContours(drawing, contours, i, color, 2, cv2.LINE_8, hierarchy, 0)
	    cv2.imshow('Contours', drawing)
	 
	    # masking object
	    # result = np.zeros(image.shape, dtype='uint8')
	    # result[mask > 0, :] = image[mask > 0, :]
	 
	    return drawing

	def segmentasi(image):
	    """
	    Object Segmentation in Uniform Background using Edge Detection
	    """
	    ret, thresh = cv2.threshold(image, 127, 255, 0)
	    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	    cv2.drawContours(image, contours, -1, (0,255,0), 3)

	    return image
	 