# sidewalk-detection


## Implmentation notes

The implementation uses the approach given in the paper linked, **except** for the issues given later below. To run, place a training image in "src/images/frame0000.jpg" to get the sidewalk and background areas.

shell1$ rosplay realsense.bag

shell2$ cd src; python detect_node.py

This will publish the images to the concerned topics, as well as dump output files in the out/ folder.

### Issues
Here are the big issues I faced: The "4 sidewalk histograms" referred to in the Seng paper are nowhere defined. Neither do the referenced papers in the bibliography give any idea. As a result, I had to **make do** with whatever I understood. The resulting algorithm identifies many of the sidewalk pixels (but certainly not all) //and this affects the overall performance very critically//. 



## Problem Statement
Sidewalk detection algorithm using the Intel Real Sense Camera. Build a ROS node called “sidewalk_detector” that consumes the replayed data of this rosbag and outputs the following topics:

(1) /sidewalk_detector/color/image_raw

(2) /sidewalk_detector/depth/points_in

(3) /sidewalk_detector/depth/points_out

Definitions: 

where (1) outputs the images from the topic "/camera/color/image_raw” with a visible highlight (e.g. a red mask) mapped over the set of pixels that are considered to be INSIDE the sidewalk

where (2) outputs a point cloud which contains the subset of points from the point cloud output by the topic "/camera/depth/points” that are considered to be INSIDE the sidewalk

where (3) outputs a point cloud which contains the subset of points from the point cloud output by the topic "/camera/depth/points” that are considered to be OUTSIDE the sidewalk

By “inside” we mean any point or pixel that maps to a piece of sidewalk, whether or not we could navigate there. So, if we were doing it by hand, we’d open an image editor and fill in all the pixels that we perceive as being the sidewalk. 

Why?

The intention of this node is to be general enough to be able to work for not just this rosbag recording but for any other that we might throw at it. As such, we have a secondary data set of a nearby similar length of sidewalk that we will also test it on once you’re done. So, try to go for an approach that has a high likelihood of working for any reasonable sidewalk - we don’t care which approach as long as it works well.

How to Structure the Code:

Make sure that your ROS node runs on Indigo / Ubuntu 14.04

It will be running on an i7 NUC with 16GB of fast memory and a speed 250GB SSD.

Ideally, put the code up on a publicly accessible GitHub repo. It should be structured as a ROS node so that we can clone it into a local workspace and run it easily on our other data sets. Bonus points if we see a few examples of your output images in the git repo as well, say, under an “examples” folder.

Need a little extra help?

Also this article has photos as an example of what we want the output to be like: http://users.csc.calpoly.edu/~jseng/papers/ccsc_paper.pdf 
