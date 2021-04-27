import lib
import Agents.environment as env
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
from scipy.ndimage.filters import gaussian_filter1d
from scipy.stats import norm

file = open("../../Experiment Data/Soli/Opti.txt")
string = file.readline()
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

FAC = 0.4

x = [i for i in range(500)]
y = [lib.null_get(probs,i) for i in range(500)]
y2 = [norm.pdf(i, 254.9583, FAC * 60.6990) for i in range(500)]

plt.plot(x,y)
plt.plot(x,y2)
plt.show()