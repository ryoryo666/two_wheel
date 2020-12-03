#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from two_wheel.msg import target_curve

def Target_Pub():
    rospy.init_node("TargetSpeedCurve_Publisher", anonymous=True)
    pub=rospy.Publisher("target_update", target_curve, queue_size=10)
    r=rospy.Rate(75)

    step=100
    r_last_target=0.0
    l_last_target=0.0
    data=target_curve()

    Wr=0.08	#wheel radius
    Bs=1.0	#Base supeed
    Ws=0.08	#Wheel separation

    while not rospy.is_shutdown():
        r_target=raw_input("Target_R(Stop:q) >>")
	l_target=raw_input("Target_L(Stop:q) >>")
        if r_target=="q" or l_target=="q":
            data.r_target=0.0
            data.l_target=0.0
            pub.publish(data)
            print("Stop")
            break;

        r_target=float(r_target)
	l_target=float(l_target)
	if r_last_target > r_target and r_target!=0.0:
     	   for i in range(step):
		    n=float(i+1.0)/step
		    data.r_target=(r_target-r_last_target)*math.sin(n*(math.pi/2))+r_last_target
		    data.l_target=(l_target-l_last_target)*math.sin(n*(math.pi/2))+l_last_target
		    pub.publish(data)
		    print "R:{0}	L:{1}". format(data.r_target,data.l_target)
		    r.sleep()
	else :
	   data.r_target=r_target
           data.l_target=l_target
	   pub.publish(data)

        r_last_target=r_target
	l_last_target=l_target

if __name__=="__main__":
    try:
        Target_Pub()
    except rospy.ROSInterruptException: pass
