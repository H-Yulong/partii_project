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
