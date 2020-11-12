#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from two_wheel.msg import PID
import os

def callback(msg):
    global value,path
    r_value=msg.r_data*60/(2*3.14)
    l_value=msg.l_data*60/(2*3.14)
    r_time=msg.r_time/10**6
    l_time=msg.l_time/10**6

    print "Right:{0}[rpm]    Left:{1}". format(r_value,l_value)

    buf_r=str(r_time)+","+str(r_value)+"\n"
    buf_l=str(l_time)+","+str(l_value)+"\n"
    with open(path_r, mode="a") as e:
        e.write(buf_r)
    with open(path_l, mode="a") as f:
        f.write(buf_l)

def listener():
    rospy.init_node("PID_getter_", anonymous=False)
    rospy.Subscriber("/rpm_data", PID, callback)

    path_r=rospy.get_param('~csv_path_r')
    path_l=rospy.get_param('~csv_path_l')
    with open(path_r, mode="w")
    with open(path_l, mode="w")

    rospy.spin()

if __name__=="__main__":
    try:
        listener()
    except rospy.ROSInterruptException: pass
