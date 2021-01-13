# -*- coding: utf-8 -*-

import os
import math

c_path=os.path.dirname(os.path.abspath(__file__))
path=c_path+'/../../csv/ReferencePathTrajectory.csv'
with open(path, mode="w") as f:
    print("\nCreate New Curve Path\n")

t = 0.0
x = 0.0
y = 0.0
th = 0.0
last_th = 0.0
v = 0.04
w = 0.0

dt = 0.05
while t <= 25:
    buf=str(t)+","+str(x)+","+str(y)+","+str(th)+","+str(v)+","+str(w)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)

    x += v * dt
    t += dt
