import matplotlib.pyplot as plt

fig, ax = plt.subplots()

x = [i for i in range(3)]

ya = [0.500, 0.439, 0.424, 0.638, 0.389, 0.157]
yb = [0.561, 0.500, 0.486, 0.662, 0.502, 0.143]
yc = [0.576, 0.514, 0.500, 0.673, 0.523, 0.198]

yya = [0.500, 0.519, 0.482, 0.779, 0.675, 0.470]
yyb = [0.481, 0.500, 0.501, 0.760, 0.684, 0.492]
yyc = [0.518, 0.499, 0.500, 0.775, 0.673, 0.503]

y3a = [0.746, 0.644, 0.636]
y3b = [0.733, 0.620, 0.643]
y3c = [0.740, 0.650, 0.623]

up = [0.531 for _ in range(3)]
low = [0.469 for _ in range(3)]
middle = [0.5 for _ in range(3)]

ax.plot(x, up, label="Confidence interval", color="Orange", linestyle="dashed")
ax.plot(x, low, color="Orange", linestyle="dashed")
ax.plot(x, middle, color="Gray", linestyle="dashed")

ax.scatter(x, y3a, label="Pawlewicz's Agent", color="#00BA00", marker="^", s=100)
ax.scatter(x, y3b, label="Normal Distribution Agent", color="#009000", marker="s", s=100)
ax.scatter(x, y3c, label="Two-Policy Agent", color="#003000", marker="v", s=100)


ax.legend()
plt.show()
