import lib
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
from scipy.ndimage.filters import gaussian_filter1d

def get_data(filename):
    file = open(filename)
    string = file.readline()
    file.close()
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

    x = [i for i in range(500)]
    y = [0 for _ in range(500)]
    for i in range(500):
        if i == 0:
            y[i] = lib.null_get(probs, i)
        else:
            y[i] = lib.null_get(probs, i) + y[i - 1]

    sx = np.linspace(0, 500, 500)
    sy = gaussian_filter1d(y, sigma=1.7)

    return sx, sy


def main():
    fig, ax = plt.subplots()

    x1, y1 = get_data("../Data/Soli/Opti.txt")
    x2, y2 = get_data("../Data/Soli/SB.txt")
    x3, y3 = get_data("../Data/Soli/Average.txt")

    line1 = ax.plot(x1, y1, label="Optimal Solitaire", color='red')
    line2 = ax.plot(x2, y2, label="Solitaire A", color='green')
    line3 = ax.plot(x3, y3, label="Average Agent", color='orange')

    # Using set_dashes() to modify dashing of an existing line
    # line1, = ax.plot(x, y, label='Using set_dashes()')
    # line1.set_dashes([2, 2, 10, 2])  # 2pt line, 2pt break, 10pt line, 2pt break

    # Using plot(..., dashes=...) to set the dashing when creating a line
    # line2, = ax.plot(x, y - 0.2, dashes=[6, 2], label='Using the dashes parameter')

    ax.legend()
    plt.show()


main()
