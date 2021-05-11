import lib
import Agents.two_player_agents as twopl
import Agents.solitaire_agents as solitaire
from scipy.stats import norm
from math import sqrt


class MultiPlayerAgent:
    def __init__(self, name):
        self.name = name
        self.cache = [[[]], lib.dicePatterns(1), lib.dicePatterns(2),
                      lib.dicePatterns(3), lib.dicePatterns(4),
                      lib.dicePatterns(5)]
        return

    def evaluate(self, dice, up, cats, cat, score, opponent_states):
        return 0

    def move(self, state, opponent_states):
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
                v = self.evaluate(state.dice, state.up, state.cats, e, state.score, opponent_states)
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
                score = self.evaluate(d, state.up, state.cats, e, state.score, opponent_states)
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


class MostDangerousAgent(MultiPlayerAgent):
    def __init__(self):
        MultiPlayerAgent.__init__(self, "MostDangerous")
        self.two_player_agent = twopl.TwoPolicyAgent()

    def move(self, state, opponent_states):
        strengths = []
        for i in range(len(opponent_states)):
            strengths.append(self.two_player_agent.dictionary.get(
                lib.code(opponent_states[i].cats, opponent_states[i].up)))

        dangerous_opponent = strengths.index(max(strengths))

        return self.two_player_agent.move(state, opponent_states[dangerous_opponent])


class NormalAgent(MultiPlayerAgent):
    def __init__(self):
        MultiPlayerAgent.__init__(self, "Normal")
        self.dictionary = {"full": 0}
        self.dictionary_sqr = {"full": 0}
        k = 0.16
        with open("../Data/Optimal Solitaire/optimal_variance.txt") as f:
            for line in f:
                (key, val, val_sqr) = line.split(", ")
                self.dictionary[int(key)] = float(val)
                self.dictionary_sqr[int(key)] = float(val_sqr) * k

    def evaluate(self, dice, up, cats, cat, score, opponent_states):
        v, new_cat, up = lib.fillScore(dice, up, cats, cat)

        self_mean = v + self.dictionary.get(lib.code(new_cat, up)) + score
        means = [s.score + self.dictionary.get(lib.code(s.cats, s.up)) for s in opponent_states]

        self_var = self.dictionary_sqr.get(lib.code(new_cat, up))
        variances = [self.dictionary_sqr.get(lib.code(s.cats, s.up)) for s in opponent_states]

        n = len(opponent_states)
        mean = n * self_mean - sum(means)
        var = sqrt(n * self_var + sum(variances))
        if var == 0:
            if mean > 0:
                return 1
            else:
                return 0
        win_rate = 1 - norm.cdf(0, mean, var)
        return win_rate


class OptimalSolitaireAgent(MultiPlayerAgent):
    def __init__(self):
        MultiPlayerAgent.__init__(self, "OptimalSolitaire")
        self.agent = solitaire.OptimalAgent()

    def evaluate(self, dice, up, cats, cat, score, opponent_states):
        return self.agent.evaluate(dice, up, cats, cat)
