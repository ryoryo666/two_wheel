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
kx = 1.9
ky = 15.0
kth = 10.0

num = 1
new_twist=Twist()

def New_cmd(odom_msg):
	global num,stop
	# Now Pose
	x_p=odom_msg.pose.pose.position.x
	y_p=odom_msg.pose.pose.position.y
	theta_p=odom_msg.pose.pose.orientation.z

	while (num < stop):
		x_diff=Reference_Path[num][1]-x_p
		y_diff=Reference_Path[num][2]-y_p
		diff = math.sqrt((x_diff**2)+(y_diff**2))
		if 0.1 < diff:
			print "Update"
			break
		num+=1

	shutdown()

	print "Reference"
	print "x:{0}	y:{1}".format(Reference_Path[num][1],Reference_Path[num][2])

	# Reference point on target trajectory
	x_r=Reference_Path[num][1]
	y_r=Reference_Path[num][2]
	theta_r=Reference_Path[num][3]
	v_r=Reference_Path[num][4]
	w_r=Reference_Path[num][5]

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
		print ""
		for i in range(len(file_list)):
			print str(i)+":"+file_list[i].replace(pack+"/csv/", "")
		number=int(raw_input("\nFileNumber>> "))
		Reference_Path=np.loadtxt(file_list[number], delimiter = ",")
		stop=len(Reference_Path)

		pub=rospy.Publisher("/cmd_vel", Twist, queue_size=2)
		Set()

    except rospy.ROSInterruptException: pass
