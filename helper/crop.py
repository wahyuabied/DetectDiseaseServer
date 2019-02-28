import cv2

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
		# location = 'cropTomat/'+str(temp)+path
		location = 'cropTesting/'+str(temp)+path
		cv2.imwrite(location,dst)
		return location