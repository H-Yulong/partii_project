import lib
import yahtzee_agent as y

agent = y.SingleNNAgent("Data/new_module4.pt")
#agent = y.SingleReallyBlindAgent()
score = []

for i in range(1000):
    state = y.GameState(cats=[], log=False)
    while not state.gameover:
        agent.move(state)
    score.append(state.score)
    print(i)
print(score)
print(sum(score) / 1000, max(score), min(score))

f = open("nn_data.txt", "w")
f.write(str(score))

