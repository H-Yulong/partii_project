import yahtzee_agent as y
import matplotlib.pyplot as plt

agent = y.SingleBestAgent("Data/output.txt")

log = []

for i in range(100):
    s = y.GameState(cats=[-1], log=True)
    s.start()
    #s.roll([1,1,1,1,1])
    while not s.gameover:
        agent.move(s)
    log.append(s.score)

