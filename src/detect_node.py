#!/usr/bin/python

'''
Ganesh P Kumar
Marble coding challenge: sidewalk detection
gpkumar@asu.edu
'''


import rosbag
import cv2
from image_converter import image_converter
import rospy


I = image_converter('images/frame0000.jpg',)
rospy.spin()





