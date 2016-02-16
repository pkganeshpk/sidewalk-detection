# $(env bash)

for i in $(seq 1 10)
do 
	rosbag play ../realsense.bag 
done

 
