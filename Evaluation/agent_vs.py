import yahtzee_agent as y
import matplotlib.pyplot as plt

episodes = 1000

'''
agent = y.SingleBestAgent("Data/output.txt")
agent2 = agent2 = y.SingleNNAgent("Data/module.pt")
agent3 = y.SingleBlindAgent()
agent4 = y.SingleBestAgent("Data/esti_table.txt")
'''

#agent2 = y.NNTwoPlayer("../Data/two_player_new.pt", 16,16)
#agent2 = y.MixedTwoPlayer()
agent2 = y.MixedTwoPlayer()
#agent2 = y.SingleBlindAgent()
#agent2 = y.NormalTwoPlayer()

#agent2 = y.SingleReallyBlindAgent()
#agent = y.SingleBlindAgent()
#agent2 = y.MixedTwoPlayer()
#agent2 = y.TableBasedTwoPlayer()
agent = y.SingleBestAgent("../Data/output.txt")

r1 = 1500
r2 = 1500

k = 16

log = []
log2 = []
win = 0

for i in range(episodes):
    s1 = y.GameState(cats=[], log=False)
    s2 = y.GameState(cats=[], log=False)

    #s1.roll([6, 6, 4, 3, 1])

    #'''
    while not s2.gameover:
        while s1.rolls > 0:
            agent.move(s1)
        if not s1.gameover:
            agent.move(s1)

        while s2.rolls > 0:
            agent2.move(s2, s1)
        if not s2.gameover:
            agent2.move(s2, s1)

    if not s1.gameover:
        print("Wrong")
        s1.printAll()
        break
    #'''

    log.append(s1.score)
    log2.append(s2.score)

    e1 = 1 / (1 + pow(10, (r2 - r1) / 400))
    e2 = 1 / (1 + pow(10, (r1 - r2) / 400))

    if s1.score > s2.score:
        win += 1
        r1 = r1 + k * (1 - e1)
        r2 = r2 + k * (0 - e2)
    else:
        r1 = r1 + k * (0 - e1)
        r2 = r2 + k * (1 - e2)

    print(s1.score, s2.score, "win rate:", win / (i + 1))
    print("Elo points:", r1, r2)
    print()

print(log)
print(log2)
print(win)
print(agent2.improve_count)
print(agent2.improve)


