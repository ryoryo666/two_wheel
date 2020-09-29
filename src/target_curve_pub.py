#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
import matplotlib.pyplot as plt
from two_wheel.msg import target_curve

def Target_Pub():
    rospy.init_node("Target_Curve_Publisher", anonymous=True)
    pub=rospy.Publisher("Target_data", target_curve, queue_size=10)
    r=rospy.Rate(5)

    target_list=[]
    step=10
    last_target=0.0
    data=target_curve()

    while not rospy.is_shutdown():
	target=float(raw_input("Target >>"))
	if target==000:
	    print("Stop")
	    break;

	if(target > last_target):
            for i in range(step):
		n=float(i+1.0)/step
    	        target_list.append(target*math.sin(n*(math.pi/2))+last_target)
		data.r_target=target_list[i]
		pub.publish(data)
		r.sleep()

	if(target < last_target):
            for i in range(step):
		n=float(i+1.0)/step
    	        target_list.append((-1)*target*math.sin(n*(math.pi/2))+last_target)
		data.r_target=target_list[i]
		pub.publish(data)
		r.sleep()

    	print(target_list)
# Curve check
#	t=range(step)
#	plt.scatter(t, target_list)
#	plt.grid()
#	plt.show()
	last_target=target
	del target_list[:]

if __name__=="__main__":
    try:
	Target_Pub()
    except rospy.ROSInterruptException: pass
