import lib
import struct
import torch
import torch.nn as nn
from scipy.stats import norm
from math import sqrt


class Dist:
    def __init__(self, min, max, dist):
        self.min = min
        self.max = max
        self.dist = dist


class TwoPlayerAgent:

    def __init__(self, name):
        self.name = name
        self.cache = [[[]], lib.dicePatterns(1), lib.dicePatterns(2),
                      lib.dicePatterns(3), lib.dicePatterns(4),
                      lib.dicePatterns(5)]
        return

    def evaluate(self, dice, up, cats, cat, score, state2):
        return 0

    def move(self, state, state2):
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
                v = self.evaluate(state.dice, state.up, state.cats, e, state.score, state2)
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


class TableBased(TwoPlayerAgent):

    def __init__(self):
        TwoPlayerAgent.__init__(self, "TableBasedTwoPlayer")
        empty_dist = Dist(0, 0, [])
        self.library = {"full": empty_dist}
        print("Loading library...")
        print("Please wait for a few minutes...")
        for i in range(1, 14):
            filename = "../Data/MaxProb/" + str(i)
            f = open(filename, "rb")
            state = f.read(4)

            while state != b"":
                state = int.from_bytes(state, "little")
                min = int.from_bytes(f.read(4), "little")
                max = int.from_bytes(f.read(4), "little")
                # Read cumulative data
                dist = []
                for j in range(min + 1, max):
                    dist.append(struct.unpack('d', f.read(8))[0])

                # Process Estimation
                dist2 = []
                dist2.append(1 - dist[0])
                for j in range(len(dist) - 1):
                    dist2.append(dist[j] - dist[j + 1])
                dist2.append(dist[len(dist) - 1])

                # Add to dictionary
                self.library[state] = Dist(min, max, dist2)
                state = f.read(4)

            f.close()
        print("Loading finished!")

    def evaluate(self, dice, up, cats, cat, score, state2):
        v, new_cat, up = lib.fillScore(dice, up, cats, cat)

        dist = self.library.get(lib.code(new_cat, up))
        dist2 = self.library.get(lib.code(state2.cats, state2.up))
        rank = 0

        # Calculate Expected rank:
        # sum( pr(player1's score = s) * sum( pr(player2's score = 7) * (s > t) ) )

        for i in range(dist.min, min(dist.max, 500 - score)):
            new_score = v + score + i

            if new_score >= dist2.max + state2.score:
                rank += dist.dist[i - dist.min]
            else:
                for j in range(dist2.min + state2.score, new_score):
                    rank += dist.dist[i - dist.min] * dist2.dist[j - dist2.min - state2.score]

        return rank


class NNAgent(TwoPlayerAgent):

    def __init__(self, path, hidden_size1, hidden_size2):
        TwoPlayerAgent.__init__(self, "NNTwoPlayer")
        self.model = nn.Sequential(nn.Linear(32, hidden_size1, False),
                                   nn.Sigmoid(),
                                   nn.Linear(hidden_size1, hidden_size2, False),
                                   nn.Sigmoid(),
                                   nn.Linear(hidden_size2, 1, False),
                                   nn.Sigmoid())
        self.model.load_state_dict(torch.load(path), strict=False)

    def evaluate(self, dice, up, cats, cat, score, state2):
        v, new_cat, up = lib.fillScore(dice, up, cats, cat)
        states = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for c in new_cat:
            if c >= 0:
                states[c] = 1
        y_state = 0
        if -1 in new_cat:
            y_state = -1
        elif 0 in new_cat:
            y_state = 1

        states2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for c in state2.cats:
            if c >= 0:
                states2[c] = 1
        y_state2 = 0
        if -1 in state2.cats:
            y_state2 = -1
        elif 0 in state2.cats:
            y_state2 = 1

        return self.model(torch.tensor(
            states + [up, y_state, score + v] + states2 + [state2.up, y_state2, state2.score],
            dtype=torch.float32))


class NNAgent2(TwoPlayerAgent):
    def __init__(self, path):
        TwoPlayerAgent.__init__(self, "TableBasedTwoPlayer")
        hidden_size1 = 32
        hidden_size2 = 64
        hidden_size3 = 32
        self.model = nn.Sequential(nn.Linear(32, hidden_size1, False),
                                   nn.Sigmoid(),
                                   nn.Linear(hidden_size1, hidden_size2, False),
                                   nn.Sigmoid(),
                                   nn.Linear(hidden_size2, hidden_size3, False),
                                   nn.Tanh(),
                                   nn.Linear(hidden_size3, 1, False),
                                   nn.Tanh())
        self.model.load_state_dict(torch.load(path))

    def evaluate(self, dice, up, cats, cat, score, state2):
        v, new_cat, up = lib.fillScore(dice, up, cats, cat)
        states = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for c in new_cat:
            if c >= 0:
                states[c] = 1
        y_state = 0
        if -1 in new_cat:
            y_state = -1
        elif 0 in new_cat:
            y_state = 1

        states2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for c in state2.cats:
            if c >= 0:
                states2[c] = 1
        y_state2 = 0
        if -1 in state2.cats:
            y_state2 = -1
        elif 0 in state2.cats:
            y_state2 = 1

        return v + self.model(torch.tensor(
            states + [up, y_state, score + v] + states2 + [state2.up, y_state2, state2.score],
            dtype=torch.float32)) * 300


