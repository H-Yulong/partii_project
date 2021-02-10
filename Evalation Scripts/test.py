import matplotlib.pyplot as plt

# The factorial function V
def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)


# Calculates the probability of getting a given roll V
def prRoll(arr):
    count = [0, 0, 0, 0, 0, 0]
    for i in arr:
        count[i - 1] = count[i - 1] + 1

    # 5/324 = (5!)/(6^5), for simplicity
    result = 5 / 324
    for i in count:
        result = result / fact(i)

    return result


def load():
    d = {"full": 0}
    with open("output.txt") as f:
        for line in f:
            (key, val) = line.split(", ")
            d[int(key)] = float(val)
    return d


def yahtzee(dice, up):
    if (dice[0] == dice[1]) and (dice[0] == dice[2]) and (dice[0] == dice[3]) and (dice[0] == dice[4]):
        return 50
    else:
        return 0


def ones(dice, up):
    count = 0
    for d in dice:
        if d == 1:
            count += 1
    if (up != 63) and (count + up >= 63):
        return count + 35
    else:
        return count


def twos(dice, up):
    count = 0
    for d in dice:
        if d == 2:
            count += 2
    if (up != 63) and (count + up >= 63):
        return count + 35
    else:
        return count


def threes(dice, up):
    count = 0
    for d in dice:
        if d == 3:
            count += 3
    if (up != 63) and (count + up >= 63):
        return count + 35
    else:
        return count


def fours(dice, up):
    count = 0
    for d in dice:
        if d == 4:
            count += 4
    if (up != 63) and (count + up >= 63):
        return count + 35
    else:
        return count


def fives(dice, up):
    count = 0
    for d in dice:
        if d == 5:
            count += 5
    if (up != 63) and (count + up >= 63):
        return count + 35
    else:
        return count


def sixes(dice, up):
    count = 0
    for d in dice:
        if d == 6:
            count += 6
    if (up != 63) and (count + up >= 63):
        return count + 35
    else:
        return count


def three_of_a_kind(dice, up):
    count = [0, 0, 0, 0, 0, 0]
    for d in dice:
        count[d - 1] += 1
    for c in count:
        if c >= 3:
            return sum(dice)
    return 0


def four_of_a_kind(dice, up):
    count = [0, 0, 0, 0, 0, 0]
    for d in dice:
        count[d - 1] += 1
    for c in count:
        if c >= 4:
            return sum(dice)
    return 0


def fullhouse(dice, up):
    count = [0, 0, 0, 0, 0, 0]
    for d in dice:
        count[d - 1] += 1
    if (2 in count) and (3 in count):
        return 25
    else:
        return 0


def small_straight(dice, up):
    if (1 in dice) and (2 in dice) and (3 in dice) and (4 in dice):
        return 30
    elif (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice):
        return 30
    elif (3 in dice) and (4 in dice) and (5 in dice) and (6 in dice):
        return 30
    else:
        return 0


def large_straight(dice, up):
    if (1 in dice) and (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice):
        return 40
    elif (2 in dice) and (3 in dice) and (4 in dice) and (5 in dice) and (6 in dice):
        return 40
    else:
        return 0


def chance(dice, up):
    return sum(dice)


def code(cats, up):
    if len(cats) == 13:
        return "full"
    result = 0
    for c in cats:
        result += pow(2, c + 1)
    result = result * 64 + up
    return result


# Generates all the possible dice-roll patterns for n dice with d faces (default 6)
# Returning a list of lists V
def dicePatterns(n, d=6):
    p = 0
    buffer = []
    terminate = []
    result = []

    for i in range(n):
        buffer.append(1)
        terminate.append(d)

    while buffer != terminate:
        result.append(list(buffer))

        if buffer[p] == d:
            while buffer[p] == d:
                p = p + 1
            buffer[p] = buffer[p] + 1
            while p != 0:
                p = p - 1
                buffer[p] = buffer[p + 1]
        else:
            buffer[p] = buffer[p] + 1

    result.append(terminate)

    # Trust me, it works. Check the cardinality for yourself.
    # print(len(result))

    return result


# Generates all possible outcomes of choosing r numbers from [0,1,2...n-1]
# Order doesn't matter V
def choosePatterns(n, r):
    p = 0
    buffer = []
    terminate = []
    result = []

    for i in range(r):
        buffer.append(r - i - 1)
        terminate.append(n - i - 1)

    while buffer != terminate:
        if 0 in buffer:
            alt = list(buffer)
            alt.remove(0)
            alt.append(-1)
            result.append(alt)
        result.append(list(buffer))

        if buffer[p] == n - 1:
            while buffer[p] + p == n - 1:
                p = p + 1
            buffer[p] = buffer[p] + 1
            while p != 0:
                p = p - 1
                buffer[p] = buffer[p + 1] + 1
        else:
            buffer[p] = buffer[p] + 1

    result.append(terminate)
    # Trust me, it works. Check the cardinality for yourself.
    # print(len(result))

    return result


