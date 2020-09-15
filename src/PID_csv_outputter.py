#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from two_wheel.msg import PID
import os

path=rospy.get_param("/PID_output_plotter/csv_path")

def callback(msg):
    global value
    value=msg.data
    time=msg.time/1000000

    rospy.loginfo("value: %f  time: %f", value,time)

    buf=str(time)+","+str(value)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)

def listener():
    rospy.init_node("PID_getter_right", anonymous=False)
    rospy.Subscriber("/rpm_data", PID, callback)
    rospy.spin()

if __name__=="__main__":
    if  not os.path.isfile(path):
         f=open(path, "a")
#         buf=str(0.0)+","+str(0.0)+"\n"
#         with open(path, mode="a") as f:
#             f.write(buf)
         f.close()

    listener()
