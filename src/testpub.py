#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int32

def pub():
    rospy.init_node("test_pub", anonymous = True)
    pub = rospy.Publisher("topic", Int32, queue_size = 1)
    r = rospy.Rate(1)
    msg = Int32()
    msg.data = 0

    while not rospy.is_shutdown():
        msg.data += 1
        print msg
        pub.publish(msg)
        r.sleep()

if __name__ == "__main__":
    try:
        pub()
    except rospy.ROSInterruptException: pass
