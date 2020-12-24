#! /usr/bin/env python
# -*- coding: utf-8 -*-

#   Use one Arduino and two motors ver

import rospy
from two_wheel.msg import RL_RPM
from two_wheel.msg import RightLeft_cmd_value
import os

i=0
def callback(msg):
    global value,path_r,path_l,i,start_Time
    r_value=msg.r_data#*60/(2*3.14)
    l_value=msg.l_data#*60/(2*3.14)

    now_Time = rospy.Time.now()
    t = now_Time - start_Time
    r_time = t.secs + t.nsecs/(10.0**9.0)
    l_time = t.secs + t.nsecs/(10.0**9.0)

    print "Left:{1}[rpm]    Right:{0}[rpm]". format(r_value,l_value)

    buf_r=str(r_time)+","+str(r_value)+"\n"
    buf_l=str(l_time)+","+str(l_value)+"\n"
    with open(path_r, mode="a") as e:
        e.write(buf_r)
    with open(path_l, mode="a") as f:
        f.write(buf_l)

def listener():
    global start_Time
    rospy.Subscriber("/rpm_data", RL_RPM, callback)

    with open(path_r, mode="w"):
        print ""
    with open(path_l, mode="w"):
        print "Record Start"
        
    rospy.spin()

if __name__=="__main__":

    try:
        rospy.init_node("Two_RotationSpeedRecoder", anonymous=False)
        path_r=rospy.get_param('~csv_path_r')
        path_l=rospy.get_param('~csv_path_l')
        start_Time = rospy.Time.now()
        listener()
    except rospy.ROSInterruptException: pass
