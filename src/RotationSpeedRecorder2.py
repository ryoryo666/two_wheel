#! /usr/bin/env python
# -*- coding: utf-8 -*-

#   Use one Arduino and two motors ver

import rospy
from two_wheel.msg import RPM2_Time
import os

i=0
def callback(msg):
    global value,path_r,path_l,i
    r_value=msg.r_data#*60/(2*3.14)
    l_value=msg.l_data#*60/(2*3.14)
    r_value=round(r_value,1)
    l_value=round(l_value,1)
    r_time=msg.time
    l_time=msg.time

    print "Left:{1}[rpm]    Right:{0}[rpm]". format(r_value,l_value)

    buf_r=str(r_time)+","+str(r_value)+"\n"
    buf_l=str(l_time)+","+str(l_value)+"\n"
    with open(path_r, mode="a") as e:
        e.write(buf_r)
    with open(path_l, mode="a") as f:
        f.write(buf_l)

def listener():
    rospy.Subscriber("/rpm_data", RPM2_Time, callback)

    with open(path_r, mode="w"):
        print "Record Start"
    with open(path_l, mode="w"):
        print ""

    rospy.spin()

if __name__=="__main__":

    try:
        rospy.init_node("Two_RotationSpeedRecoder", anonymous=False)
        path_r=rospy.get_param('~csv_path_r')
        path_l=rospy.get_param('~csv_path_l')
        listener()
    except rospy.ROSInterruptException: pass
