#参照軌道と追従結果をグラフで表示
import glob,os
import numpy as np
import matplotlib.pyplot as plt

fig, ax=plt.subplots()

c_path=os.path.dirname(os.path.abspath(__file__))
file_list_T=glob.glob(os.path.join(c_path, "Tracking*"))
file_list_R=glob.glob(os.path.join(c_path, "Reference*"))
file_list_T.sort()
file_list_R.sort()

#追従結果軌道データを選択
for i in range(len(file_list_T)):
	print str(i)+": "+file_list_T[i].replace(c_path+"/", "")
number1=int(raw_input("File Number1>> "))
data1=np.loadtxt(fname=file_list_T[number1], delimiter = ",")
file_list_T[number1] = file_list_T[number1].replace(c_path+"/", "")
print ""

#参照軌道データを選択
for i in range(len(file_list_R)):
	print str(i)+": "+file_list_R[i].replace(c_path+"/", "")
number2=int(raw_input("File Number2>> "))
data2=np.loadtxt(fname=file_list_R[number2], delimiter = ",")
file_list_R[number2] = file_list_R[number2].replace(c_path+"/", "")

x1=data1[:,1]
y1=data1[:,2]
x2=data2[:,1]
y2=data2[:,2]

Real_label = file_list_T[number1].replace(".csv","")
Reference_label = file_list_R[number2].replace(".csv","")

ax.plot(x1,y1,color="green", label=Real_label)
ax.scatter(x2,y2,color="red", label=Reference_label,alpha=0.6, s=1)

# Label Name
ax.set_xlabel("X[m]", fontsize=18)
ax.set_ylabel("Y[m]", fontsize=18)

# x and y Axis Limit
x_lim = 0.5
y_lim = 0.5
ax.set_xlim(-1 * x_lim, y_lim)
ax.set_ylim(-1 * x_lim, y_lim)

# Position Adjustment
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.2)

# Label Font Size
ax.tick_params(labelsize=15)

ax.grid()
ax.legend()
plt.show()
