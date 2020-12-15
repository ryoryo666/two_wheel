# -*- coding: utf-8 -*-

import os
import math

path='/home/ryo/catkin_ws/src/gazebo_sim/csv/TargetTrajectory_Curve.csv'
with open(path, mode="w") as f:
    print("Make New Trajectory")

t=0.0
x=0.0
y=0.0
th=0.0
last_th=0.0
v=0.0
w=0.0

step=21
for x in range(step):
    y=10*math.sin(x*(math.pi/2)/10)
    th=math.atan(math.cos(x*(math.pi/2)/10))
    v=1.0
    w=(th-last_th)/10

    last_th=th
    buf=str(t)+","+str(x+1.0)+","+str(y)+","+str(th)+","+str(v)+","+str(w)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)
