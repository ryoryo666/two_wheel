# -*- coding: utf-8 -*-

import os
import math

c_path=os.path.dirname(os.path.abspath(__file__))
path=c_path+'/../../csv/ReferenceTrajectory_DFL.csv'
with open(path, mode="w") as f:
    print("\nCreate New Reference Path\n")

t = 0.0
x = 0.0
y = 0.0
vx = 0.04   #[m/s]
vy = 0.0    #[m/s]

dt = 0.05
while t <= 25:
    buf=str(t)+","+str(x)+","+str(y)+","+str(vx)+","+str(vy)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)

    x += vx * dt
    y += vy * dt
    t += dt
