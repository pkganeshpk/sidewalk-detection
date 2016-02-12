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
    	

  def color_callback(self,data):
  
    	
    try:
      self.color_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print ("Exception:", e)
    
    plt.clf()  
    self.hsv_img = cv2.cvtColor(self.color_img,cv2.COLOR_BGR2HSV)
    hist = cv2.calcHist([self.hsv_img], [0, 1], None, [180, 256], [0, 180, 0, 256])
    
    
    if(self.imgcount == 0):
       self.imgcount = 1
       self.redden_sw()
      # cv2.imshow("red", self.red_img)
       # scv2.imshow("non_red", self.non_red_img)	
       cv2.waitKey(10)	
   	


    self.process_sidewalk()
    print 'Color = ', self.color_img[100][100]	

  def plot_hist(self): 
    pass	


  def redden_sw(self):
    lower = np.array((90,90,90), dtype = "uint8")
    upper = np.array((110,110,110), dtype = "uint8")
    self.red_img = cv2.inRange(self.color_img, lower, upper)

    # print self.red_img[1][0]
    # self.non_red_img = cv2.add(cv2.threshold(self.color_img, 0, 90,  cv2.THRESH_BINARY), cv2.threshold(self.color_img, 111, 255,  cv2.THRESH_BINARY))
				



 			
	
 
  def process_sidewalk(self):
	self.flip_img = self.color_img
	self.depth_in = self.depth_img
        self.depth_out = self.depth_img
	print self.flip_img.shape
	print self.depth_in.shape
 	
	
   
  def depth_callback(self,data):
    #print 'depth Callback'	
    try:
      self.depth_img = self.bridge.imgmsg_to_cv2(data, "16UC1")
    except CvBridgeError as e:
      print ("Exception:", e)

    #cv2.imshow("depth image", self.depth_img)	
    #cv2.waitKey(0)


