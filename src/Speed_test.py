#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from geometry_msgs.msg import Twist
from two_wheel.msg import RightLeft_cmd_value

def pub():
    rospy.init_node("Test_talker")
    pub=rospy.Publisher("New_cmd", RightLeft_cmd_value, queue_size=10)
    ref_v=RightLeft_cmd_value()
    ref_v.r_ref = 10.0
    ref_v.l_ref = 10.0
    r=rospy.Rate(1)

    while not rospy.is_shutdown():
        pub.publish(ref_v)
        r.sleep()

if __name__=="__main__":
    try:
        pub()
    except rospy.ROSInterruptException: pass
