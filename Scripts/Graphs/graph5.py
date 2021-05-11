import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x = [i for i in range(4)]

y1 = [0.0001, 0.00001, 0.0002,0.0003]
y2 = [0.0007, 0.0007, 0.0026,0.0018]
y3 = [0.0002, 0.0009, 0.0016,0.0029]
y4 = [0.0021, 0.0042, 0.0045,0.0055]

ax.plot(x,y1, label="Pawlewicz's Agent")
ax.plot(x,y2, label="Optimal Solitaire Agent")
ax.plot(x,y3, label="Two-player B")
ax.plot(x,y4, label="Average Agent")

ax.legend()
plt.show()