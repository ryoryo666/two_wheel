import glob,os
import numpy as np
import matplotlib.pyplot as plt

fig, ax=plt.subplots()

c_path=os.path.dirname(os.path.abspath(__file__))

dataR=np.loadtxt(fname="R-rpm.csv", delimiter = ",")
dataL=np.loadtxt(fname="L-rpm.csv", delimiter = ",")

x1=dataR[:,0]
y1=dataR[:,1]
x2=dataL[:,0]
y2=dataL[:,1]

ax.plot(x1,y1,color="green", label="R-rpm")
ax.plot(x2,y2,color="red", label="L-rpm")

# Label Name
ax.set_xlabel("t[s]", fontsize=18)
ax.set_ylabel("[rpm]", fontsize=18)

# x and y Axis Limit
#ax.set_xlim(-0.1*lim,-1)
#ax.set_ylim(-1,15)

# Position Adjustment
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)

# Label Font Size
ax.tick_params(labelsize=15)

ax.grid()
ax.legend()
plt.show()
