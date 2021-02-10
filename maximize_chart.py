import matplotlib.pyplot as plt

f = open("Data/Table_Maximize/13_readbale.txt","r")
f.readline()
f.readline()
f.readline()
s = f.readline()
arr = s.split(" ")
x = [i for i in range(1576)]
y = [float(arr[i]) for i in range(len(arr) - 1)]
y = [1.0,1.0,1.0,1.0,1.0,1.0] + y
plt.plot(x,y)
plt.show()
