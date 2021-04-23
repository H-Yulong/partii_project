import lib
import struct
import torch
import torch.nn as nn
from scipy.stats import norm
from math import sqrt


class ThreePlayerAgent:

    def __init__(self, name):
        self.name = name
        self.cache = [[[]], lib.dicePatterns(1), lib.dicePatterns(2),
                      lib.dicePatterns(3), lib.dicePatterns(4),
                      lib.dicePatterns(5)]
        return

    def evaluate(self, dice, up, cats, cat, score, state2, state3):
        return 0

    def move(self, state, state2, state3):
        full = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        empty = list(full)
        for c in state.cats:
            if c == -1:
                empty.remove(0)
            elif c == 0:
                empty.remove(0)
            else:
                empty.remove(c)

        if state.rolls == 0:
            max_cat = empty[0]
            max_score = 0
            for e in empty:
                v = self.evaluate(state.dice, state.up, state.cats, e, state.score, state2, state3)
                if v > max_score:
                    max_cat = e
                    max_score = v
            state.fill(max_cat)
            if not state.gameover:
                state.rolls = 3
                state.roll([])
            return

        R3 = {}
        # Evaluate R3
        for d in self.cache[5]:
            max_exp = 0
            # max_cat = 0
            for e in empty:
                score = self.evaluate(d, state.up, state.cats, e, state.score, state2)
                if score > max_exp:
                    max_exp = score
                    # max_cat = e
            R3[self.cache[5].index(d)] = max_exp

        K2 = {}
        for d in self.cache[5]:
            K2[self.cache[5].index(d) * 10 + 5] = R3[self.cache[5].index(d)]
        for k in range(4, -1, -1):
            for d in self.cache[k]:
                exp = 0
                for e in range(1, 7):
                    new_d = lib.extend(d, e)
                    exp += K2[self.cache[k + 1].index(new_d) * 10 + k + 1]
                K2[self.cache[k].index(d) * 10 + k] = exp / 6

        if state.rolls == 1:
            max_keep = []
            max_exp = 0.0

            for key, val in K2.items():
                d = self.cache[key % 10][key // 10]
                # print(d, val)

                if lib.subset(d, state.dice):
                    if val > max_exp:
                        max_exp = val
                        max_keep = d
            if (lib.subset(max_keep, state.dice)) and lib.subset(state.dice, max_keep):
                state.rolls = 0
                # self.move(state, state2)
            else:
                state.roll(max_keep)

            return max_keep

        R2 = {0: K2.get(0)}
        for k in range(1, 6):
            for d in self.cache[k]:
                max_exp = K2.get(self.cache[k].index(d) * 10 + k)
                for e in range(1, 7):
                    r = lib.remove(d, e)
                    if r or (r == []):
                        max_exp = max(max_exp, R2[self.cache[k - 1].index(r) * 10 + k - 1])
                R2[self.cache[k].index(d) * 10 + k] = max_exp

        # Evaluate K1
        K1 = {}
        for d in self.cache[5]:
            K1[self.cache[5].index(d) * 10 + 5] = R2[self.cache[5].index(d) * 10 + 5]
        for k in range(4, -1, -1):
            for d in self.cache[k]:
                exp = 0
                for e in range(1, 7):
                    new_d = lib.extend(d, e)
                    exp += K1[self.cache[k + 1].index(new_d) * 10 + k + 1]
                K1[self.cache[k].index(d) * 10 + k] = exp / 6

        if state.rolls == 2:
            max_keep = []
            max_exp = 0.0
            for key, val in K1.items():
                d = self.cache[key % 10][key // 10]

                if lib.subset(d, state.dice):
                    if val > max_exp:
                        max_exp = val
                        max_keep = d
            if (lib.subset(max_keep, state.dice)) and lib.subset(state.dice, max_keep):
                state.rolls = 0
                # self.move(state, state2)
            else:
                state.roll(max_keep)

            return max_keep

        if state.rolls == 3:
            state.roll([])
            return

        raise Exception("Invalid roll number: greater than 2")


class MostDangerousAgent:
    def __init__(self):
        return
