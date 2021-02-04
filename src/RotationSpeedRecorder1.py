#! /usr/bin/env python
# -*- coding: utf-8 -*-

#モーターが1つの場合の回転角速度 or 回転数の記録

import rospy
from two_wheel.msg import RPM1_Time
import os


def callback(msg):
    global value,path
    value=msg.data  #角速度　or 回転数受信・格納
    time=msg.time/1000000   #時間受信・格納

    rospy.loginfo("value: %f  time: %f", value,time)    #受信データ画面出力

    #受信データ記録
    buf=str(time)+","+str(value)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)

def listener():
    with open(path, mode="w"):
        print "Record Start"
    rospy.Subscriber("/Encoder_data", RPM1_Time, callback)  #購読するトピック名、データ型、購読時実行関数定義
    rospy.spin()

if __name__=="__main__":
    try:
        rospy.init_node("Rotation_Speed_Recorder", anonymous=False) #ノード名定義

        #記録データ保存先パス・ファイル名設定
        #パラメータから取得　or パラメータから取得しなかった場合のデフォルト
        path=rospy.get_param('~csv_path')
        listener()
    except rospy.ROSInterruptException: pass
