# -*- coding: utf-8 -*-

import os
import math

c_path=os.path.dirname(os.path.abspath(__file__))
path=c_path+'/../../csv/ReferenceTrajectory_DFL1.csv'
with open(path, mode="w") as f:
    print("\nCreate New Reference Path\n")

t = 0.0
x = 0.0
y = 0.0

dt = 0.05
while t <= 20.0:
    x = 0.03 * t
    y = 0.0 * t
    vx = 0.05
    vy = 0.0
    ax = 0.0
    ay = 0.0
    t += dt

    buf=str(t)+","+str(x)+","+str(y)+","+str(vx)+","+str(vy)+","+str(ax)+","+str(ay)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)
