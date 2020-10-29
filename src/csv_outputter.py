#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from two_wheel.msg import PID
import os

def callback(msg):
    global value,path
    r_value=msg.r_data
    r_time=msg.r_time/1000000
    l_value=msg.l_data
    l_time=msg.l_time/1000000

    rospy.loginfo("value: %f  time: %f", r_value,r_time)

    buf=str(r_time)+","+str(r_value)+","+str(l_time)+","+str(l_value)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)

def listener():
    rospy.Subscriber("/rpm_data", PID, callback)

    with open(path, mode="w") as f:
        print("New\n")

    rospy.spin()

if __name__=="__main__":
    try:
        rospy.init_node("PID_getter_", anonymous=False)
        path=rospy.get_param('~csv_path')
        listener()
    except rospy.ROSInterruptException: pass
