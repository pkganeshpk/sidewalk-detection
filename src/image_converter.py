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



class image_converter:

  sidewalk_colors = [ [90, 105] , [90, 105], [90, 105]]

  def __init__(self):
    print 'Image_converter'	
    rospy.init_node('sidewalk_detector', anonymous = True)
    self.bridge = CvBridge()

    self.color_sub = rospy.Subscriber("/camera/color/image_raw",Image,self.color_callback)
    self.depth_sub = rospy.Subscriber("/camera/depth/image_raw", Image,self.depth_callback)

    self.color_pub = rospy.Publisher("/color",Image, queue_size = 1)
    self.depth_in_pub = rospy.Publisher("/depth/points_in", Image , queue_size = 1)	
    self.depth_out_pub = rospy.Publisher("/depth/points_out",Image, queue_size = 1)

    self.imgcount = 0
    self.p_thresh = 0.7 # Threshold probability for 		
    	

  def color_callback(self,data):
    	
    try:
      self.color_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print ("Exception:", e)
  
    if(self.imgcount == 0):
       self.imgcount = 1 	 
       # Get training histogram & background histogram
       self.get_hist_sw()
       self.get_hist_bg()
       print 'size of histograms = ', self.hist_sw.shape
       assert(self.hist_bg.shape == self.hist_sw.shape)		
    
       cv2.imshow('sidewalk', self.hsv_sw)
       cv2.waitKey(5)	 
       print 'correl = ', cv2.compareHist(self.hist_sw, self.hist_bg, cv2.cv.CV_COMP_CORREL)
     
    else:
	self.color_new_img()
        cv2.imshow('red image', self.red_img)
    	
  def color_new_img(self):
     print "!"
     self.hsv_cur = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2HSV)
     rows = self.hsv_cur.shape[0]
     cols = self.hsv_cur.shape[1]
     #assert(self.hist_sw.shape == self.hsv_cur.shape)


     self.red_img = self.color_img[:]	
     for i in xrange(rows):
	for j in xrange(cols):
		
		[hue,sat] = self.hsv_cur[i][j][0:2]
                assert(hue <= self.hist_sw.shape[0] and sat <= self.hist_sw.shape[1])
		
		sum_freq = float(self.hist_bg[hue][sat] + self.hist_sw[hue][sat])
		if (sum_freq > 0):	
			prob = float(self.hist_sw[hue][sat]) / sum_freq
			if (prob > self.p_thresh):
				self.red_img[i][j] = [255, 0, 0] # set to red color 
				 



  def get_hist_bg(self):
    
     self.bg_img = self.color_img[200:300,100:200]
     height = self.bg_img.shape[0]
     width = self.bg_img.shape[1]	
     for i in xrange(height):
	for j in xrange(width):
		row = np.random.rand() * self.color_img.shape[0] 				     
		col = np.random.rand() * self.color_img.shape[1]
                self.bg_img[i][j] =  self.color_img[row][col] 
     
      		
     self.hsv_bg = cv2.cvtColor(self.bg_img, cv2.COLOR_BGR2HSV)
     self.hist_bg = cv2.calcHist([self.hsv_bg], [0, 1], None, [180, 256], [0, 180, 0, 256]) 
     ''' Didn't normalize '''

  def get_hist_sw(self):
    self.hsv_sw = cv2.cvtColor(self.color_img[50:200,100:200], cv2.COLOR_BGR2HSV)
    self.hist_sw = cv2.calcHist([self.hsv_sw], [0, 1], None, [180, 256], [0, 180, 0, 256])
    print 'sidewalk histogram:', self.hist_sw.shape
    print 'sidewalk hsv:', self.hsv_sw.shape	
	
 	
	
   
  def depth_callback(self,data):
    #print 'depth Callback'	
    try:
      self.depth_img = self.bridge.imgmsg_to_cv2(data, "16UC1")
    except CvBridgeError as e:
      print ("Exception:", e)

    #cv2.imshow("depth image", self.depth_img)	
    #cv2.waitKey(0)


