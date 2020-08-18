#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from two_wheel.msg import curve_data

V=0.4
R=0    #default

def callback(data):
    if data.

def pub():
    rospy.init_node("robot_twist_pub",anonymous=True)
    rospy.Subscriber("Turning_info", curve_data, callback)
    pub=rospy.Publisher("/robo_gazebo/diff_drive_controller/cmd_vel", Twist, queue_size=10)
    r=rospy.Rate(10)

    twist=Twist()
    twist.linear.x=V
    twist.angular.z=0

    while not rospy.is_shutdown():
        pub.publish(twist)
        r.sleep()

if __name__=="__main__":
    try:
        pub()
    except rospy.ROSInterruptException: pass
