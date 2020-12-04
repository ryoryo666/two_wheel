#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
from geometry_msgs.msg import Twist
from two_wheel.msg import target_curve

Rw = 0.4    # Wheel Radius [m]
T  = 0.4    # Distance between Wheels [m]

def New_cmd(msg):
    v=msg.linear.x  # Translation Speed [m/s]
    w=msg.angular.z # Angular velocity

    target.r_target = (v/Rw)+((T*w)/(2*Rw)) # [rad / s]
    target.l_target = (v/Rw)-((T*w)/(2*Rw)) # [rad / s]
#    target.r_target = (v/Rw)+((T*w)/(2*Rw))/(2*math.pi)*60 # [rpm]
#    target.l_target = (v/Rw)-((T*w)/(2*Rw))/(2*math.pi)*60 # [rpm]
    pub.publish(target)

def set():
    rospy.init_node("RL_Target_Publisher", anonymous=False)
    rospy.Subscriber("/cmd_vel", Twist, New_cmd)
    rospy.spin()

if __name__=="__main__":
    try:
        target = target_curve()
        pub = rospy.Publisher("target_update", target_curve, queue_size=10)
        set()
    except rospy.ROSInterruptException: pass
