#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy,rospkg
from nav_msgs.msg import Odometry
from two_wheel.msg import RightLeft_cmd_value
import os

def Recorder(odom_msg):
    #現在位置・速度・時間取得
    x_ref=odom_msg.pose.pose.position.x
    y_ref=odom_msg.pose.pose.position.y
    theta_ref=odom_msg.pose.pose.orientation.z
    v_ref=odom_msg.twist.twist.linear.x
    w_ref=odom_msg.twist.twist.angular.z
    time=odom_msg.header.stamp.secs+(odom_msg.header.stamp.nsecs*(10.0**-9))
    print "Odometry:x={0}   y={1}   θ={2}". format(x_ref, y_ref, theta_ref)

    #現在位置・速度・時間記録
    buf=str(time)+","+str(x_ref)+","+str(y_ref)+","+str(theta_ref)+","+str(v_ref)+","+str(w_ref)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)


def Set():
    Start_check = RightLeft_cmd_value()
    #速度指令配信確認時記録開始
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
        rospy.init_node("Path_Recorder", anonymous=False)　#ノード目定義
        rospack=rospkg.RosPack()
        df_path=rospack.get_path("two_wheel")   #パッケージtwo_wheelの絶対パス取得
        
        #記録データ保存先パス・ファイル名設定
        #パラメータから取得　or パラメータから取得しなかった場合のデフォルト
        path=rospy.get_param('~csv_path',df_path+"/csv/RealReferenceTrajectory.csv")
        with open(path, mode="w") as f:
            print("/nNew Reference Trajectory")

        Set()

    except rospy.ROSInterruptException: pass
