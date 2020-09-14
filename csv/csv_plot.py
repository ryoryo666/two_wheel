import numpy as np
import matplotlib.pyplot as plt


r_data=np.loadtxt(fname="R_data.csv", delimiter = ",")
xr=r_data[:,0]
yr=r_data[:,1]

l_data=np.loadtxt(fname="L_data.csv", delimiter = ",")
xl=l_data[:,0]
yl=l_data[:,1]

plt.plot(xr,yr,color="red",label="Right")
plt.plot(xl,yl,color="green",label="Left")

plt.title("Kp=0.18 Kd=0.085", fontsize=18)
plt.xlabel("Time[s]", fontsize=18)
plt.ylabel("Output[rpm]", fontsize=18)
#plt.ylabel("speed [m/s]", fontsize=18)
plt.xlim(0,)
plt.ylim(0,)
plt.tick_params(labelsize=15)
plt.grid()
plt.legend()
plt.show()

