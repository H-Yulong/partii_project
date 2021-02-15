import lib
import yahtzee_agent as y

'''
Single Evaluator:
Calculate the expected lose of score due to sub-optimal move
'''


def evaluate(dice, up, cats, cat, dictionary):
    v, new_cat, up = lib.fillScore(dice, up, cats, cat)
    v += dictionary.get(lib.code(new_cat, up))
    return v


def case_evaluate(cats,up):
    # Params
    nn = y.SingleNNAgent("../Data/new_module4.pt")

    # Load dictionary
    dictionary = {"full": 0}
    with open("../Data/output.txt") as f:
        for line in f:
            (key, val) = line.split(", ")
            dictionary[int(key)] = float(val)

    print("Loading finished!")

    # Calculate R1 for the initial state
    cache = [[[]], lib.dicePatterns(1), lib.dicePatterns(2),
             lib.dicePatterns(3), lib.dicePatterns(4),
             lib.dicePatterns(5)]
    full = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    empty = list(full)
    for c in cats:
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
        # max_cat = 0
        for e in empty:
            score = evaluate(d, up, cats, e, dictionary)
            if score > max_exp:
                max_exp = score
                # max_cat = e
        R3[cache[5].index(d)] = max_exp

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

    print("R1 calculation finished!")

    # Calculate Mean-Choice-Error in the first turn

    blind = y.SingleBlindAgent()
    error = 0
    error2 = 0
    for dice in cache[5]:
        state = y.GameState(cats=cats, up=up, log=False)
        state2 = y.GameState(cats=cats, up=up, log=False)

        state.roll(dice)
        keep = nn.move(state)
        error += (R1[cache[5].index(dice) * 10 + 5] - K1[cache[len(keep)].index(keep) * 10 + len(keep)]) * lib.prRoll(dice)

        state2.roll(dice)
        keep2 = blind.move(state2)
        error2 += (R1[cache[5].index(dice) * 10 + 5] - K1[cache[len(keep2)].index(keep2) * 10 + len(keep2)]) * lib.prRoll(dice)

    print(cats,up)
    print("Errors: ", error, error2)
    return error, error2


def main():
    cats = lib.choosePatterns(13,1)
    nn_error = 0
    blind_error = 0
    deno = len(cats) * 30
    for cat in cats:
        for u in range(30):
            e1,e2 = case_evaluate(cat,u)
            nn_error += e1
            blind_error += e2
    nn_error = nn_error / deno
    blind_error = blind_error / deno

    print("Final errors: ", nn_error, blind_error)


main()
