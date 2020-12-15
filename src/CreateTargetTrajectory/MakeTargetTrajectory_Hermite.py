# -*- coding: utf-8 -*-

import os
import math
import HermiteCurve

path='../../csv/TargetTrajectory_Hermite.csv'
with open(path, mode="w") as f:
    print("New Trajectory")

x_ref=[0,5]
y_ref=[0,5]
vx_ref=[1,0]
vy_ref=[0,10]
c=0.0
t=0.0
dt=0.001
print "{0},{1} to {2},{3}".format(x_ref[0],y_ref[0],x_ref[1],y_ref[1])

hermite=HermiteCurve.HermiteCurve(x_ref,y_ref,vx_ref,vy_ref)
while(c<=1):
	x=hermite.Xt(c)
	y=hermite.Yt(c)
	theta=hermite.Tht(c)
	v=1.0
	w=hermite.Wt(c,dt)*2

	c+=dt
	t=t+dt*10
	buf=str(t)+","+str(x)+","+str(y)+","+str(theta)+","+str(v)+","+str(w)+"\n"
	with open(path, mode="a") as f:
		f.write(buf)



x_ref=[x,10]
y_ref=[y,10]
vx_ref=[0,10]
vy_ref=[hermite.Vyt(c),0]
c=0.0
print "{0},{1} to {2},{3}".format(x_ref[0],y_ref[0],x_ref[1],y_ref[1])

hermite=HermiteCurve.HermiteCurve(x_ref,y_ref,vx_ref,vy_ref)
while(c<=1):
	x=hermite.Xt(c)
	y=hermite.Yt(c)
	theta=math.atan2(hermite.Vyt(c),hermite.Vxt(c))
	v=hermite.Vt(c)

	c+=dt
	t=t+dt*10
	buf=str(t)+","+str(x)+","+str(y)+","+str(theta)+","+str(v)+","+str(w)+"\n"
	with open(path, mode="a") as f:
		f.write(buf)
