#!/usr/bin/env python

'''
Ganesh P Kumar
Marble coding challenge: sidewalk detection
gpkumar@asu.edu
'''


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

  def __init__(self, ref_img_path):

    self.p_thresh = 0.9 # Threshold probability for sidewalk 
    self.ref_img = cv2.imread(ref_img_path) # Training image
			    	
    self.get_hist_sw() # Get initial sidewalk and non-sidewalk = background
    self.get_hist_bg()

    assert(self.hist_bg.shape == self.hist_sw.shape)	# Just a checks		 

    rospy.init_node('sidewalk_detection')
    self.bridge = CvBridge() # ROS <-> OpenCV

    self.color_sub = rospy.Subscriber("/camera/color/image_raw",Image,self.color_callback)
    self.depth_sub = rospy.Subscriber("/camera/depth/image_raw", Image,self.depth_callback)
    
    self.color_pub = rospy.Publisher("/sidewalk_detector/color",Image, queue_size = 1)
    self.depth_in_pub = rospy.Publisher("/sidewalk_detector/depth/points_in", Image , queue_size = 1)	
    self.depth_out_pub = rospy.Publisher("/sidewalk_detector/depth/points_out",Image, queue_size = 1)

    self.red_img = None
    self.depth_img_in = None
    self.depth_img_out = None 
    self.seq_no = 0	
	    		

  def color_callback(self,data):
    try:
       self.color_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print ("Subscription Exception:", e)
    
    self.seq_no += 1 

    self.hsv_cur = cv2.cvtColor(self.color_img, cv2.COLOR_BGR2HSV)
    rows = self.hsv_cur.shape[0]
    cols = self.hsv_cur.shape[1]
    
    assert(self.hsv_cur.shape == self.color_img.shape)
    self.thres_img = cv2.inRange(self.color_img, np.array([80,80,80]), np.array([130, 130, 130]))	# Threshold for sidewalk colors (not used now) 

    self.red_img = self.color_img.copy()
   
  

    for i in xrange(rows):
       for j in xrange(cols):
		
	    [hue,sat] = self.hsv_cur[i][j][0:2]
            assert(hue <= self.hist_sw.shape[0] and sat <= self.hist_sw.shape[1])

            sum_freq = float(self.hist_bg[hue][sat] + self.hist_sw[hue][sat])
	    if (sum_freq > 0 ):
		
		prob = float(self.hist_sw[hue][sat]) / sum_freq  # Compute P(Sidewalk)
		if (prob > self.p_thresh and self.thres_img[i][j] == 255  ):
			self.red_img[i][j] = [ 0, 0, 255 ] # set to red color

    cv2.imwrite("out/red_img_" + str(self.seq_no) + ".jpg", self.red_img) 

    try:
      self.color_pub.publish(self.bridge.cv2_to_imgmsg(self.red_img, "bgr8"))
    except CvBridgeError as e:
      print "Publication Exception:", e 

  # Get histogram of background
  def get_hist_bg(self):
    
     self.bg_img = self.ref_img[50:200,200:450]
     height = self.bg_img.shape[0]
     width = self.bg_img.shape[1]	
     for i in xrange(height):
	for j in xrange(width):
		
		while (True):
			row = int(np.random.rand() * self.ref_img.shape[0]) 	 # Choose random pixels ...			     
			col = int(np.random.rand() * self.ref_img.shape[1])
			if (50 <= row <= 200 and 200 <= col <= 450): # ... not from sidewalk range
				continue
			else:
				break
			
                self.bg_img[i][j] =  self.ref_img[row][col] 
     
      		
     self.hsv_bg = cv2.cvtColor(self.bg_img, cv2.COLOR_BGR2HSV)
     self.hist_bg = cv2.calcHist([self.hsv_bg], [0, 1], None, [256, 256], [0, 256, 0, 256]) 
    
     self.hist_bg_dest = cv2.normalize(self.hist_bg, alpha = 0.0, beta = 1.0, norm_type = cv2.NORM_MINMAX)    
     self.hist_bg = self.hist_bg_dest.copy()
     	
	

  # Get hist of sidewalk for training
  def get_hist_sw(self):
    self.hsv_sw = cv2.cvtColor(self.ref_img[50:200,200:450], cv2.COLOR_BGR2HSV) # this is the "image in front of robot", representing sidewalk
    self.hist_sw = cv2.calcHist([self.hsv_sw], [0, 1], None, [256, 256], [0, 256, 0, 256])
    self.hist_sw_dest = cv2.normalize(self.hist_sw, alpha = 0.0, beta = 1.0, norm_type = cv2.NORM_MINMAX)    
    self.hist_sw = self.hist_sw_dest.copy()
	
    
	
 	
	
   
  def depth_callback(self,data):
    #print 'depth Callback'	
    try:
      self.depth_img = self.bridge.imgmsg_to_cv2(data, "16UC1") # 16UC1 works for depth images
    except CvBridgeError as e:
      print ("Depth subscriber Exception:", e)
     
    # Depth and colour images are of different sizes (possibly)
    row_ratio = float(self.color_img.shape[0]) / float(self.depth_img.shape[0])  
    col_ratio = float(self.color_img.shape[1]) / float(self.depth_img.shape[1])  


    self.depth_img_in = self.depth_img.copy()
    self.depth_img_out = self.depth_img.copy()
    print "!"

    red_count = 0
    for i in xrange(self.red_img.shape[0]):
	for j in xrange(self.red_img.shape[1]):
		i2 = int (i / row_ratio)
		j2 = int (j / col_ratio ) 
		
		if (self.red_img[i][j][0] == 0 and self.red_img[i][j][1] == 0 and self.red_img[i][j][2] == 255):
			self.depth_img_out[i2][j2] = [0] # From max
		else:
			self.depth_img_in[i2][j2] = [0]
 			red_count = red_count + 1

    
    cv2.imwrite( "out/depth_in" + str(self.seq_no) + ".jpg", self.depth_img_in )
    cv2.imwrite( "out/depth_out" + str(self.seq_no) + ".jpg", self.depth_img_out)   
 

    try:
      self.depth_in_pub.publish(self.bridge.cv2_to_imgmsg(self.depth_img_in, "16UC1"))
      self.depth_out_pub.publish(self.bridge.cv2_to_imgmsg(self.depth_img_out, "16UC1"))
    except CvBridgeError as e:
      print "Publication Exception:", e 			


