#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import readchar as rc
from geometry_msgs.msg import Twist
from two_wheel.msg import curve_data

V=0.4
R=0    #default

def callback(data):
    if data.Radius==0:
	twist.angular.z=0
    elif data.Direction=="r":
	twist.angular.z=V/data.Radius
    elif data.Direction=="l":
	twist.angular.z=(-1)*(V/data.Radius)

def pub():
    rospy.init_node("robot_twist_pub",anonymous=True)
    rospy.Subscriber("Turning_info", curve_data, callback)
    pub=rospy.Publisher("/robo_gazebo/diff_drive_controller/cmd_vel", Twist, queue_size=10)
    r=rospy.Rate(10)

    twist.linear.x=V
    twist.angular.z=0

    EOF="q"

    print("Reading from keyboard")
    print("-----------------------------")
    print("Use arrow keys tomove the robot. (↑ or ↓)")

    while not rospy.is_shutdown():
	c=rc.readchar()
	if c==EOF :
		break ;
	print("ok")
#	if :
#		V*=(-1)
        pub.publish(twist)
        r.sleep()

if __name__=="__main__":
    twist=Twist()
    try:
        pub()
    except rospy.ROSInterruptException: pass
