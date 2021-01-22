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
    ref_v.r_ref = 1.0   #[rad/s]
    ref_v.l_ref = 1.0   #[rad/s]
    r = rospy.Rate(1)
    i = 0
    s = 0
    
    while s > 4():
        pub.publish(ref_v)
        r.sleep()
        if i ==4:
                ref_v.r_ref = 0.0
                ref_v.l_ref = 0.0
        i+=1
        s += 1

if __name__=="__main__":
    try:
        pub()
    except rospy.ROSInterruptException: pass
