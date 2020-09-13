#! /usr/bin/env python
# -*- coding: utf-8 -*-

from std_msgs.msg import Float32
import rospy
import target_getter

_base_speed=10.0*1000/3600        #[Km/h]　→　[m/s]
_Wheel_radius=0.08      #[m]
_Wheel_separation=0.5   #[m]

def Target_pub():
    rospy.init_node("Target_value_publisher", anonymous=True)
    pub_right=rospy.Publisher("Right_wheel_target_update", Float32, queue_size=10)
    pub_left=rospy.Publisher("Left_wheel_target_update", Float32, queue_size=10)

    while not rospy.is_shutdown():
        Turning_direction=raw_input("\nTurning direction( r or l) >> ")
        if Turning_direction=="q":
            print("\n --------------------------------- ")
            print("|             Finish!             |")
            print(" --------------------------------- \n")

            break;
        Turning_radius=float(raw_input("Turning radius >> "))
        print("")

        get=target_getter.target_getter(Turning_radius, Turning_direction, _base_speed, _Wheel_radius, _Wheel_separation)
        RwT.data=get.VR_RPM()
        LwT.data=get.VL_RPM()

        pub_right.publish(RwT)
        pub_left.publish(LwT)



if __name__=="__main__":
    RwT=Float32()
    LwT=Float32()
    try:
        Target_pub()
    except rospy.ROSInterruptException: pass
