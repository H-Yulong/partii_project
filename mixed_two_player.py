import random
import torch
import torch.nn as nn
import lib as util


def roll(kept):
    result = [0, 0, 0, 0, 0]
    length = len(kept)
    for i in range(length):
        result[i] = kept[i]
    for i in range(5 - length):
        result[length + i] = random.randint(1, 6)
    result.sort(reverse=True)
    return result


def input_format(states1, up1, y_state1, score1, states2, up2, y_state2, score2):
    return torch.tensor(states1 + [up1, y_state1, score1] + states2 + [up2, y_state2, score2], dtype=torch.float32)


def state_evaluate(dice, cat, up, state, y_state, score1, state2, up2, y_state2, score2, mode):
    # mode 0: play for higher expected result
    # mode 1: play for beating opponent

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

    return score


def main():
    input_size = 32
    hidden_size1 = 32
    hidden_size2 = 32
    output_size = 1
    l = 0.7
    g = 0.5
    a = 0.01
    episodes = 1000
    score_weight = 100

    m = nn.Sequential(nn.Linear(input_size, hidden_size1, False),
                      nn.Sigmoid(),
                      nn.Linear(hidden_size1, hidden_size2, False),
                      nn.Sigmoid(),
                      nn.Linear(hidden_size2, output_size, False),
                      nn.Sigmoid())

    cache = [[[]], util.dicePatterns(1), util.dicePatterns(2), util.dicePatterns(3), util.dicePatterns(4),
             util.dicePatterns(5)]
    full = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    for p in m.parameters():
        #p.data = torch.zeros_like(p)
        p.grad = torch.zeros_like(p)

    print("training...")

    for episode in range(episodes):
        # Clear the trace
        for p in m.parameters():
            p.grad = torch.zeros_like(p)

        # Initial state
        state = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        up = 0
        y_state = 0
        current_score = 0

        state2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        up2 = 0
        y_state2 = 0
        current_score2 = 0




main()