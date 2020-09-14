import numpy as np
import matplotlib.pyplot as plt


data=np.loadtxt(fname="data.csv", delimiter = ",")
x=data[:,0]
y=data[:,1]

plt.plot(x,y,color="red")
#plt.title("PID control result")
plt.title("Target=30rpm Kp=0.18 Kd=0.085", fontsize=18)
plt.xlabel("Time[s]", fontsize=18)
plt.ylabel("Output[rpm]", fontsize=18)
plt.xlim(0,)
plt.ylim(0,40)
plt.tick_params(labelsize=15)
plt.grid()
plt.show()

