"""
This is the first part of the third two-player agent
Aim: use supervised learning to fit a model of optimal solitaire agent
"""
import random
import torch
import torch.nn as nn
import numpy

INPUT_SIZE = 32
HIDDEN_SIZE1 = 32
HIDDEN_SIZE2 = 64
HIDDEN_SIZE3 = 32
OUTPUT_SIZE = 1
ALPHA = 0.1
EPISODES = 10
OUTPUT_PATH = "../Data/Neural Network/output.pt"

def generate_features(num):
    dictionary = {"full": 0}
    with open("../Data/Optimal Solitaire/optimal.txt") as f:
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
    test_state = 0

    # Generate Features
    features = generate_features(EPISODES)

    # Setup Network
    m = nn.Sequential(nn.Linear(INPUT_SIZE, HIDDEN_SIZE1, False),
                      nn.Sigmoid(),
                      nn.Linear(HIDDEN_SIZE1, HIDDEN_SIZE2, False),
                      nn.Sigmoid(),
                      nn.Linear(HIDDEN_SIZE2, HIDDEN_SIZE3, False),
                      nn.Tanh(),
                      nn.Linear(HIDDEN_SIZE3, OUTPUT_SIZE, False),
                      nn.Tanh())

    for p in m.parameters():
        # p.data = torch.zeros_like(p)
        p.grad = torch.zeros_like(p)

    print("training...")

    # Supervised learning
    for i in range(EPISODES):
        state = features[i][0]
        val = features[i][1] / 300 + numpy.random.normal(0, 0.5)

        loss = (val - m(input_format(state, True))) ** 2
        loss.backward()
        with torch.no_grad():
            for p in m.parameters():
                p -= p.grad * ALPHA
            m.zero_grad()

        # print(loss)
        print(m(input_format(test_state, True)))

    torch.save(m.state_dict(), OUTPUT_PATH)


main()