class TwoPolicyAgent(TwoPlayerAgent):

    def __init__(self):
        TwoPlayerAgent.__init__(self, "MixedTwoPlayer")
        self.dictionary = {"full": 0}
        self.dictionary_sqr = {"full": 0}
        empty_dist = Dist(0, 0, [])
        self.library = {"full": empty_dist}
        with open("../Data/Optimal Solitaire/optimal.txt") as f:
            for line in f:
                (key, val, val_sqr) = line.split(", ")
                self.dictionary[int(key)] = float(val)
                self.dictionary_sqr[int(key)] = float(val_sqr)
        self.improve = 0
        self.improve_count = 0

    def move(self, state, state2):
        self_code = lib.code(state.cats, state.up)
        oppo_code = lib.code(state2.cats, state2.up)

        self_potential = state.score + self.dictionary.get(self_code)
        oppo_potential = state2.score + self.dictionary.get(oppo_code)

        if self_potential + sqrt(self.dictionary_sqr.get(self_code)) >= oppo_potential:
            # Follow solitarie optimal if expected score is higher
            self.evaluate = self.opti_evaluate
        else:
            # 1. Estimate game result using Normal Distribution, if both following optimal strategy
            # 2. Assume opponent's score is his expected score, and beat it with maximal probability
            # Choose the one between 1 and 2 with higher win rate

            self_var = self.dictionary_sqr.get(self_code)
            oppo_var = self.dictionary_sqr.get(oppo_code)

            opti_winrate = 1 - norm.cdf((oppo_potential - self_potential) / sqrt(self_var + oppo_var))

            self_dist = self.lib_get(self_code)

            risky_winrate = 0
            if self_dist.max > (oppo_potential - state.score):
                risky_winrate = self_dist.dist[int(oppo_potential - state.score - self_dist.min - 1)]

            # print(opti_winrate, risky_winrate)

            if opti_winrate >= risky_winrate:
                self.evaluate = self.opti_evaluate
                # print("Opti move!")
            else:
                self.evaluate = self.risky_evaluate
                self.improve += (risky_winrate - opti_winrate)
                self.improve_count += 1
                # print("Risky move!")

        return TwoPlayerAgent.move(self, state, state2)

    def opti_evaluate(self, dice, up, cats, cat, score, state2):
        v, new_cat, up = lib.fillScore(dice, up, cats, cat)
        v += self.dictionary.get(lib.code(new_cat, up))
        return v

    def risky_evaluate(self, dice, up, cats, cat, score, state2):
        v, new_cat, up = lib.fillScore(dice, up, cats, cat)
        oppo_potential = self.dictionary.get(lib.code(state2.cats, state2.up)) + state2.score
        dist = self.lib_get(lib.code(new_cat, up))
        if (oppo_potential - v - score) > dist.min:
            if (oppo_potential - v - score) > dist.max:
                return 0
            else:
                return dist.dist[int(oppo_potential - v - score - dist.min - 1)]
        else:
            return 1

    def lib_get(self, code):
        # Lazy load library
        if (code not in self.library.keys()):
            cats, up = lib.decode(code)
            empty = 13 - len(cats)
            filename = "../Data/Table_Maximize/" + str(empty)
            print("Lazy loading table " + str(empty) + "...")
            f = open(filename, "rb")
            state_no = f.read(4)

            while state_no != b"":
                state_no = int.from_bytes(state_no, "little")
                min = int.from_bytes(f.read(4), "little")
                max = int.from_bytes(f.read(4), "little")
                # Read cumulative data
                dist = []
                for j in range(min + 1, max):
                    dist.append(struct.unpack('d', f.read(8))[0])

                # Add to dictionary
                self.library[state_no] = Dist(min, max, dist)
                state_no = f.read(4)
            f.close()
        return self.library.get(code)


class NormalAgent(TwoPlayerAgent):
    def __init__(self):
        TwoPlayerAgent.__init__(self, "NormalTwoPlayer")
        self.dictionary = {"full": 0}
        self.dictionary_sqr = {"full": 0}
        empty_dist = Dist(0, 0, [])
        with open("../Data/Optimal Solitaire/optimal_variance.txt") as f:
            for line in f:
                (key, val, val_sqr) = line.split(", ")
                self.dictionary[int(key)] = float(val)
                self.dictionary_sqr[int(key)] = float(val_sqr)

    def evaluate(self, dice, up, cats, cat, score, state2):
        v, new_cat, up = lib.fillScore(dice, up, cats, cat)
        self_potential = v + self.dictionary.get(lib.code(new_cat, up)) + score
        oppo_potential = state2.score + self.dictionary.get(lib.code(state2.cats, state2.up))
        self_var = self.dictionary_sqr.get(lib.code(new_cat, up))
        oppo_var = self.dictionary_sqr.get(lib.code(state2.cats, state2.up))

        if (self_var == 0) and (oppo_var == 0):
            if self_potential > oppo_potential:
                return 1
            else:
                return 0
        return 1 - norm.cdf((oppo_potential - self_potential) / sqrt(self_var + oppo_var))
