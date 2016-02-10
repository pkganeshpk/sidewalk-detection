import rosbag
import cv2
from cv_bridge import CvBridge, CvBridgeError

bag = rosbag.Bag('../realsense.bag', 'r')

# Get list of topics
for topic, msg, t in bag.read_messages(topics = ['/camera/color/image_raw']):
   cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
	
bag.close()
