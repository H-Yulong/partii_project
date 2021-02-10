import random
import torch
import torch.nn as nn
import test as util
import yahtzee_agent as y
import torch.nn.functional as F
import numpy


def roll(kept):
    result = [0, 0, 0, 0, 0]
    length = len(kept)
    for i in range(length):
        result[i] = kept[i]
    for i in range(5 - length):
        result[length + i] = random.randint(1, 6)
    result.sort(reverse=True)
    return result


def pre_format(cats):
    empty = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for c in cats:
        empty[c] = 1
    if -1 in cats:
        empty[0] = 1
    return empty


def input_format(states1, up1, y_state1, score1, states2, up2, y_state2, score2):
    return torch.tensor(states1 + [up1, y_state1, score1] + states2 + [up2, y_state2, score2], dtype=torch.float32)


def state_evaluate(dice, cat, up, state, y_state, score1, state2, up2, y_state2, score2, model):
    # Initialization
    evals = [util.yahtzee, util.ones, util.twos, util.threes, util.fours, util.fives, util.sixes, util.three_of_a_kind,
             util.four_of_a_kind, util.fullhouse, util.small_straight, util.large_straight, util.chance]

    # First evaluation
    score = evals[cat](dice, up)

    # Handle upper bonus counter
    if (cat < 7) and (cat > 0) and (up < 63):
        up = up + score
        if up > 63:
            up = 63

    # Joker rule and Yahtzee bonus
    if util.yahtzee(dice, up) > 0:
        # In the case of Yahtzee is filled:
        if (y_state == 1) or (y_state == -1):
            # If Yahtzee is filled with 50, get a bonus of 100.
            if y_state == 1:
                score += 100

            # Check Joker.
            # If the corresponding upper section is filled, Joker is allowed.
            if state[dice[0]] == 1:
                # Check small straight, large straight, fullhouse.
                if cat == 9:
                    score += 25
                elif cat == 10:
                    score += 30
                elif cat == 11:
                    score += 40

    next_state = list(state)
    next_state[cat] = 1
    next_y_state = 0
    if y_state != 0:
        next_y_state = y_state
    else:
        if cat == 0:
            if score > 0:
                next_y_state = 1
            else:
                next_y_state = 0

    if model:
        return model(input_format(next_state, up, next_y_state, score1 + score, state2, up2, y_state2, score2)).item()
    else:
        return score