def evaluate(dice, cat, up, cats, dictionary):
    # Initialization
    evals = [yahtzee, ones, twos, threes, fours, fives, sixes, three_of_a_kind,
             four_of_a_kind, fullhouse, small_straight, large_straight, chance]

    # First evaluation
    score = evals[cat](dice, up)

    if (cat == 0) and (score == 0):
        cat = -1

    # Handle upper bonus counter
    if (cat < 7) and (cat > 0) and (up < 63):
        up = up + score
        if up > 63:
            up = 63

    # Joker rule and Yahtzee bonus
    if yahtzee(dice, up) > 0:
        # In the case of Yahtzee is filled:
        if (0 in cats) or (-1 in cats):
            # If Yahtzee is filled with 50, get a bonus of 100.
            if 0 in cats:
                score += 100

            # Check Joker.
            # If the corresponding upper section is filled, Joker is allowed.
            if dice[0] in cats:
                # Check small straight, large straight, fullhouse.
                if cat == 9:
                    score += 25
                elif cat == 10:
                    score += 30
                elif cat == 11:
                    score += 40

    new_cat = list(cats)
    new_cat.append(cat)
    return score + dictionary.get(code(new_cat, up))


def extend(dice, d):
    result = list(dice)
    result.append(d)
    result.sort(reverse=True)
    return result


def subset(this, that):
    if len(this) > len(that):
        return False
    for t in this:
        if t not in that:
            return False
        else:
            that = remove(that, t)
    return True


def remove(dice, d):
    if d in dice:
        result = list(dice)
        result.remove(d)
        return result
    return False


def move(cats, up, dice, roll, dictionary):
    full = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    empty = list(full)
    for c in cats:
        if c == -1:
            empty.remove(0)
        elif c == 0:
            empty.remove(0)
        else:
            empty.remove(c)

    if roll == 0:
        max_cat = 0
        max_score = 0
        for e in empty:
            v = evaluate(dice, e, up, cats, dictionary)
            if v > max_score:
                max_cat = e
                max_score = v
        return  "Fill in category " + str(max_cat) + ", expected score " + str(max_score) + "."

    cache = [[[]], dicePatterns(1), dicePatterns(2), dicePatterns(3), dicePatterns(4), dicePatterns(5)]

    R3 = {}
    # Evaluate R3
    for d in cache[5]:
        max_exp = 0
        # max_cat = 0
        for e in empty:
            score = evaluate(d, e, up, cats, dictionary)
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
                new_d = extend(d, e)
                exp += K2[cache[k + 1].index(new_d) * 10 + k + 1]
            K2[cache[k].index(d) * 10 + k] = exp / 6

    if roll == 1:
        max_keep = []
        max_exp = 0.0
        for key, val in K2.items():
            d = cache[key % 10][key // 10]

            if subset(d, dice):
                if val > max_exp:
                    max_exp = val
                    max_keep = d
        if (subset(max_keep, dice)) and subset(dice, max_keep):
            return move(cats, up, dice, 0, dictionary)

        return "Keep " + str(max_keep) + "."

    R2 = {0: K2.get(0)}
    for k in range(1, 6):
        for d in cache[k]:
            max_exp = K2.get(cache[k].index(d) * 10 + k)
            for e in range(1, 7):
                r = remove(d, e)
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
                new_d = extend(d, e)
                exp += K1[cache[k + 1].index(new_d) * 10 + k + 1]
            K1[cache[k].index(d) * 10 + k] = exp / 6

    if roll == 2:
        max_keep = []
        max_exp = 0.0
        for key, val in K1.items():
            d = cache[key % 10][key // 10]

            if subset(d, dice):
                if val > max_exp:
                    max_exp = val
                    max_keep = d
        if (subset(max_keep, dice)) and subset(dice, max_keep):
            return move(cats, up, dice, 0, dictionary)

        return "Keep " + str(max_keep) + "."

    return "Invalid inputs."


def main():
    dictionary = load()
    cats = [2,7]
    up = 4
    dice = [4,4,5,5,6]
    roll = 0
    dice.sort(reverse=True)
    print(move(cats,up,dice,roll,dictionary))
    '''
    result = [0,0,0,0,0,0]
    for d in dicePatterns(5):
        pr = prRoll(d)
        v = ones(d,0)
        for i in range(6):
            if i <= v:
                result[i] += pr

    print(result)




    
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    exp = 254.5896095

    for d in dicePatterns(5):
        x = move(cats, up, d, 0, dictionary) - exp
        y = prRoll(d)

        if x in x1:
            y1[x1.index(x)] += y
        else:
            x1.append(x)
            y1.append(y)

    outx = list(x1)
    outx.sort()
    outy = []
    for x in outx:
        outy.append(y1[x1.index(x)])
    plt.plot(outx, outy)
    plt.show()
    '''


#main()
