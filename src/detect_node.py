import rosbag
import cv2
from image_converter import image_converter
import rospy

I = image_converter('images/frame0000.jpg','/images/frame%4d.jpg')
I.run_no_ros()
#rospy.spin()





