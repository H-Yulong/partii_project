import lib


# Defines the Yahtzee gamestate for game simulations

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
    def start(self, keep=[]):
        if self.log:
            print("Start!")
            print("-----Round 0-----")
        self.roll(keep)

    # Rolls a dice with a keep
    def roll(self, kept):
        self.dice = lib.roll(kept)
        self.rolls = self.rolls - 1
        if self.log:
            print(kept, "kept;", "roll result", str(self.dice) + ";", self.rolls, "rolls left.")

    # Fill in a category, calculate the score obtained
    # Capable of printing game log
    def fill(self, cat):
        current_score, new_cat, up = lib.fillScore(self.dice, self.up, self.cats, cat)
        self.score += current_score
        self.cats = new_cat
        self.up = up
        self.dice = []
        self.rolls = 3

        if len(self.cats) == 13:
            self.gameover = True

        if self.log:
            print("Filled in category", cat, "with", current_score, "scores.")
            print("Current score", str(self.score) + ";", "Upper bonus", self.up)
            if len(self.cats) == 13:
                print("Gameover! Total score:", self.score)
            else:
                print("-----Round " + str(len(self.cats)) + "-----")

    # Prettyprint the gamestate
    def printAll(self):
        print("Categories & Up:", self.cats, self.up)
        print("Dice & Rolls:", self.dice, self.rolls)
        print("Score:", self.score)
