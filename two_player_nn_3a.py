"""
This is the first part of the thrid two-player agent
Aim: use supervised learning to fit a model of optimal solitaire agent
"""
import math
import random
import torch
import torch.nn as nn
import lib
import torch.nn.functional as F
import numpy


def generate_features(num):
    dictionary = {"full": 0}
    with open("Data/output.txt") as f:
        for line in f:
            (key, val) = line.split(", ")
            dictionary[int(key)] = float(val)
    listd = list(dictionary.items())

    result = []
    for _ in range(num):
        key, val = random.choice(listd)
        result.append([key, val])

    return result


def input_format(n, fill_right):
    # Extract up
    up = n % 64
    n = n // 64
    cats = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    y_state = 0

    # Extract Yahtzee state
    if n % 2 == 1:
        cats[0] = 1
        y_state = -1
        n = n // 2
    else:
        n = n // 2
        if n % 2 == 1:
            cats[0] = 1
            y_state = 1
    n = n // 2

    # Extract other states
    for i in range(1, 13):
        cats[i] = n % 2
        n = n // 2

    # Formatting
    fill = [0 for i in range(16)]
    if fill_right:
        return torch.tensor(cats + [up, y_state, 0] + fill, dtype=torch.float32)
    else:
        return torch.tensor(fill + cats + [up, y_state, 0], dtype=torch.float32)


def main():
    input_size = 32
    hidden_size1 = 32
    hidden_size2 = 64
    hidden_size3 = 32
    output_size = 1
    a = 0.1
    episodes = 10000
    test_state = 0

    # Generate Features
    features = generate_features(episodes)

    # Setup Network
    m = nn.Sequential(nn.Linear(input_size, hidden_size1, False),
                      nn.Sigmoid(),
                      nn.Linear(hidden_size1, hidden_size2, False),
                      nn.Sigmoid(),
                      nn.Linear(hidden_size2, hidden_size3, False),
                      nn.Tanh(),
                      nn.Linear(hidden_size3, output_size, False),
                      nn.Tanh())

    for p in m.parameters():
        # p.data = torch.zeros_like(p)
        p.grad = torch.zeros_like(p)

    print("training...")

    # Supervised learning
    for i in range(episodes):
        state = features[i][0]
        val = features[i][1] / 300 + numpy.random.normal(0,0.5)

        loss = (val - m(input_format(state, True))) ** 2
        loss.backward()
        with torch.no_grad():
            for p in m.parameters():
                p -= p.grad * a
            m.zero_grad()

        #print(loss)
        print(m(input_format(test_state, True)))

    torch.save(m.state_dict(), "Data/two_player4.pt")


main()
