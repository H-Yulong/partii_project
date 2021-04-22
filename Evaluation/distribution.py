import yahtzee_agent as y
import matplotlib.pyplot as plt


def null_get(dic, key):
    if key in dic.keys():
        return dic[key]
    else:
        return 0


results = {}
episodes = 1000
total = 0
total_sqr = 0
data = []
agent = y.SingleBestAgent("../Data/output.txt")
#agent = y.SingleNNAgent("../Data/new_module5c.pt")

for i in range(episodes):
    state = y.GameState(cats=[2,6,9,10,11], log=False)
    while not state.gameover:
        while state.rolls > 0:
            agent.move(state)
        if not state.gameover:
            agent.move(state)
    score = state.score
    total += score
    total_sqr += score * score
    data.append(score)
    if score > 500:
        score = 500
    if score not in results.keys():
        results[score] = 1
    else:
        results[score] += 1
    print("Game no.", i, ":", score)

x = [i for i in range(500)]
y = [null_get(results, i) / episodes for i in x]

f = open("../Data/Soli/nn2.txt", "w")
f.write(str(data) + "\n")
f.write(str(total / episodes) + " ")
f.write(str(pow((total_sqr - total * total / episodes) / (episodes - 1), 0.5)))

plt.plot(x, y)
plt.show()
