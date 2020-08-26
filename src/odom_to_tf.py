#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import tf
from nav_msgs.msg import Odometry

def Converter(msg):
    br=tf.TransformBroadcaster()
    br.sendTransform(msg.pose, tf.transformations.quaternion_from_euler(0, 0, pose.theta), rospy.Time.now(), "odom", msg.child_frame_id)

def Sub():
    rospy.init_node("odom_converter", anonymous=True)
    rospy.Subscriber("/gazebo_position", Odometry, Converter)

    rospy.spin()

if __name__=="__main__":
    try:
        Sub()
    except rospy.ROSInterruptException: pass
