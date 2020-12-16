# -*- coding: utf-8 -*-

import os
import math

c_path=os.path.dirname(os.path.abspath(__file__))
path=c_path+'/../../csv/TargetTrajectory_Curve.csv'
with open(path, mode="w") as f:
    print("\nCreate New Trajectory\n")

t=0.0
x=0.0
y=0.0
th=0.0
last_th=0.0
v=0.0
w=0.0

max = 1.0
max = max /2.0
step=50
for i in range(step+1):
    x = max / step * i
    y = max * math.sin(i*(math.pi/2)/step)
    th = math.atan(math.cos(i*(math.pi/2)/step))
    v=0.04
    w=(th-last_th)/10.0

    last_th=th
    buf=str(t)+","+str(x)+","+str(y)+","+str(th)+","+str(v)+","+str(w)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)
