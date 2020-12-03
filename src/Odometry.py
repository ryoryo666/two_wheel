#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from two_wheel.msg import RPM2_Time
from nav_msgs.msg import Odometry

wr = 0.03825	# Wheel Radius [m]
d  = 0.00615	# Wheel-Center distance [m]
dt = 0.0
last_time=0.0

last_x=0.0
last_y=0.0
last_th=0.0
last_time=0.0

def odom(msg):
	global last_x,last_y,last_th,last_time
	R_data = msg.r_data
	L_data = msg.l_data
	dt = msg.time - last_time
	vr = round(R_data,1)*((2*math.pi)/60.0) * wr 
	vl = round(L_data,1)*((2*math.pi)/60.0) * wr 
	w = (vr-vl)/(2*d)

	dL_r = vr*dt
	dL_l = vl*dt
	dth = w *dt
	dL = (dL_r + dL_l)/2
	

	if dth < 0.000001 or dth==0.0 :
		Odom.pose.pose.position.x = round(last_x + dL * math.cos(last_th+(dth/2)),3)
		Odom.pose.pose.position.y = round(last_y + dL * math.sin(last_th+(dth/2)),3)

	else :
		p = dL/dth
		dL1 = 2*p*math.sin(dth/2)
		Odom.pose.pose.position.x = round(last_x + dL1 * math.cos(last_th+(dth/2)),3)
		Odom.pose.pose.position.y = round(last_y + dL1 * math.sin(last_th+(dth/2)),3)

	Odom.pose.pose.orientation.z = round(last_th + dth,4)
	Odom.twist.twist.linear.x = (vr + vl)/2
	Odom.twist.twist.angular.z = w
	pub.publish(Odom)
	print(Odom)

	last_x = Odom.pose.pose.position.x
	last_y = Odom.pose.pose.position.y
	last_th = Odom.pose.pose.orientation.z
	last_time = msg.time

	

def Set():
	rospy.init_node("Odom")
	rospy.Subscriber("/rpm_data", RPM2_Time, odom)
	rospy.spin()

if __name__=="__main__":
	try:
		Odom=Odometry()
		pub=rospy.Publisher("/Odometry", Odometry, queue_size=2)
		Set()

	except rospy.ROSInterruptException: pass
