import rosbag
import cv2


bag = rosbag.Bag('../realsense.bag', 'r')

# Get list of topics
for topic, msg, t in bag.read_messages(topics = ['/camera/color/image_raw']):
   print "!"	
   clrimg = CvBridge.bridge.imgmsg_to_cv2(data, "bgr8")
   cv2.imshow('image',clrimg)	
	
bag.close()
