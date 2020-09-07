import numpy as np
import matplotlib.pyplot as plt

data=np.loadtxt("plot_data.csv", delimiter = ",")
x=data[:,0]
y=data[:,1]

plt.plot(x,y,color="red")
plt.title("PID control result")
plt.xlabel("Time[s]")
plt.ylabel("output")
plt.xlim(0,)
plt.ylim(0,)
plt.grid()
plt.show()
