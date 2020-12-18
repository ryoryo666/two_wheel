#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from geometry_msgs.msg import Twist
from two_wheel.msg import target_curve

def pub():
    rospy.init_node("Test_talker")
    pub=rospy.Publisher("target_update", target_curve, queue_size=10)
    target=target_curve()
    target.r_target = 10.0
    target.l_target = 10.0
    r=rospy.Rate(1)

    while not rospy.is_shutdown():
        pub.publish(target)
        r.sleep()

if __name__=="__main__":
    try:
        pub()
    except rospy.ROSInterruptException: pass
