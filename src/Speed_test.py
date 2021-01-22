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
    ref_v.r_ref = 1.0
    ref_v.l_ref = 1.0
    r=rospy.Rate(1)
    i=0

    start = raw_input("何か入力でスタート >> ")

    if start != None:
        while not rospy.is_shutdown():
            pub.publish(ref_v)
            r.sleep()
            i+=1
            if i ==5:
                ref_v.r_ref = 0.0
                ref_v.l_ref = 0.0

if __name__=="__main__":
    try:
        pub()
    except rospy.ROSInterruptException: pass
