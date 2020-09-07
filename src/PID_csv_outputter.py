#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from two_wheel.msg import PID
import os

path="/home/ryo/catkin_ws/src/two_wheel/csv/data.csv"
count=0

def callback(msg):
    global count
    global value
    value=msg.data
    time=msg.time/1000000

    rospy.loginfo("value: %f  time: %f", value,time)

    buf=str(time)+","+str(value)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)
    count+=1

def listener():
    rospy.init_node("PID_getter", anonymous=False)
    rospy.Subscriber("/Volume", PID, callback)
    rospy.spin()

if __name__=="__main__":
    if  not os.path.isfile(path):
         f=open(path, "a")
         buf=str(0.0)+","+str(0.0)+"\n"
         with open(path, mode="a") as f:
             f.write(buf)
         count+=1
         f.close()

    listener()
