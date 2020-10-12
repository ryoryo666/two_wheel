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

    buf=str(r_time)+","+str(r_value)+"\n"
    with open(r_path, mode="a") as f:
        f.write(buf)

def listener():
    rospy.init_node("PID_getter_", anonymous=False)
    rospy.Subscriber("/rpm_data", PID, callback)
    r_path=rospy.get_param('~csv_path')

    if  not os.path.isfile(path):
        f=open(path, "a")
#         buf=str(0.0)+","+str(0.0)+"\n"
#         with open(path, mode="a") as f:
#             f.write(buf)
        f.close()

    rospy.spin()

if __name__=="__main__":
    try:
        listener()
    except rospy.ROSInterruptException: pass
