#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float32
import os

path="/home/students/catkin_ws/src/two_wheel/csv/plot_data.csv"
count=0

def callback(msg):
    global count
    global value
    value=msg.data
    rospy.loginfo("value: %f", value)

    buf=str(count)+"."+str(value)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)
    count+=1

def listener():
    rospy.init_node("PID_getter", anonymous=False)
    rospy.Subscriber("/Volume", Float32, callback)
    rospy.spin()

if __name__=="__main__":
    if  not os.path.isfile(path):
         f=open(path, "a")
         f.close()

    listener()
