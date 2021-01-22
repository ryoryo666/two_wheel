#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Kanayama Control Method

import math
import rospy
import rospkg
import numpy as np
import glob,os
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

kx = 0.5
ky = 10.0
kth = 5.0

num = 0
new_twist=Twist()

def New_cmd(odom_msg):
	global num,stop
	# Now Pose
	x_p=odom_msg.pose.pose.position.x
	y_p=odom_msg.pose.pose.position.y
	theta_p=odom_msg.pose.pose.orientation.z

	shutdown()

	print "Reference"
	print "x:{0}	y:{1}".format(Reference_Trajectory[num][1],Reference_Trajectory[num][2])

	# Reference point on target trajectory
	x_r=Reference_Trajectory[num][1]
	y_r=Reference_Trajectory[num][2]
	theta_r=Reference_Trajectory[num][3]
	v_r=Reference_Trajectory[num][4]
	w_r=Reference_Trajectory[num][5]
	num += 1

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
		file_list=glob.glob(os.path.join(pack+"/csv", "Reference*"))
		file_list.sort()
		print "\nSelect Reference Trajectory\n"
		for i in range(len(file_list)):
			print str(i)+":"+file_list[i].replace(pack+"/csv/", "")
		number=int(raw_input("\nFileNumber>> "))
		Reference_Trajectory=np.loadtxt(file_list[number], delimiter = ",")
		stop=len(Reference_Trajectory)

		pub=rospy.Publisher("/cmd_vel", Twist, queue_size=2)
		Set()

    except rospy.ROSInterruptException: pass
