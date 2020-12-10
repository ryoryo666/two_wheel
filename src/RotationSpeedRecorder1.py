#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from two_wheel.msg import RPM1_Time
import os


def callback(msg):
    global value,path
    value=msg.data
    time=msg.time/1000000

    rospy.loginfo("value: %f  time: %f", value,time)

    buf=str(time)+","+str(value)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)

def listener():
    path=rospy.get_param('~csv_path')
    with open(path, mode="w"):
        print "Record Start"
    rospy.Subscriber("/rpm_data", RPM1_Time, callback)
    rospy.spin()

if __name__=="__main__":
    try:
        rospy.init_node("Rotation_Speed_Recorder", anonymous=False)
        path=rospy.get_param('~csv_path')
        listener()
    except rospy.ROSInterruptException: pass
