#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist

def pub():
    rospy.init_node("robot_twist_pub",anonymous=True)
    pub=rospy.Publisher("/robo_gazebo/diff_drive_controller/cmd_vel", Twist, queue_size=10)
    
