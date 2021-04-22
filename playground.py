import lib
import yahtzee_agent as y

agent = y.SingleNNAgent("Data/new_module4.pt")
#agent = y.SingleBlindAgent()

state1 = y.GameState(cats=[],log=True)

while not state1.gameover:
    while state1.rolls > 0:
        agent.move(state1)
    if not state1.gameover:
        agent.move(state1)




