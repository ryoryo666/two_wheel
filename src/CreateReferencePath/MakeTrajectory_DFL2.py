# -*- coding: utf-8 -*-

import os
import math

c_path=os.path.dirname(os.path.abspath(__file__))
path=c_path+'/../../csv/ReferenceTrajectory_DFL2.csv'
with open(path, mode="w") as f:
    print("\nCreate New Reference Path\n")

t = 0.0
x = 0.25
y = 0.0

dt = 0.05
while t <= 30.0:
    x = 0.25 * math.cos((math.pi*t) / 15.0)
    y = 0.25 * math.sin((math.pi*t) / 15.0)
    vx = 0.25 * (math.pi/15.0) * math.sin((math.pi*t) / 15.0) * -1
    vy = 0.25 * (math.pi/15.0) * math.cos((math.pi*t) / 15.0)
    ax = 0.25 * (math.pi/15.0)**2 * math.cos((math.pi*t) / 15.0) * -1
    ay = 0.25 * (math.pi/15.0)**2 * math.sin((math.pi*t) / 15.0) * -1


    t += dt

    buf=str(t)+","+str(x)+","+str(y)+","+str(vx)+","+str(vy)+","+str(ax)+","+str(ay)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)
