#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
import matplotlib.pyplot as plt

if __name__=="__main___":
    data=np.loadtxt(fname=data1, delimiter = ",")
    x=data[:,0]
    y=data[:,1]

    plt.plot(x,y,color="red")
    plt.title("PID control result")
    plt.xlabel("Time[s]")
    plt.ylabel("output")
    plt.xlim(0,)
    lt.ylim(0,)
    plt.grid()
    plt.show()
