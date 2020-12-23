#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from two_wheel.msg import RL_RPM
from nav_msgs.msg import Odometry

wr = 0.03825	# Wheel Radius [m]
d  = 0.0615 	# Wheel-Center distance [m]

last_x = 0.0
last_y = 0.0
last_th = 0.0

def odom(event):
    global last_x,last_y,last_th,last_Time,now_Time
    msg = rospy.wait_for_message("/rpm_data", RL_RPM)

    R_data = msg.r_data
    L_data = msg.l_data

    now_Time = rospy.Time.now()
    dt = now_Time - last_Time
    dt = dt.secs + dt.nsecs/10.0**9.0
    t = now_Time - start_Time
    Odom.header.stamp.secs = t.secs
    Odom.header.stamp.nsecs = t.nsecs

    vr = round(R_data,6)*((2*math.pi)/60.0) * wr
    vl = round(L_data,6)*((2*math.pi)/60.0) * wr
    v  = (vr+vl)/2.0
    w = (vr-vl)/(2.0*d)

    Odom.pose.pose.position.x = last_x + v * dt * math.cos(Odom.pose.pose.orientation.z)
    Odom.pose.pose.position.y = last_y + v * dt * math.sin(Odom.pose.pose.orientation.z)
    Odom.pose.pose.orientation.z = last_th + w * dt

    Odom.twist.twist.linear.x = v
    Odom.twist.twist.angular.z = w

    print "x:{0}    y:{1}   V:{2}".format(round(Odom.pose.pose.position.x,2), round(Odom.pose.pose.position.y,2), round(v,2))
    pub.publish(Odom)

    last_x = Odom.pose.pose.position.x
    last_y = Odom.pose.pose.position.y
    last_th = Odom.pose.pose.orientation.z
    last_Time = now_Time

if __name__=="__main__":
	try:
		rospy.init_node("Odom")
		pub=rospy.Publisher("/Odometry", Odometry, queue_size=2)
		Odom=Odometry()

		start_Time = 0.0

		rospy.Timer(rospy.Duration(0.1), odom)

	except rospy.ROSInterruptException: pass
