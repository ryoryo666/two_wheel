# -*- coding: utf-8 -*-

import os
import math

c_path=os.path.dirname(os.path.abspath(__file__))
path=c_path+'/../../csv/ReferenceTrajectory2.csv'
with open(path, mode="w") as f:
    print("\nCreate New Curve Path\n")

t = 0.0
x = 0.25
y = 0.0
th = math.pi / 2.0
last_th = th
v = 0.0
w = 0.0

dt = 0.05

buf=str(t)+","+str(x)+","+str(y)+","+str(th)+","+str(v)+","+str(w)+"\n"
with open(path, mode="a") as f:
    f.write(buf)

while t <= 30.0:
    w = 2*math.pi / 30.0
    x = 0.25 * math.cos((math.pi*t) / 15.0)
    y = 0.25 * math.sin((math.pi*t) / 15.0)
    th = last_th + w * t
    vx = 0.25 * (math.pi/15.0) * math.sin((math.pi*t) / 15.0) * -1
    vy = 0.25 * (math.pi/15.0) * math.cos((math.pi*t) / 15.0)
    v = math.sqrt(vx**2 + vy**2)

    t += dt

    buf=str(t)+","+str(x)+","+str(y)+","+str(th)+","+str(v)+","+str(w)+"\n"
    with open(path, mode="a") as f:
        f.write(buf)
