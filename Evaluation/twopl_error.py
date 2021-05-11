import Agents.environment as env
import Agents.two_player_agents as twopl
import Agents.solitaire_agents as soli
import lib

cache = [[[]], lib.dicePatterns(1), lib.dicePatterns(2),
         lib.dicePatterns(3), lib.dicePatterns(4),
         lib.dicePatterns(5)]
full = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Function that generates gamestates of Yahtzee late games
def generate_game(agent, empty):
    turns = 26 - empty
    s1 = env.GameState(cats=[], log=False)
    s2 = env.GameState(cats=[], log=False)
    while turns > 0:

        while s1.rolls > 0:
            agent.move(s1)
        if not s1.gameover:
            agent.move(s1)

        turns = turns - 1
        if turns == 0:
            break

        while s2.rolls > 0:
            agent.move(s2)
        if not s2.gameover:
            agent.move(s2)

        turns = turns - 1

    return s1, s2


# Functions that recursively calculate the relative error
def base_eval(dice, up, cats, cat, score, score2, empty_initial):
    odd = empty_initial % 2 != 0
    v, new_cat, up = lib.fillScore(dice, up, cats, cat)
    if v + score2 > score:
        if odd:
            return 1
        else:
            return 0
    else:
        if odd:
            return 0
        else:
            return 1



def even_eval(dice, up, cats, cat, score, state2, agent, empty_cats, empty_initial):
    v, new_cat, up = lib.fillScore(dice, up, cats, cat)
    state = env.GameState(cats=new_cat, up=up, rolls=2, score=score + v)
    return eval_error(agent, state, state2, empty_cats - 1, empty_initial)


def odd_eval(dice, state1, up, cats, cat, score, agent, empty_cats, empty_initial):
    v, new_cat, up = lib.fillScore(dice, up, cats, cat)
    state = env.GameState(cats=new_cat, up=up, rolls=2, score=score + v)
    return eval_error(agent, state1, state, empty_cats - 1, empty_initial)


# Returns the expected error at state config s1,s2
# If auto-win or auto-lose, expected error should be 0
# Because all moves result in the same outcome: no error would ever occur.
def eval_error(agent, s1, s2, empty_cats, empty_initial):
    empty = list(full)
    for c in s2.cats:
        if c == -1:
            empty.remove(0)
        elif c == 0:
            empty.remove(0)
        else:
            empty.remove(c)

    R3 = {}
    # Evaluate R3
    for d in cache[5]:
        max_exp = 0
        for e in empty:
            score = 0
            if empty_cats == 1:
                # Case1: auto win
                if s2.score > s1.score:
                    return 0
                score = base_eval(d, s1.up, s1.cats, e, s1.score, s2.score, empty_initial)
            elif empty_cats % 2 == 0:
                score = even_eval(d, s1.up, s1.cats, e, s1.score, s2, agent, empty_cats, empty_initial)
            else:
                score = odd_eval(d, s1, s2.up, s2.cats, e, s2.score, agent, empty_cats, empty_initial)
            if score > max_exp:
                max_exp = score
                # max_cat = e
        R3[cache[5].index(d)] = max_exp

    # Case 2: auto lose
    found = False
    for v in R3.values():
        if v > 0:
            found = True
    if not found:
        return 0

    # Evaluate the rest: K2, R2...
    K2 = {}
    for d in cache[5]:
        K2[cache[5].index(d) * 10 + 5] = R3[cache[5].index(d)]
    for k in range(4, -1, -1):
        for d in cache[k]:
            exp = 0
            for e in range(1, 7):
                new_d = lib.extend(d, e)
                exp += K2[cache[k + 1].index(new_d) * 10 + k + 1]
            K2[cache[k].index(d) * 10 + k] = exp / 6

    R2 = {0: K2.get(0)}
    for k in range(1, 6):
        for d in cache[k]:
            max_exp = K2.get(cache[k].index(d) * 10 + k)
            for e in range(1, 7):
                r = lib.remove(d, e)
                if r or (r == []):
                    max_exp = max(max_exp, R2[cache[k - 1].index(r) * 10 + k - 1])
            R2[cache[k].index(d) * 10 + k] = max_exp

    # Evaluate K1
    K1 = {}
    for d in cache[5]:
        K1[cache[5].index(d) * 10 + 5] = R2[cache[5].index(d) * 10 + 5]
    for k in range(4, -1, -1):
        for d in cache[k]:
            exp = 0
            for e in range(1, 7):
                new_d = lib.extend(d, e)
                exp += K1[cache[k + 1].index(new_d) * 10 + k + 1]
            K1[cache[k].index(d) * 10 + k] = exp / 6

    R1 = {0: K1.get(0)}
    for k in range(1, 6):
        for d in cache[k]:
            max_exp = K1.get(cache[k].index(d) * 10 + k)
            for e in range(1, 7):
                r = lib.remove(d, e)
                if r or (r == []):
                    max_exp = max(max_exp, R1[cache[k - 1].index(r) * 10 + k - 1])
            R1[cache[k].index(d) * 10 + k] = max_exp

    error = 0

    if empty_cats < empty_initial:
        for dice in cache[5]:
            error += R1[cache[5].index(dice) * 10 + 5] * lib.prRoll(dice)
        return error

    if empty_cats % 2 == 0:
        for dice in cache[5]:
            state = env.GameState(cats=s1.cats, up=s1.up, dice=dice, rolls=2, score=s1.score)
            # keep = agent.move(state)
            keep = agent.move(state, s2)
            error += (R1[cache[5].index(dice) * 10 + 5] - K1[
                cache[len(keep)].index(keep) * 10 + len(keep)]) * lib.prRoll(
                dice)
    else:
        for dice in cache[5]:
            state = env.GameState(cats=s2.cats, up=s2.up, dice=dice, rolls=2, score=s2.score)
            # keep = agent.move(state)
            keep = agent.move(state, s1)
            error += (R1[cache[5].index(dice) * 10 + 5] - K1[
                cache[len(keep)].index(keep) * 10 + len(keep)]) * lib.prRoll(
                dice)
    # print(dice, R1[cache[5].index(dice) * 10 + 5], keep, K1[cache[len(keep)].index(keep) * 10 + len(keep)])

    return error


def main():
    # Initialize agnets
    agent_gen = soli.OptimalAgent()
    agent_eval = twopl.TwoPolicyAgent()
    empty_cats = 1
    episodes = 20
    data = []
    for i in range(episodes):
        print("Generating NO.", i)
        s1, s2 = generate_game(agent_gen, empty_cats)
        print("Calculating NO.", i)
        data.append(eval_error(agent_eval, s1, s2, empty_cats, empty_cats))

    print(data)
    print("Average error:", sum(data) / episodes)
    f = open("../Data/Error 3 step/NN3bError.txt", "w")
    f.write(str(data) + "\n")
    f.write(str(sum(data) / episodes))


main()
