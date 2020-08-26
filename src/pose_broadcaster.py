#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Pose2D
import tf

def pose_broadcaster(pose):
    br=tf.TransformBroadcaster()
    br.sendTransform((pose.x, pose.y, 0.0), tf.transformations.quaternion_from_euler(0, 0, pose.theta), rospy.Time.now(), "body_link", "base_link")


if __name__=="__main__":
    rospy.init_node("pose_broadcaster",  anonymous=True)
    rospy.Subscriber("pose", Pose2D, pose_broadcaster)

    rospy.spin()
