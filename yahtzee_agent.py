import lib


class GameState:
    def __init__(self, cats=None, up=0, dice=None, rolls=3, score=0, log=False):
        if cats is None:
            cats = []
        if dice is None:
            dice = []

        self.cats = cats
        self.up = up
        self.dice = dice
        self.rolls = rolls
        self.score = score
        self.log = log
        self.gameover = (len(cats) == 13)

    # Generates the first roll
    def start(self):
        if self.log:
            print("Start!")
            print("-----Round 0-----")
        self.roll([])

    # Rolls a dice with a keep
    def roll(self, kept):
        self.dice = lib.roll(kept)
        self.rolls = self.rolls - 1
        if self.log:
            print(kept, "kept;", "roll result", str(self.dice) + ";", self.rolls, "rolls left.")

    # Fill in a category, calculate the score obtained
    def fill(self, cat):
        current_score, new_cat, up = lib.fillScore(self.dice, self.up, self.cats, cat)
        self.score += current_score
        self.cats = new_cat
        self.up = up
        self.dice = []
        self.rolls = 3

        if self.log:
            print("Filled in category", cat, "with", current_score, "scores.")
            print("Current score", str(self.score) + ";", "Upper bonus", self.up)
            if len(self.cats) == 13:
                print("Gameover! Total score:", self.score)
                self.gameover = True
            else:
                print("-----Round " + str(len(self.cats)) + "-----")

    def printAll(self):
        print("Categories & Up:", self.cats, self.up)
        print("Dice & Rolls:", self.dice, self.rolls)
        print("Score:", self.score)


class YahtzeeAgent:
    def __init__(self, name):
        self.name = name
        return

    def move(self, state):
        return


class SingleBestAgent(YahtzeeAgent):

    def __init__(self, path):
        YahtzeeAgent.__init__(self, "SingleBest")
        self.dictionary = {"full": 0}
        with open(path) as f:
            for line in f:
                (key, val) = line.split(", ")
                self.dictionary[int(key)] = float(val)

        self.cache = [[[]], lib.dicePatterns(1), lib.dicePatterns(2),
                      lib.dicePatterns(3), lib.dicePatterns(4),
                      lib.dicePatterns(5)]

    def evaluate(self, dice, up, cats, cat):
        v, new_cat, up = lib.fillScore(dice, up, cats, cat)
        v += self.dictionary.get(lib.code(new_cat, up))
        return v

    def move(self, state):
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
            max_cat = 0
            max_score = 0
            for e in empty:
                v = self.evaluate(state.dice, state.up, state.cats, e)
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
                score = self.evaluate(d, state.up, state.cats, e)
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

                if lib.subset(d, state.dice):
                    if val > max_exp:
                        max_exp = val
                        max_keep = d
            if (lib.subset(max_keep, state.dice)) and lib.subset(state.dice, max_keep):
                state.rolls = 0
                self.move(state)
            else:
                state.roll(max_keep)

            return

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
                self.move(state)
            else:
                state.roll(max_keep)

            return

        raise Exception("Invalid roll number: greater than 2")
