import numpy as np


# The factorial function
def fact(n):
    if n == 0:
        return 1
    return n * fact(n - 1)


# Calculates the probability of getting a given roll
def prRoll(arr):
    count = [0, 0, 0, 0, 0, 0]
    for i in arr:
        count[i - 1] = count[i - 1] + 1

    # 5/324 = (5!)/(6^5), for simplicity
    result = 5 / 324
    for i in count:
        result = result / fact(i)

    return result


# Generates all the possible dice-roll patterns for n dice with d faces (default 6)
# Returning a list of lists
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
# Order doesn't matter
def choosePatterns(n, r):
    p = 0
    buffer = []
    terminate = []
    result = []

    for i in range(r):
        buffer.append(r - i - 1)
        terminate.append(n - i - 1)

    while buffer != terminate:
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
        result += pow(2, c)
    result = result * 100 + up
    return result


def evaluate(dice, cat, up, cats, dictionary):
    # Initialization
    evals = [yahtzee, ones, twos, threes, fours, fives, sixes, three_of_a_kind,
             four_of_a_kind, fullhouse, small_straight, large_straight, chance]

    # First evaluation
    score = evals[cat](dice, up)

    # Handle upper bonus counter
    if (cat < 7) and (cat > 0) and (up < 63):
        up = up + score
        if up > 63:
            up = 63

    # Joker rule and Yahtzee bonus
    if (0 in cats) and (yahtzee(dice, up) > 0):
        if dice[0] == cat:
            score += 100
        elif dice[0] not in cats:
            return 0
        else:
            score += 100
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


def remove(dice, d):
    if d in dice:
        result = list(dice)
        result.remove(d)
        return result
    return False


'''
 TODO: Everything so far are perfectly correct.
 You have successfully implemented R3.
 Now, implement K2. Then R2. Test them.
 K1 and R1 are exactly the same, so make sure K2 and R2 are correct.
 If possible, store that in some text/css file.
'''


def main():
    acc = 0
    pacc = 5242
    dictionary = {"full": 0}
    full = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    cache = [[[]], dicePatterns(1), dicePatterns(2), dicePatterns(3), dicePatterns(4), dicePatterns(5)]
    for i in range(12, -1, -1):
        states = choosePatterns(13, i)
        #if i < 12: return
        for cats in states:
            empty = list(full)
            for c in cats: empty.remove(c)

            for u in range(64):
                R3 = {}
                # Evaluate R3
                for d in cache[5]:
                    max_exp = 0
                    # max_cat = 0
                    for e in empty:
                        score = evaluate(d, e, u, cats, dictionary)
                        if score > max_exp:
                            max_exp = score
                            # max_cat = e
                    R3[cache[5].index(d)] = max_exp

                # Evaluate K2
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

                # Evaluate R2
                R2 = {0: K2.get(0)}
                for k in range(1, 6):
                    for d in cache[k]:
                        max_exp = K2.get(cache[k].index(d) * 10 + k)
                        for e in range(1, 7):
                            r = remove(d, e)
                            if r:
                                max_exp = max(max_exp, R2[cache[k - 1].index(r) * 10 + k - 1])
                        R2[cache[k].index(d)*10+k] = max_exp

                # Evaluate K1
                K1 = {}
                for d in cache[5]:
                    K1[cache[5].index(d) * 10 + 5] = R2[cache[5].index(d)*10+5]
                for k in range(4, -1, -1):
                    for d in cache[k]:
                        exp = 0
                        for e in range(1, 7):
                            new_d = extend(d, e)
                            exp += K1[cache[k + 1].index(new_d) * 10 + k + 1]
                        K1[cache[k].index(d) * 10 + k] = exp / 6

                # Evaluate R1
                R1 = {0: K1.get(0)}
                for k in range(1, 6):
                    for d in cache[k]:
                        max_exp = K1.get(cache[k].index(d) * 10 + k)
                        for e in range(1, 7):
                            r = remove(d, e)
                            if r:
                                max_exp = max(max_exp, R1[cache[k - 1].index(r) * 10 + k - 1])
                        R1[cache[k].index(d) * 10 + k] = max_exp

                # Evaluate expectation
                exp = 0
                for key in R1.keys():
                    if (key % 10 == 5):
                        exp += prRoll(cache[5][key // 10]) * K1.get(key)
                dictionary[code(cats,u)] = exp


                acc += 1
                '''
                for key in R1.keys():
                    print(cache[key % 10][key // 10], R1.get(key))
                # '''

                '''
                if acc >= 1:
                    return
                # '''

                print(acc)
                '''
                if acc >= pacc :
                    print(pacc / 5242,"% finished...")
                    pacc += 5242
                #'''

    print("done.", acc)


main()
