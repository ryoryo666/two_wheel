#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy,rospkg
from nav_msgs.msg import Odometry
from two_wheel.msg import RightLeft_cmd_value
import os

def Recorder(odom_msg):
    x_ref=odom_msg.pose.pose.position.x
    y_ref=odom_msg.pose.pose.position.y
    theta_ref=odom_msg.pose.pose.orientation.z
    v_ref=odom_msg.twist.twist.linear.x
    w_ref=odom_msg.twist.twist.angular.z
    time=odom_msg.header.stamp.secs+(odom_msg.header.stamp.nsecs*(10.0**-9))
    print "Odometry:x={0}   y={1}   θ={2}". format(x_ref, y_ref, theta_ref)

    buf=str(time)+","+str(x_ref)+","+str(y_ref)+","+str(theta_ref)+","+str(v_ref)+","+str(w_ref)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)


def Set():
    Start_check = RightLeft_cmd_value()
    while(1):
        Start_check = rospy.wait_for_message("/New_cmd", RightLeft_cmd_value)
        if Start_check == None:
            continue
        break
        print("Record Start\n")

    rospy.Subscriber("/Odometry", Odometry, Recorder)
    rospy.spin()

if __name__=="__main__":
    try:
        rospy.init_node("Path_Recorder", anonymous=False)
        rospack=rospkg.RosPack()
        df_path=rospack.get_path("two_wheel")
        path=rospy.get_param('~csv_path',df_path+"/csv/RealReferenceTrajectory.csv")
        with open(path, mode="w") as f:
            print("/nNew Path")

        Set()

    except rospy.ROSInterruptException: pass
