#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from two_wheel.msg import curve_data

def curve_info_pub():
    rospy.init_node("turning info publisher", anonymous=True)
    pub=rospy.Publisher("turning_info", curve_data, queue_size=10)
    begin=rospy.Time.now()

    while not rospy.is_shutdown():
        turning_info.Radius=float(raw_input("Turning radius: "))
        turning_info.Direction=raw_input("Turning direction:")
        print("")
        time=rospy.Time.now()
        du=time-begin
        dt=du.secs+(du.nsecs/10.0**9)
        print dt
        print du.secs
        print du.nsecs/10.0**9
        pub.publish(turning_info)

if __name__=="__main__":
    turning_info=curve_data()
    try:
        curve_info_pub()
    except rospy.ROSInterruptException: pass
