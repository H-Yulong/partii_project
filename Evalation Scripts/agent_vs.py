import yahtzee_agent as y
import matplotlib.pyplot as plt

episodes = 100

'''
agent = y.SingleBestAgent("Data/output.txt")
agent2 = agent2 = y.SingleNNAgent("Data/module.pt")
agent3 = y.SingleBlindAgent()
agent4 = y.SingleBestAgent("Data/esti_table.txt")
'''

agent = y.NNTwoPlayer("../Data/two_player3.pt", 32,32)
agent2 = y.SingleBlindAgent()
#agent2 = y.TableBasedTwoPlayer()
#agent2 = y.SingleBestAgent("../Data/output.txt")


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
            agent.move(s1,s2)
        if not s1.gameover:
            agent.move(s1,s2)

        while s2.rolls > 0:
            agent2.move(s2)
        if not s2.gameover:
            agent2.move(s2)
    if not s1.gameover:
        print("Wrong")
        s1.printAll()
        break
    #'''

    log.append(s1.score)
    log2.append(s2.score)
    print(s1.score, s2.score)
    if s1.score > s2.score:
        win += 1


print(log)
print(log2)
print(win)


