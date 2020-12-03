#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from two_wheel.msg import RPM1_Time
import os

path=rospy.get_param('~csv_path')

def callback(msg):
    global value
    value=msg.data
    time=msg.time/1000000

    rospy.loginfo("value: %f  time: %f", value,time)

    buf=str(time)+","+str(value)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)

def listener():
    rospy.init_node("Rotation_Speed_Recorder", anonymous=False)
    rospy.Subscriber("/rpm_data", RPM1_Time, callback)
    rospy.spin()

if __name__=="__main__":
    if  not os.path.isfile(path):
         f=open(path, "w")
         f.close()

    listener()
