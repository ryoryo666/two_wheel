#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import readchar as rc
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from two_wheel.msg import curve_data

#default
V=10*1000/3600   #[m/s]
W=0.0

def callback(data):
    global V,W
    if data.Radius==0:
        W=0.0
    elif data.Direction=="r":
        W=V/data.Radius
    elif data.Direction=="l":
        W=(-1)*(V/data.Radius)

def callback2(joy):
    global V,W
    if joy.axes[1] > 0.2:
        twist.linear.x=V
        twist.angular.z=W
    elif joy.axes[1] < -0.2:
        twist.linear.x=V*(-1)
        twist.angular.z=W*(-1)
    else:
        twist.linear.x=0.0
        twist.angular.z=0


def set():
    rospy.init_node("joy_to_twist",anonymous=True)
    rospy.Subscriber("Turning_info", curve_data, callback)
    rospy.Subscriber("/joy", Joy, callback2)
    pub=rospy.Publisher("/robot_gazebo/diff_drive_controller/cmd_vel", Twist, queue_size=10)
    r=rospy.Rate(10)

    twist.linear.x=0
    twist.angular.z=0

    while not rospy.is_shutdown():
            pub.publish(twist)
            r.sleep()

if __name__=="__main__":
    twist=Twist()
    try:
        set()
    except rospy.ROSInterruptException: pass
