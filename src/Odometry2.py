#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from two_wheel.msg import RL_RPM
from nav_msgs.msg import Odometry

wr = 0.045  	# タイヤ半径 [m]
d  = 0.0615 	# トレッド幅の半分 [m]

#初期位置設定
last_x = 0.0
last_y = 0.0
last_th = 0.0

#初期速度、回転角速度設定
pre_v = 0.0
pre_w = 0.0

def odom(msg):  #データを受信するたび実行
    global last_x, last_y, last_th, last_Time, now_Time, pre_v, pre_w

    #エンコーダより左右のモータ角速度受信・格納
    R_data = msg.r_data
    L_data = msg.l_data
#    print "R:{0}[rad/s]    L:{1}[rad/s]".format(R_data, L_data)
#    print "R:{0}[rpm]    L:{1}[rpm".format(R_data*(30/math.pi), L_data*(30/math.pi))

    now_Time = rospy.Time.now() #ROSを起動してからの現在時刻取得
    dt = now_Time - last_Time   #前回実行時との時間差を計算
    dt = dt.secs + dt.nsecs/10.0**9.0   #時間差の形式変更
    t = now_Time - start_Time   #ノード実行時からの経過時間計算
    Odom.header.stamp.secs = t.secs #配信する時間を格納 単位はsec
    Odom.header.stamp.nsecs = t.nsecs   #配信する時間を格納　単位はnsec
#    print "t:{0}".format(t.secs + t.nsecs/10.0**9.0)
#    print "dt:{0}".format(dt)

    #左右車輪の速度計算
    vr = R_data * wr   
    vl = L_data * wr
#    print "Vr:{0}    vl:{1}".format(vr, vl)

    #ロボットの並進速度・回転角速度計算
    v = (vr+vl)/2.0
    w = (vr-vl)/(2.0*d)
#    print "V:{0}    W:{1}".format(v, w)

    #現在位置を計算　配信するデータをインスタンスに格納
    Odom.pose.pose.position.x = last_x + pre_v * dt * math.cos(Odom.pose.pose.orientation.z)
    Odom.pose.pose.position.y = last_y + pre_v * dt * math.sin(Odom.pose.pose.orientation.z)
    Odom.pose.pose.orientation.z = last_th + pre_w * dt

    #現在速度を計算　配信するデータをインスタンスに格納
    Odom.twist.twist.linear.x = v
    Odom.twist.twist.angular.z = w

#    print "x:" + str(Odom.pose.pose.position.x)
#    print "y:" + str(Odom.pose.pose.position.y)
#    print "θ:" + str(math.degrees(Odom.pose.pose.orientation.z))
#    print "v:{0}".format(Odom.twist.twist.linear.x)
    print ""
    pub.publish(Odom)   #データを配信

    #前回実行時データとして各データを格納
    last_x = Odom.pose.pose.position.x
    last_y = Odom.pose.pose.position.y
    last_th = Odom.pose.pose.orientation.z
    pre_v = v
    pre_w = w
    last_Time = now_Time


if __name__=="__main__":
	try:
		rospy.init_node("Odom") #ノード名定義
		rospy.Subscriber("/Encoder_data", RL_RPM, odom) #購読するトピック名、データ型、購読時実行関数定義
		pub=rospy.Publisher("/Odometry", Odometry, queue_size=3)    #配信するトピック名、データ型、バッファサイズ定義
		Odom=Odometry() #Odometry形式のインスタンス生成

		start_Time = rospy.Time.now()   #ノード実行時の時間取得
		last_Time = start_Time

		rospy.spin()

	except rospy.ROSInterruptException: pass
