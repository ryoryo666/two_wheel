#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from two_wheel.msg import RPM2_Time
from nav_msgs.msg import Odometry

wr = 0.03825	# Wheel Radius [m]
d  = 0.00615	# Wheel-Center distance [m]

def odom(msg):
	global last_x,last_y,last_th,last_time
	R_data = msg.r_data
	L_data = msg.l_data
	now_time = rospy.Time.now()
	dt = now_time - last_time
	dt = dt.secs + dt.nsecs/10.0**9

	vr = round(R_data,2)*((2*math.pi)/60.0) * wr
	vl = round(L_data,2)*((2*math.pi)/60.0) * wr
	w = (vr-vl)/(2*d)

	dL_r = vr*dt
	dL_l = vl*dt
	dth = w *dt
	dL = (dL_r + dL_l)/2

	Odom.header.stamp.secs = now_time.secs - start_Time.secs
	Odom.header.stamp.nsecs = now_time.nsecs - start_Time.nsecs

	if dth < 0.000001 or dth==0.0 :
		Odom.pose.pose.position.x = last_x + dL * math.cos(last_th+(dth/2))
		Odom.pose.pose.position.y = last_y + dL * math.sin(last_th+(dth/2))
	else :
		p = dL/dth
		dL1 = 2*p*math.sin(dth/2)
		Odom.pose.pose.position.x = last_x + dL1 * math.cos(last_th+(dth/2))
		Odom.pose.pose.position.y = last_y + dL1 * math.sin(last_th+(dth/2))

	Odom.pose.pose.orientation.z = last_th + dth
	Odom.twist.twist.linear.x = (vr + vl)/2
	Odom.twist.twist.angular.z = w
	pub.publish(Odom)

	last_x = Odom.pose.pose.position.x
	last_y = Odom.pose.pose.position.y
	last_th = Odom.pose.pose.orientation.z
	last_time = now_time



def Set():
	rospy.spin()

if __name__=="__main__":
	try:
		rospy.init_node("Odom")
		rospy.Subscriber("/rpm_data", RPM2_Time, odom)
		pub=rospy.Publisher("/Odometry", Odometry, queue_size=2)
		Odom=Odometry()

		last_x = 0.0
		last_y = 0.2
		last_th = 0.0
		last_time = rospy.Time.now()
		start_Time = last_time
		Set()

	except rospy.ROSInterruptException: pass
