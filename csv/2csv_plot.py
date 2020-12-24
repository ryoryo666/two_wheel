import glob,os
import numpy as np
import matplotlib.pyplot as plt

fig, ax=plt.subplots()

c_path=os.path.dirname(os.path.abspath(__file__))
#file_list_M=glob.glob(os.path.join(c_path, "Real*"))
#file_list_T=glob.glob(os.path.join(c_path, "ReferencePath*"))
file_list_M=glob.glob(os.path.join(c_path, "R-*"))
file_list_T=glob.glob(os.path.join(c_path, "L-*"))

file_list_M.sort()
for i in range(len(file_list_M)):
	print str(i)+": "+file_list_M[i].replace(c_path+"/", "")
number1=int(raw_input("File Number1>> "))
data1=np.loadtxt(fname=file_list_M[number1], delimiter = ",")
file_list_M[number1] = file_list_M[number1].replace(c_path+"/", "")

print ""
file_list_T.sort()
for i in range(len(file_list_T)):
	print str(i)+": "+file_list_T[i].replace(c_path+"/", "")
number2=int(raw_input("File Number2>> "))
data2=np.loadtxt(fname=file_list_T[number2], delimiter = ",")
file_list_T[number2] = file_list_T[number2].replace(c_path+"/", "")

x1=data1[:,1]
y1=data1[:,2]
x2=data2[:,1]
y2=data2[:,2]

Mobile_label = file_list_M[number1].replace(".csv","")
Target_label = file_list_T[number2].replace(".csv","")

ax.plot(x1,y1,color="green", label=Mobile_label)
ax.plot(x2,y2,color="red", label=Mobile_label)
ax.scatter(x2,y2,color="red", label=Target_label,alpha=0.6, s=5)

# Label Name
ax.set_xlabel("X[m]", fontsize=18)
ax.set_ylabel("Y[m]", fontsize=18)

# x and y Axis Limit
lim=1.1
ax.set_xlim(-0.1*lim,lim)
ax.set_ylim(-0.1*lim,lim)

# Position Adjustment
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)

# Label Font Size
ax.tick_params(labelsize=15)

ax.grid()
ax.legend()
plt.show()
