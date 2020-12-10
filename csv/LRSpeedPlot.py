import glob,os
import numpy as np
import matplotlib.pyplot as plt

fig, ax=plt.subplots()

file_list_1=glob.glob(os.path.join("", "R*"))
file_list_2=glob.glob(os.path.join("", "L*"))

file_list_1.sort()
#for i in range(len(file_list_1)):
#	print str(i)+": "+file_list_1[i]
#number1=int(raw_input("File Number1>> "))
number1=0
data1=np.loadtxt(fname=file_list_1[number1], delimiter = ",")
print ""

file_list_2.sort()
#for i in range(len(file_list_2)):
#	print str(i)+": "+file_list_2[i]
#number2=int(raw_input("File Number2>> "))
number2=0
data2=np.loadtxt(fname=file_list_2[number2], delimiter = ",")

x1=data1[:,0]
y1=data1[:,1]
x2=data2[:,0]
y2=data2[:,1]

ax.plot(x1,y1,color="green", label=file_list_1[number1].replace(".csv",""))
ax.plot(x2,y2, color="red", label=file_list_2[number2].replace(".csv",""))

# Label Name
ax.set_xlabel("X[m]", fontsize=18)
ax.set_ylabel("Y[m]", fontsize=18)

# x and y Axis Limit
#lim=10
#ax.set_xlim(-1*lim,lim)
#ax.set_ylim(-1*lim,lim)

# Position Adjustment
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)

# Label Font Size
ax.tick_params(labelsize=15)

ax.grid()
ax.legend()
plt.show()
