#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Int32
from getch import getch

def sub():
    rospy.init_node("test_sub", anonymous = True)
    while not rospy.is_shutdown():
        print "Input :"
        c = getch()

        if c == "q":
            msg = rospy.wait_for_message("/topic", Int32)
            print msg
        elif c == "c":
            break

if __name__ == "__main__":
    try:
        sub()
    except rospy.ROSInterruptException: pass
