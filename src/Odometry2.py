#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from two_wheel.msg import RL_RPM
from nav_msgs.msg import Odometry

wr = 0.045  	# Wheel Radius [m]
d  = 0.0615 	# Wheel-Center distance [m]

#Initial Position
last_x = 0.0
last_y = 0.0
last_th = 0.0

pre_v = 0.0
pre_w = 0.0

def odom(msg):
    global last_x, last_y, last_th, last_Time, now_Time, pre_v, pre_w
    R_data = msg.r_data
    L_data = msg.l_data
#    print "R:{0}[rad/s]    L:{1}[rad/s]".format(R_data, L_data)
#    print "R:{0}[rpm]    L:{1}[rpm".format(R_data*(30/math.pi), L_data*(30/math.pi))

    now_Time = rospy.Time.now()
    dt = now_Time - last_Time
    dt = dt.secs + dt.nsecs/10.0**9.0
    t = now_Time - start_Time
    Odom.header.stamp.secs = t.secs
    Odom.header.stamp.nsecs = t.nsecs
#    print "t:{0}".format(t.secs + t.nsecs/10.0**9.0)
#    print "dt:{0}".format(dt)

    vr = R_data * wr
    vl = L_data * wr
#    print "Vr:{0}    vl:{1}".format(vr, vl)
    v  = (vr+vl)/2.0
    w = (vr-vl)/(2.0*d)
#    print "V:{0}    W:{1}".format(v, w)

    Odom.pose.pose.position.x = last_x + pre_v * dt * math.cos(Odom.pose.pose.orientation.z)
    Odom.pose.pose.position.y = last_y + pre_v * dt * math.sin(Odom.pose.pose.orientation.z)
    Odom.pose.pose.orientation.z = last_th + pre_w * dt

    Odom.twist.twist.linear.x = v
    Odom.twist.twist.angular.z = w

    print "x:" + str(Odom.pose.pose.position.x)
    print "y:" + str(Odom.pose.pose.position.y)
    print "θ:" + str(math.degrees(Odom.pose.pose.orientation.z))
#    print "v:{0}".format(Odom.twist.twist.linear.x)
    print ""
    pub.publish(Odom)

    last_x = Odom.pose.pose.position.x
    last_y = Odom.pose.pose.position.y
    last_th = Odom.pose.pose.orientation.z
    pre_v = v
    pre_w = w
    last_Time = now_Time

#def set():


if __name__=="__main__":
	try:
		rospy.init_node("Odom")
		rospy.Subscriber("/Encoder_data", RL_RPM, odom)
		pub=rospy.Publisher("/Odometry", Odometry, queue_size=3)
		Odom=Odometry()

		start_Time = rospy.Time.now()
		last_Time = start_Time

		rospy.spin()

	except rospy.ROSInterruptException: pass