def main():
    input_size = 32
    hidden_size1 = 32
    hidden_size2 = 32
    output_size = 1
    a = 0.01
    l = 0.7
    episodes = 1000

    cache = [[[]], util.dicePatterns(1), util.dicePatterns(2), util.dicePatterns(3), util.dicePatterns(4),
             util.dicePatterns(5)]
    full = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    '''
    State encoding:
        13 values for 13 categories, filled = 1, unfilled = 0.
        1 value for upper section score.
        1 value for yahtzee status: unfilled = 0, obtained = 1, unobtained = -1.
        initial_state = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        Lowest possible score: 5
        Highest possible score: 1575
    '''

    m = nn.Sequential(nn.Linear(input_size, hidden_size1, False),
                      nn.Sigmoid(),
                      nn.Linear(hidden_size1, hidden_size2, False),
                      nn.Sigmoid(),
                      nn.Linear(hidden_size2, output_size, False),
                      nn.Sigmoid())

    for p in m.parameters():
        # p.data = torch.zeros_like(p)
        p.grad = torch.zeros_like(p)

    print("training...")

    opti = y.SingleBestAgent("Data/output.txt")

    for episode in range(episodes):
        # Clear the trace
        for p in m.parameters():
            p.grad = torch.zeros_like(p)

        # Initial state
        opti_state = y.GameState(cats=[], log=False)
        opti_y = 0

        state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        up = 0
        y_state = 0
        current_score = 0

        for round_id in range(13):
            # Let the optimal agent move
            while opti_state.rolls > 0:
                opti.move(opti_state)
            if not opti_state.gameover:
                opti.move(opti_state)

            if -1 in opti_state.cats:
                opti_y = -1
            elif 0 in opti_state.cats:
                opti_y = 1

            # Compute R3,K2,R2,K1
            empty = list(full)
            for i in range(13):
                if state[i] == 1:
                    empty.remove(i)

            R3 = {}
            for d in cache[5]:
                max_exp = 0
                for e in empty:
                    score = state_evaluate(d, e, up, state, y_state, current_score, pre_format(opti_state.cats),
                                           opti_state.up, opti_y,
                                           opti_state.score, m)
                    if score > max_exp:
                        max_exp = score
                R3[cache[5].index(d)] = max_exp

            K2 = {}
            for d in cache[5]:
                K2[cache[5].index(d) * 10 + 5] = R3[cache[5].index(d)]
            for k in range(4, -1, -1):
                for d in cache[k]:
                    exp = 0
                    for e in range(1, 7):
                        new_d = util.extend(d, e)
                        exp += K2[cache[k + 1].index(new_d) * 10 + k + 1]
                    K2[cache[k].index(d) * 10 + k] = exp / 6

            R2 = {0: K2.get(0)}
            for k in range(1, 6):
                for d in cache[k]:
                    max_exp = K2.get(cache[k].index(d) * 10 + k)
                    for e in range(1, 7):
                        r = util.remove(d, e)
                        if r or (r == []):
                            max_exp = max(max_exp, R2[cache[k - 1].index(r) * 10 + k - 1])
                    R2[cache[k].index(d) * 10 + k] = max_exp

            K1 = {}
            for d in cache[5]:
                K1[cache[5].index(d) * 10 + 5] = R2[cache[5].index(d) * 10 + 5]
            for k in range(4, -1, -1):
                for d in cache[k]:
                    exp = 0
                    for e in range(1, 7):
                        new_d = util.extend(d, e)
                        exp += K1[cache[k + 1].index(new_d) * 10 + k + 1]
                    K1[cache[k].index(d) * 10 + k] = exp / 6

            # 1st Roll
            dice = roll([])
            max_keep = []
            max_exp = 0.0
            for key, val in K1.items():
                d = cache[key % 10][key // 10]

                if util.subset(d, dice):
                    if val > max_exp:
                        max_exp = val
                        max_keep = d

            # 2nd Roll
            dice = roll(max_keep)
            max_keep = []
            max_exp = 0.0
            for key, val in K2.items():
                d = cache[key % 10][key // 10]

                if util.subset(d, dice):
                    if val > max_exp:
                        max_exp = val
                        max_keep = d

            # 3rd Roll
            dice = roll(max_keep)
            max_cat = empty[0]
            max_exp = 0
            for e in empty:
                v = state_evaluate(dice, e, up, state, y_state, current_score, pre_format(opti_state.cats),
                                   opti_state.up, opti_y,
                                   opti_state.score, m)
                if v > max_exp:
                    max_exp = v
                    max_cat = e

            # Work out next state
            next_state = list(state)
            next_state[max_cat] = 1
            next_up = up
            next_ystate = y_state
            if (up < 63) and (max_cat >= 1) and (max_cat <= 6):
                for d in dice:
                    if d == max_cat:
                        next_up += max_cat
                if next_up > 63:
                    next_up = 63

            if max_cat == 0:
                if util.yahtzee(dice, 0) > 0:
                    next_ystate = 1
                else:
                    next_ystate = -1

            next_score = current_score + state_evaluate(dice, max_cat, up, state, y_state, current_score,
                                                        pre_format(opti_state.cats), opti_state.up, opti_y,
                                                        opti_state.score, None)

            # Do the TD-Lambda thing
            with torch.no_grad():
                for p in m.parameters():
                    p.grad *= l

            out = m(input_format(state, up, y_state, current_score, pre_format(opti_state.cats), opti_state.up, opti_y,
                                 opti_state.score))
            out.backward()
            with torch.no_grad():
                reward = (next_score - opti_state.score) / 1575
                delta = reward + m(
                    input_format(next_state, next_up, next_ystate, next_score, pre_format(opti_state.cats),
                                 opti_state.up, opti_y, opti_state.score)) - out

                for p in m.parameters():
                    p += a * delta * p.grad

            state = next_state
            up = next_up
            y_state = next_ystate
            current_score = next_score

        print(episode, " / ", episodes)
        print(m(input_format([0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0], 0, 0, 67,
                             [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0], 0, 0, 100)))
        print(m(input_format([0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0], 0, 0, 100,
                             [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0], 0, 0, 67)))

    torch.save(m.state_dict(), "Data/two_player3.pt")


main()
