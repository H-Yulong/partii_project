import matplotlib.pyplot as plt
import lib
import struct

LOW = 0
HIGH = 300

code = lib.code([2,6,9,10,11], 0)
maxbeat_data = []

filename = "../../Data/MaxBeat/8"
f = open(filename, "rb")
state_no = f.read(4)

found = False
while (not found) and (state_no != b""):
    state_no = int.from_bytes(state_no, "little")
    min = int.from_bytes(f.read(4), "little")
    max = int.from_bytes(f.read(4), "little")
    # Read cumulative data
    dist = []
    for j in range(min + 1, max):
        dist.append(struct.unpack('d', f.read(8))[0])

    if state_no == code:
        maxbeat_data = dist
        found = True
    state_no = f.read(4)
f.close()

f = open("../../Experiment Data/Soli/Chosen.txt")
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

maxexp_data = [0 for _ in range(HIGH - LOW)]
for i in range(HIGH - LOW):
    if i == 0:
        maxexp_data[i] = 1
    else:
        maxexp_data[i] = - lib.null_get(probs, i) + maxexp_data[i - 1]

x = [i for i in range(LOW,HIGH)]
y = [float(maxbeat_data[i]) for i in range(LOW,HIGH-6)]
y = [1.0,1.0,1.0,1.0,1.0,1.0] + y
y2 = [maxexp_data[i] for i in range(LOW,HIGH)]
y3 = [y[i] - y2[i] for i in range(HIGH - LOW)]

fig, ax = plt.subplots()
ax.plot(x,y, label="MaxBeat")
ax.plot(x,y2, label="MaxExp")
ax.plot(x,y3, label="MaxBeat - MaxExp")
ax.legend()
plt.show()