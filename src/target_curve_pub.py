#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math

from two_wheel.msg import target_curve

def Target_Pub():
    rospy.init_node("Target_Curve_Publisher", anonymous=True)
    pub=rospy.Publisher("target_update", target_curve, queue_size=10)
    r=rospy.Rate(2)

    target_list=[]
    step=10
    last_target=0.0
    data=target_curve()

    Wr=0.08	#wheel radius
    Bs=1.0	#Base supeed
    Ws=0.08	#Wheel separation

    while not rospy.is_shutdown():
	target=float(raw_input("Target(Stop:000) >>"))
	if target==000:
	    print("Stop")
	    break;


	for i in range(step):
		n=float(i+1.0)/step
		data.r_target=(target-last_target)*math.sin(n*(math.pi/2))+last_target
		data.l_target=data.r_target
		pub.publish(data)
		print(data)
		r.sleep()


	last_target=target
	del target_list[:]

if __name__=="__main__":
    try:
	Target_Pub()
    except rospy.ROSInterruptException: pass
