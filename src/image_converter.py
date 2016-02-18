#!/usr/bin/env python
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from matplotlib import pyplot as plt
import time
import math

class image_converter:

  sidewalk_colors = [ [90, 105] , [90, 105], [90, 105]]

  def __init__(self, ref_img_path, img_dir):
    print 'Image_converter'	
 

    self.imgcount = 0
    self.p_thresh = 0.5 # Threshold probability for 
    self.ref_img = cv2.imread(ref_img_path)			
    	
    self.get_hist_sw()
    self.get_hist_bg()
    assert(self.hist_bg.shape == self.hist_sw.shape)			 
    print 'correl = ', cv2.compareHist(self.hist_sw, self.hist_bg, cv2.cv.CV_COMP_CORREL)
    self.cap = 	cv2.VideoCapture(img_dir)
    self.bgsub = cv2.BackgroundSubtractorMOG()	

  def run_no_ros(self):  
    while(self.cap.isOpened()):
	    ret, self.color_img = self.cap.read()
	    self.find_lines()	

	    self.color_new_img()
            cv2.imshow('color image', self.color_img)
            # cv2.imshow('edges', self.edges)

    	    cv2.waitKey(20) 
	    time.sleep(5)


  def find_lines(self):

	    gray = cv2.cvtColor(self.color_img,cv2.COLOR_BGR2GRAY)
	    self.edges = cv2.Canny(gray,0,250,apertureSize = 3)
	    minLineLength = 50
	    maxLineGap = 20
	    self.lines = cv2.HoughLinesP(self.edges, 1, math.pi / 180, 100,minLineLength,maxLineGap)
	   # for x1,y1,x2,y2 in self.lines[0]:
    		#cv2.line(self.red_img,(x1,y1),(x2,y2),(0,255,255),2)
	    		

  def color_callback(self,data):
    try:
      self.color_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print ("Exception:", e)
  
  
	
  
	
    	
  def color_new_img(self):
     self.hsv_cur = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2HSV)
     rows = self.hsv_cur.shape[0]
     cols = self.hsv_cur.shape[1]
    
     assert(self.hsv_cur.shape == self.color_img.shape)
     self.thres_img = cv2.inRange(self.color_img, np.array([80,80,80]), np.array([130, 130, 130]))	

     self.red_img = self.color_img[:]

     
   

     for i in xrange(rows):
	for j in xrange(cols):
		
		[hue,sat] = self.hsv_cur[i][j][0:2]
                assert(hue <= self.hist_sw.shape[0] and sat <= self.hist_sw.shape[1])
		
		sum_freq = float(self.hist_bg[hue][sat] + self.hist_sw[hue][sat])
		if (sum_freq > 0 ):
		
			prob = float(self.hist_sw[hue][sat]) / sum_freq
			if (prob > self.p_thresh and self.thres_img[i][j] == 255  ):
				
				self.red_img[i][j] = [ 0, 0, 255] # set to red color 


  
				 
  def threshold_sw(self):
     pass


  def get_hist_bg(self):
    
     self.bg_img = self.ref_img[50:200,200:450]
     height = self.bg_img.shape[0]
     width = self.bg_img.shape[1]	
     for i in xrange(height):
	for j in xrange(width):
		
		while (True):
			row = int(np.random.rand() * self.ref_img.shape[0]) 				     
			col = int(np.random.rand() * self.ref_img.shape[1])
			if (50 <= row <= 200 and 200 <= col <= 450):
				continue
			else:
				break
			
                self.bg_img[i][j] =  self.ref_img[row][col] 
     
      		
     self.hsv_bg = cv2.cvtColor(self.bg_img, cv2.COLOR_BGR2HSV)
     self.hist_bg = cv2.calcHist([self.hsv_bg], [0, 1], None, [256, 256], [0, 256, 0, 256]) 
     self.hist_bg /= self.hsv_bg.shape[0]	


  def get_hist_sw(self):
    self.hsv_sw = cv2.cvtColor(self.ref_img[50:200,200:450], cv2.COLOR_BGR2HSV)
  	
    self.hist_sw = cv2.calcHist([self.hsv_sw], [0, 1], None, [256, 256], [0, 256, 0, 256])
    print 'sidewalk histogram:', self.hist_sw.shape
    print 'sidewalk hsv:', self.hsv_sw.shape	
    self.hist_sw /= self.hsv_sw.shape[0]
    print self.hist_sw
	
 	
	
   
  def depth_callback(self,data):
    #print 'depth Callback'	
    try:
      self.depth_img = self.bridge.imgmsg_to_cv2(data, "16UC1")
    except CvBridgeError as e:
      print ("Exception:", e)

    #cv2.imshow("depth image", self.depth_img)	
    #cv2.waitKey(0)


