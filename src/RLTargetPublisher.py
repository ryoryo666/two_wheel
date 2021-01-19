#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from geometry_msgs.msg import Twist
from two_wheel.msg import RightLeft_cmd_value

Rw = 0.045   # Wheel Radius [m]
T  = 0.062 * 2 # Distance between Wheels [m]

def New_cmd(msg):
    v=msg.linear.x  # Translation Speed [m/s]
    w=msg.angular.z # Angular velocity

    ref_v.r_ref = (v/Rw)+((T*w)/(2*Rw)) #[rad / s]
    ref_v.l_ref = (v/Rw)-((T*w)/(2*Rw)) #[rad / s]
#    ref_v.r_ref = (v/Rw)+((T*w)/(2*Rw))/(2*math.pi)*60 #[rpm]
#    ref_v.l_ref = (v/Rw)-((T*w)/(2*Rw))/(2*math.pi)*60 #[rpm]
    pub.publish(ref_v)

def set():
    rospy.init_node("RL_Cmd_Value", anonymous=False)
    rospy.Subscriber("/cmd_vel", Twist, New_cmd)
    rospy.spin()

if __name__=="__main__":
    try:
        ref_v = RightLeft_cmd_value()
        pub = rospy.Publisher("New_cmd", RightLeft_cmd_value, queue_size=10)
        set()
    except rospy.ROSInterruptException: pass
