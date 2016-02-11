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
    rospy.init_node('image_converter', anonymous = True)
    self.bridge = CvBridge()
    self.color_sub = rospy.Subscriber("/camera/color/image_raw",Image,self.color_callback)
    self.depth_sub = rospy.Subscriber("/camera/depth/image_raw", Image,self.depth_callback)

    	

  def color_callback(self,data):
  	
    try:
      self.color_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print ("Exception:", e)
    
    plt.clf()  
    self.hsv_img = cv2.cvtColor(self.color_img,cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([self.hsv_img], [0, 1], None, [180, 256], [0, 180, 0, 256])
    

    #self.color_img[100,100] = [0, 0 ,255]
    self.process_sidewalk()
    cv2.imshow('color image', self.flip_img)
    #plt.imshow(hist,interpolation = 'nearest') 
    cv2.waitKey(1) 	

 
  def process_sidewalk(self):
	self.flip_img = cv2.flip(self.color_img, -1)
	 
	print " Shape : ",self.flip_img.shape
	for i in xrange(self.flip_img.shape[0]):
		for j in xrange(self.flip_img.shape[1]):
			px = self.flip_img[i][j]
			if min(px) <= 110 and max(px) >= 90:
				self.flip_img[i][j] = [0,0,255]
   
  def depth_callback(self,data):
    #print 'depth Callback'	
    try:
      self.depth_img = self.bridge.imgmsg_to_cv2(data, "16UC1")
    except CvBridgeError as e:
      print ("Exception:", e)

    #cv2.imshow("depth image", self.depth_img)	
    #cv2.waitKey(0)


