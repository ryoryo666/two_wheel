#! /usr/bin/env python
# -*- coding: utf-8 -*-

#   Dynamic feedback linearization

import math
import rospy
import rospkg
import numpy as np
import glob,os
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

#パラメーター設定
kx1 = 0.25  # P gain
ky1 = 0.25
kx2 = 0.05  # D gain
ky2 = 0.05

#速度制限設定
v_max = 0.06
w_max = 0.21

qe = 0.02
uv = 0.0
uw = 0.0

#参照軌道インデックス
num = 0
i = 1
new_twist=Twist()   #Twist型のインスタンス生成

def New_cmd(odom_msg):
    global num, stop, pre_Time
    global v_max, w_max, uv, uw, qe, i

	#現在位置、速度取得
    x_p = odom_msg.pose.pose.position.x
    y_p = odom_msg.pose.pose.position.y
    theta_p = odom_msg.pose.pose.orientation.z
    v_p = odom_msg.twist.twist.linear.x
    if i ==1:
        v_p = qe
        i = 0
#    print "Xp:{0}    Yp:{1}".format(x_p,y_p)

    shutdown()  #参照軌道データすべて参照時ノード終了

	#参照軌道データ取得
    x_r = Reference_Trajectory[num][1]
    y_r = Reference_Trajectory[num][2]
    vx_r = Reference_Trajectory[num][3]
    vy_r = Reference_Trajectory[num][4]
    ax_r = Reference_Trajectory[num][5]
    ay_r = Reference_Trajectory[num][6]
#    print "Xr:{0}    Yr:{1}".format(x_r,y_r)
    num += 1    #次の参照軌道上の目標点へ

	#位置・速度誤差計算
    x_err = x_r - x_p
    y_err = y_r - y_p
    vx_err = vx_r - (v_p*math.cos(theta_p))
    vy_err = vy_r - (v_p*math.sin(theta_p))
#    print "Xerr:{0}    Yerr:{1}".format(x_err,y_err)
#    print "Vxerr:{0}    Vyerr:{1}".format(vx_err,vy_err)

    ux = ax_r + kx1*vx_err + kx2*x_err
    uy = ay_r + ky1*vy_err + ky2*y_err

    qe += ux*math.cos(theta_p) + uy*math.sin(theta_p)
    uv = qe
    uw = ( uy*math.cos(theta_p) - ux*math.sin(theta_p) ) / uv
    print "uv:{0}    uw:{0}".format(uv, uw)

    #速度制限のための処理
    z = max([abs(uv)/v_max, abs(uw)/w_max, 1.0])
    if z == 1.0:
        Vc = uv
        Wc = uw
    elif z == abs(uv)/v_max:
        Vc = np.sign(uv) * v_max
        Wc = uw / z
    else:
        Vc = uv / z
        Wc = np.sign(uw) * w_max
    print "V:{0}    W:{0}".format(Vc, Wc)

	#新たな速度指令値格納・配信
    new_twist.linear.x  = Vc
    new_twist.angular.z = Wc
    pub.publish(new_twist)

def Set():
    rospy.Subscriber("/Odometry", Odometry, New_cmd)    #購読するトピック名、データ型、購読時実行関数定義
    rospy.spin()

def shutdown(): #参照軌道データすべて参照時ノードシャットダウン
	global num,stop
	if num >= stop:
			print "\nFinish\n"
			new_twist.linear.x  = 0.0
			new_twist.angular.z = 0.0
			pub.publish(new_twist)
			rospy.signal_shutdown("Finish")

if __name__=="__main__":
    try:
        rospy.init_node("Kanayama_Method_Controller", disable_signals=True, anonymous=True) #ノード名定義
        pub=rospy.Publisher("/cmd_vel", Twist, queue_size=2)     #配信するトピック名、データ型、バッファサイズ定義
        
        rospack=rospkg.RosPack()    #rospackを使用するためのインスタンス生成
        pack=rospack.get_path("two_wheel")  #パッケージtwo_wheelの絶対パス取得
        file_list=glob.glob(os.path.join(pack+"/csv", "Reference*"))    #参照軌道ファイルリスト取得
        file_list.sort()

        #参照軌道選択
        print "\nSelect Reference Trajectory\n"
        for i in range(len(file_list)):
        	print str(i)+":"+file_list[i].replace(pack+"/csv/", "")
        number=int(raw_input("\nFileNumber>> "))
        Reference_Trajectory=np.loadtxt(file_list[number], delimiter = ",")
        stop=len(Reference_Trajectory)  #参照軌道上の目標点数取得

        Set()

    except rospy.ROSInterruptException: pass
