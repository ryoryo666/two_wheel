#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist
from std_msgs.msg import Time
from std_msgs.msg import Bool
from two_wheel.msg import curve_data
import VW
import math

def callback(data):
    print("Subscribe!")
    Turning_info.Radius=data.Radius
    Turning_info.Direction=data.Direction
    flag.data=True
    if Turning_info.Direction=="s":
        flag.data=False
        print("Robot stop")
    elif Turning_info.Radius==0:
        print("Straight")
    elif Turning_info.Radius != 0:
        print("Curve:R=%f" % Turning_info.Radius)
        print("Direction:%s (r:Right l:Left)" %Turning_info.Direction)


def pub():
    rospy.init_node("robot_pose_publisher", anonymous=True)
    rospy.Subscriber("turning_info", curve_data, callback)
    pub=rospy.Publisher("pose", Pose2D, queue_size=10)

    pose.x=0.0
    pose.y=0.0
    pose.theta=math.radians(90)
    r=rospy.Rate(10)

    D=0.3           # Wheel-center distance
    vec_straight=0.5    # Center vector [m/s]
    vec_inner=0.5            # Inner ring vector [m/s]
    t=Time(data=0.0)
    dt=0.1

    while not rospy.is_shutdown():
        t.data+=dt

        # Straight
        if Turning_info.Radius == 0 and flag.data==True:
            vector.linear.x= vec_straight * math.cos(pose.theta)
            vector.linear.y= vec_straight * math.sin(pose.theta)

            pose.x = pose.x + vector.linear.x*dt
            pose.y = pose.y + vector.linear.y*dt

        # Curve
        elif Turning_info.Radius != 0 and flag.data==True:
            vec=VW.VW(Turning_info,D,vec_inner)
            turning_v=vec.V() #center vector
            vector.linear.x= turning_v * math.cos(pose.theta)
            vector.linear.y= turning_v * math.sin(pose.theta)
            vector.angular.z=vec.W()

            pose.x = pose.x + vector.linear.x*dt
            pose.y = pose.y + vector.linear.y*dt
            pose.theta = pose.theta + vector.angular.z*dt

        pub.publish(pose)
        r.sleep()

if __name__=="__main__":
    Turning_info=curve_data()
    pose=Pose2D()
    vector=Twist()
    flag=Bool(data=False)

    try:
        pub()
    except rospy.ROSInterruptException: pass
