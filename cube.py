#!/usr/bin/env python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import cv2
import numpy as np
import os
import logging
logging.basicConfig(level=logging.DEBUG)

# 28 inches from the center of robot to the end for the arm
# Minimum distance to pick up well is 21 inches with [28, 40, 125] - [75, 175, 230]
# Cube area at 96 inches away is about 1900
# Noise max is about 50

# Restore defaults for cam
os.system('v4l2-ctl -c exposure=12q0')
os.system('v4l2-ctl -c contrast=32')

#Creating Windows
cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.resizeWindow("frame", 100,100)
cv2.namedWindow("original", cv2.WINDOW_NORMAL)
cv2.resizeWindow("original", 100,100)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
#Strings
hh = 'hue high'
sh = 'saturation high'
vh = 'value high'

hl = 'hue low'
sl = 'saturation low'
vl = 'value low'
                      
#Creating Trackbars with defaults
#Lower
cv2.createTrackbar(hl, 'image', 25, 179, lambda:none)	
cv2.createTrackbar(sl, 'image', 80, 255, lambda:none)	
cv2.createTrackbar(vl, 'image', 120, 255, lambda:none)	
#Upper
cv2.createTrackbar(hh, 'image', 70, 179, lambda:none)	
cv2.createTrackbar(sh, 'image', 185, 255, lambda:none)	
cv2.createTrackbar(vh, 'image', 255, 255, lambda:none)	

#Erosion
erosionKernel = np.ones((3,3), np.uint8)
dilateKernel = np.ones((0,0), np.uint8)

cap = cv2.VideoCapture(0)
count = 0
i = 0

#Loop
while True:
	error = 0
        
	#reading every frame
	ret, img = cap.read()
	default = img
	height, width = img.shape[:2]
	
	#increased upper HSV vals	
	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break
	
	# Convert the image from RGB to HSV color space.  This is required for the next operation.
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
	#Read Trackbar Position
	ahl=cv2.getTrackbarPos(hl, 'image')
	asl=cv2.getTrackbarPos(sl, 'image')
	avl=cv2.getTrackbarPos(vl, 'image')
	ahh=cv2.getTrackbarPos(hh, 'image')
	ash=cv2.getTrackbarPos(sh, 'image')
	avh=cv2.getTrackbarPos(vh, 'image')

	# Make array
	hsvl = np.array([ahl,asl,avl])
	hsvh = np.array([ahh,ash,avh])
	# Apply range on a mask
	mask = cv2.inRange(hsv, hsvl, hsvh)
	res = cv2.bitwise_and(img, img, mask=mask)

	# Create a new image that contains yellow where the color was detected
	img = cv2.inRange(hsv, hsvl, hsvh)
	img = cv2.erode(img, erosionKernel, iterations =1)
	img = cv2.dilate(img, dilateKernel, iterations=1)

	# Blurring operation helps forthcoming contours work better
	img= cv2.blur(img, (3,3))
	    
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv
	# Find contours
	# contours, h = cv2.findContour(thresh, 1, 2)

	#for cnt in contours:
	#	approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
	#	if len(approx) == 4 :
	#		print "cube"
	#		cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
	#	elif len (approx) > 15 :
	#		print "circle"
	#		cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)
	#(_, cnts, _) = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    

	# Makes the first contour the largest
	#contours = sorted(cnts, key = cv2.contourArea, reverse = True)

	# If no contours are detected, then don't try to process them or you'll get an error:
	#if len(contours) > 0:
	#	cnt1 = contours[0]
	#	area = cv2.contourArea(cnt1)
		
		# Draw a minimum area rectangle around the contour
	#	rect1 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt1)))
		
		# Draw the contour over image
	#	cv2.drawContours(img, [rect1], -1, (255, 0, 0), 2)
	#	M1 = cv2.moments(cnt1)
	#	cx1 = int(M1['m10']/M1['m00'])
	#	cy1 = int(M1['m01']/M1['m00'])
		
		#draw center of cube on image in red
	#	cv2.circle(img,(cx1,cy1), 50, (0,0,255))

		#display center of image on img in white
	#	centX = int(width/2)
	#	centY = int(height/2)

		#error to be sent over network tables
#		error = centX - cx1
#		if area < 200:
#                       error = 0 
#		cv2.circle(img, (centX, centY),30, (255,255,255))

	cv2.imshow('frame', img)
	cv2.imshow('original', default)
	cv2.imshow('image', res)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
