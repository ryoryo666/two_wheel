#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
import matplotlib.pyplot as plt

target=float(raw_input("Target >>"))
target_list=[]
step=10
for i in range(step+1):
    n=float(i)/step
    target_list.append(target*math.cos(n*(math.pi/2)))

t=range(step+1)

plt.scatter(t, target_list)
plt.grid()
plt.show()
print(target_list)
