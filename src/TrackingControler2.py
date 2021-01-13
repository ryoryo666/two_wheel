#! /usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy
import rospkg
import numpy as np
import glob,os
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

#Euler
kx1 = 0.1
kx2 = 0.1
ky1 = 0.1
ky2 = 0.1


num = 1
new_twist=Twist()

def New_cmd(odom_msg):
    global num, stop, pre_Time
	# Now Pose
    x_p = odom_msg.pose.pose.position.x
    y_p = odom_msg.pose.pose.position.y
    theta_p = odom_msg.pose.pose.orientation.z
    v_p = odom_msg.twist.twist.linear.x

    now_Time = rospy.Time.now()
    dt = now_Time - pre_Time
    dt = dt.secs + dt.nsecs/(10.0**9.0)

#	while (num < stop):
#		x_diff=Reference_Path[num][1]-x_p
#		y_diff=Reference_Path[num][2]-y_p
#		diff = math.sqrt((x_diff**2)+(y_diff**2))
#		if 0.1 < diff:
#			print "\nUpdate"
#			break
#		num+=1
    num += 1
    shutdown()

	# Reference point on Reference Path
    x_r = Reference_Path[num][1]
    y_r = Reference_Path[num][2]
    vx_r = Reference_Path[num][3]
    vy_r = Reference_Path[num][4]

	# Error value
    x_err = x_r - x_p
    y_err = y_r - y_p

    vx_err = vx_r - (v_p*math.cos(theta_p))
    vy_err = vy_r - (v_p*math.sin(theta_p))

    ax_r = (vx_r - pre_vx_r) / dt
    ay_r = (vy_r - pre_vy_r) / dt

    ux = ax_r + kx1*vx_err + kx2*x_err
    uy = ay_r + ky1*vy_err + ky2*y_err

    uv += ux*math.cos(theta_p) + uy*math.sin(theta_p)
    uw = (uy*math.cos(theta_p) - ux*math.sin(theta_p)) / uv

	# New Command Value
    new_twist.linear.x  = uv
    new_twist.angular.z = uw
    pub.publish(new_twist)

    pre_vx_r = x_r - pre_x_r
    pre_vy_r = y_r - pre_y_r
    pre_Time = now_Time

def Set():
    rospy.Subscriber("/Odometry", Odometry, New_cmd)
    pre_Time = rospy.Time.now()
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
		rospack=rospkg.RosPack()
		pack=rospack.get_path("two_wheel")
		file_list=glob.glob(os.path.join(pack+"/csv", "Reference*"))
		file_list.sort()
		print "\nSelect Reference Trajectory\n"
		for i in range(len(file_list)):
			print str(i)+":"+file_list[i].replace(pack+"/csv/", "")
		number=int(raw_input("\nFileNumber>> "))
		Reference_Path=np.loadtxt(file_list[number], delimiter = ",")
		stop=len(Reference_Path)

		pub=rospy.Publisher("/cmd_vel", Twist, queue_size=2)
		Set()

    except rospy.ROSInterruptException: pass
