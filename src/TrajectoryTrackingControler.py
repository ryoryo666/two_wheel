#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy
import rospkg
import numpy as np
import glob,os
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

#Euler
kx=40.0
ky=80.0
kth=20.0

num=0
new_twist=Twist()

def New_cmd(odom_msg):
	global num,stop
	# Now Pose
	x_p=odom_msg.pose.pose.position.x
	y_p=odom_msg.pose.pose.position.y
	theta_p=odom_msg.pose.pose.orientation.z

	x_diff=Target_Trajectory[num][1]-x_p
	y_diff=Target_Trajectory[num][2]-y_p
	diff = math.sqrt((x_diff**2)+(y_diff**2))

	if diff < 0.2:
		num += 1
		if diff < 0.1:
			num += 1
			if diff < 0.05:
				num += 2
				if diff < 0.01:
					num += 2
	
	shutdown()

	print "Target"
	print "x:{0}	y:{1}".format(Target_Trajectory[num][1],Target_Trajectory[num][2])

	# Refference point on target trajectory
	x_r=Target_Trajectory[num][1]
	y_r=Target_Trajectory[num][2]
	theta_r=Target_Trajectory[num][3]
	v_r=Target_Trajectory[num][4]
	w_r=Target_Trajectory[num][5]

	# Error value
	x_err = (x_r-x_p)*math.cos(theta_p)+(y_r-y_p)*math.sin(theta_p)
	y_err = -(x_r-x_p)*math.sin(theta_p)+(y_r-y_p)*math.cos(theta_p)
	theta_err = theta_r-theta_p

	# New Command Value
	new_twist.linear.x  = v_r*math.cos(theta_err)+kx*x_err
	new_twist.angular.z = w_r+v_r*(ky*y_err+kth*math.sin(theta_err))
	pub.publish(new_twist)

def Set():
	rospy.Subscriber("/Odometry", Odometry, New_cmd)
	rospy.spin()

def shutdown():
	global num,stop
	if num >= stop:
			print "\nFinish\n"
			new_twist.linear.x  = 0.0
			new_twist.angular.z = 0.0
			pub.publish(new_twist)
			rospy.signal_shutdown("Finish")

if __name__=="__main__":
    try:
		rospy.init_node("Kanayama_Method_Controller", disable_signals=True, anonymous=True)
		rospack=rospkg.RosPack()
		pack=rospack.get_path("two_wheel")
		file_list=glob.glob(os.path.join(pack+"/csv", "Target*"))
		file_list.sort()
		print ""
		for i in range(len(file_list)):
			print str(i)+":"+file_list[i].replace(pack+"/csv/", "")
		number=int(raw_input("\nFileNumber>> "))
		Target_Trajectory=np.loadtxt(file_list[number], delimiter = ",")
		stop=len(Target_Trajectory)

		pub=rospy.Publisher("/cmd_vel", Twist, queue_size=2)
		Set()

    except rospy.ROSInterruptException: pass
