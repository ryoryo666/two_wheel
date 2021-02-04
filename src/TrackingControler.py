#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Kanayama Control Method

import math
import rospy
import rospkg
import numpy as np
import glob,os
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

#パラメータ設定
kx = 0.5
ky = 10.0
kth = 5.0

num = 0	#参照軌道インデックス初期化
new_twist=Twist()	#Twist型にインスタンス生成

def New_cmd(odom_msg):
	global num,stop
	#現在位置取得・格納
	x_p=odom_msg.pose.pose.position.x
	y_p=odom_msg.pose.pose.position.y
	theta_p=odom_msg.pose.pose.orientation.z

	shutdown()	#参照軌道データすべて参照時ノード終了

	print "Reference"
	print "x:{0}	y:{1}".format(Reference_Trajectory[num][1],Reference_Trajectory[num][2])

	#参照軌道上の目標点取得
	x_r=Reference_Trajectory[num][1]
	y_r=Reference_Trajectory[num][2]
	theta_r=Reference_Trajectory[num][3]
	v_r=Reference_Trajectory[num][4]
	w_r=Reference_Trajectory[num][5]
	num += 1	#次の参照軌道上の目標点へ

	#位置誤差計算
	x_err = (x_r-x_p)*math.cos(theta_p)+(y_r-y_p)*math.sin(theta_p)
	y_err = -(x_r-x_p)*math.sin(theta_p)+(y_r-y_p)*math.cos(theta_p)
	theta_err = theta_r-theta_p

	#新たな速度指令の生成、インスタンスへ格納、配信
	new_twist.linear.x  = v_r*math.cos(theta_err)+kx*x_err
	new_twist.angular.z = w_r+v_r*(ky*y_err+kth*math.sin(theta_err))
	pub.publish(new_twist)

def Set():
	rospy.Subscriber("/Odometry", Odometry, New_cmd)	#購読するトピック名、データ型、購読時実行関数定義
	rospy.spin()

def shutdown():
	global num,stop
	if num >= stop:
			print "\nFinish\n"
			new_twist.linear.x  = 0.0
			new_twist.angular.z = 0.0
			pub.publish(new_twist)
			rospy.signal_shutdown("Finish")

if __name__=="__main__":
    try:
		rospy.init_node("Kanayama_Method_Controller", disable_signals=True, anonymous=True)	#ノード名定義
		pub=rospy.Publisher("/cmd_vel", Twist, queue_size=2)	#配信するトピック名、データ型、バッファサイズ定義
		
		rospack=rospkg.RosPack()	#rospackを使用するためのインスタンス生成
		pack=rospack.get_path("two_wheel")	#パッケージtwo_wheelの絶対パス取得
		file_list=glob.glob(os.path.join(pack+"/csv", "Reference*"))	#参照軌道ファイルリスト取得
		file_list.sort()

		#参照軌道選択
		print "\nSelect Reference Trajectory\n"
		for i in range(len(file_list)):
			print str(i)+":"+file_list[i].replace(pack+"/csv/", "")
		number=int(raw_input("\nFileNumber>> "))
		Reference_Trajectory=np.loadtxt(file_list[number], delimiter = ",")
		stop=len(Reference_Trajectory)	#参照軌道上の目標点数取得

		Set()

    except rospy.ROSInterruptException: pass
