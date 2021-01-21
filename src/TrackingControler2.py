#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy
import rospkg
import numpy as np
import glob,os
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

# Parameter
kx1 = 0.25  # P gain
ky1 = 0.25
kx2 = 0.05  # D gain
ky2 = 0.05
v_max = 0.06
w_max = 0.21

qe = 0.02
uv = 0.0
uw = 0.0

num = 0
i = 1
new_twist=Twist()

def New_cmd(odom_msg):
    global num, stop, pre_Time
    global v_max, w_max, uv, uw, qe, i
	# Now Pose
    x_p = odom_msg.pose.pose.position.x
    y_p = odom_msg.pose.pose.position.y
    theta_p = odom_msg.pose.pose.orientation.z
    v_p = odom_msg.twist.twist.linear.x
    if i ==1:
        v_p = qe
        i = 0
#    print "Xp:{0}    Yp:{1}".format(x_p,y_p)

#    while (num < stop):
#		x_diff=Reference_Trajectory[num][1]-x_p
#		y_diff=Reference_Trajectory[num][2]-y_p
#		diff = math.sqrt((x_diff**2)+(y_diff**2))
#		if 0.15< diff:
#			break
#		num+=1
    shutdown()

	# Reference point on Reference Trajectory
    x_r = Reference_Trajectory[num][1]
    y_r = Reference_Trajectory[num][2]
    vx_r = Reference_Trajectory[num][3]
    vy_r = Reference_Trajectory[num][4]
    ax_r = Reference_Trajectory[num][5]
    ay_r = Reference_Trajectory[num][6]
#    print "Xr:{0}    Yr:{1}".format(x_r,y_r)
    num += 1

	# Error value
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

	# New Command Value
    new_twist.linear.x  = Vc
    new_twist.angular.z = Wc
    pub.publish(new_twist)

def Set():
    rospy.Subscriber("/Odometry", Odometry, New_cmd)
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
        rospy.init_node("Kanayama_Method_Controller", disable_signals=True, anonymous=True)
        pub=rospy.Publisher("/cmd_vel", Twist, queue_size=2)
        
        rospack=rospkg.RosPack()
        pack=rospack.get_path("two_wheel")
        file_list=glob.glob(os.path.join(pack+"/csv", "Reference*"))
        file_list.sort()
        print "\nSelect Reference Trajectory\n"
        for i in range(len(file_list)):
        	print str(i)+":"+file_list[i].replace(pack+"/csv/", "")
        number=int(raw_input("\nFileNumber>> "))
        Reference_Trajectory=np.loadtxt(file_list[number], delimiter = ",")
        stop=len(Reference_Trajectory)

        Set()

    except rospy.ROSInterruptException: pass
