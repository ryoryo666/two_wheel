#! /usr/bin/env python

import rospy
from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Vector3
from std_msgs.msg import Time
from std_msgs.msg import Bool
from two_wheel.msg import curve_data
import DXY
import VW
import math

def callback(data):
    print("Subscribe!")
    sub_data.R=data.R
    sub_data.d=data.d
    flag.data=True
    if sub_data.R==0:
        print("Straight R=%f" % sub_data.R)
    elif sub_data.R != 0:
        print("Curve:R=%f" % sub_data.R)
        print("direction:%s" %sub_data.d)
    print("")
    print(flag)


def Set_pub():
    rospy.init_node("robot_pose_publisher", anonymous=True)
    rospy.Subscriber("curve", curve_data, callback)
    pub=rospy.Publisher("pose", Pose2D, queue_size=10)

    pose.x=0.0
    pose.y=0.0
    pose.theta=math.radians(90)
    r=rospy.Rate(1)

    dt=1
    D=0.3           # Wheel-center distance
    vm=1 # Inner ring vector [m/s]
    t=Time()
    t.data=0.0


    while not rospy.is_shutdown():
        t.data+=dt

        # Straight
        if sub_data.R == 0 and flag.data==True:
            dxy=DXY.DXY(1,pose.theta)
            vector.x=dxy.dx()
            vector.y=dxy.dy()

            pose.x = pose.x + vector.x*dt
            pose.y = pose.y + vector.y*dt

        # Curve
        elif sub_data.R != 0 and flag.data==True:
            vec=VW.VW(sub_data,D,vm)
            v=vec.V()
            w=vec.W()

            dxy=DXY.DXY(v,pose.theta)
            vector.x=dxy.dx()
            vector.y=dxy.dy()

            pose.x = pose.x + vector.x*dt
            pose.y = pose.y + vector.y*dt
            pose.theta = pose.theta + w*dt

        print("%d sec" % t.data)
        print("x:%d\ny:%d\n" %(int(pose.x),int(pose.y)))
        pub.publish(pose)
        r.sleep()

if __name__=="__main__":
    # Turning radius [m]
    # Direction Right or left (r or l)
    sub_data=curve_data()
    pose=Pose2D()
    vector=Vector3()
    flag=Bool()
    flag.data=False
    try:
        Set_pub()
    except rospy.ROSInterruptException: pass
