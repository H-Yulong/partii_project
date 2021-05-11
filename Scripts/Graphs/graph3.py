import matplotlib.pyplot as plt
import lib

LOW = 0
HIGH = 600


f = open("../../Data/MaxBeat/8","r")
f.readline()
f.readline()
f.readline()
s = f.readline()
arr = s.split(" ")
x = [i for i in range(LOW,HIGH)]
y = [float(arr[i]) for i in range(LOW,HIGH-6)]
y = [1.0,1.0,1.0,1.0,1.0,1.0] + y
f.close()

f = open("../../Experiment Data/Soli/Opti.txt")
string = f.readline()
string = string[1:-2]
data = string.split(", ")
for i in range(len(data)):
    data[i] = int(data[i])

probs = {}

for d in data:
    if not d in probs.keys():
        probs[d] = 1 / len(data)
    else:
        probs[d] += 1 / len(data)

accu = [0 for _ in range(600)]
for i in range(600):
    if i == 0:
        accu[i] = 1
    else:
        accu[i] = - lib.null_get(probs, i) + accu[i - 1]

y2 = [accu[i] for i in range(LOW,HIGH)]
y3 = [y[i] - y2[i] for i in range(HIGH - LOW)]

fig, ax = plt.subplots()
ax.plot(x,y, label="MaxBeat")
ax.plot(x,y2, label="MaxExp")
ax.plot(x,y3, label="MaxBeat - MaxExp")
ax.legend()
plt.show()
