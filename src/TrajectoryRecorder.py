#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from nav_msgs.msg import Odometry
from two_wheel.msg import target_curve
import os
import Quat_Euler

def Recorder(odom_msg):
    global time
    x_ref=odom_msg.pose.pose.position.x
    y_ref=odom_msg.pose.pose.position.y
    q=Quat_Euler.Quat_TF(0,0, odom_msg.pose.pose.orientation.z, odom_msg.pose.pose.orientation.w)
    theta_ref=q.Euler_z()
    v_ref=odom_msg.twist.twist.linear.x
    w_ref=odom_msg.twist.twist.angular.z
    time=odom_msg.header.stamp.secs+(odom_msg.header.stamp.nsecs*(10**-9))
    print "Odometry:x={0}   y={1}   θ={2}". format(x_ref, y_ref, theta_ref)

    buf=str(time)+","+str(x_ref)+","+str(y_ref)+","+str(theta_ref)+","+str(v_ref)+","+str(w_ref)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)
    time+=0.01

def Set():
    Start_check = target_curve()
    while(1):
        Start_check = rospy.wait_for_message("/target_update", target_curve)
        if not Start_check:
            continue
        break
        print("Record Start")

    rospy.Subscriber("/Odometry", Odometry, Recorder)
    rospy.spin()

if __name__=="__main__":
    try:
        rospy.init_node("Trajectory_Recorder", anonymous=False)
        path=rospy.get_param('~csv_path','/home/ubuntu/catkin_ws/src/gazebo_sim/csv/TargetTrajectory.csv')
        time=0.0
#        print(os.getcwd())
        with open(path, mode="w") as f:
            print("New Trajectory")
        Set()

    except rospy.ROSInterruptException: pass
