import Agents.environment as env
import Agents.two_player_agents as twopl


# Initialize parameters and agents
episodes = 1
agent = twopl.OptimalSolitaireAgent()
agent2 = twopl.NNAgent("../Data/Neural Network/two_player_B.pt", 32, 32)
log = []
log2 = []
win = 0

# Runninng game simulations
for i in range(episodes):
    s1 = env.GameState(cats=[], log=True)
    s2 = env.GameState(cats=[], log=True)

    while not s2.gameover:
        while s1.rolls > 0:
            agent.move(s1,s2)
        if not s1.gameover:
            agent.move(s1,s2)

        while s2.rolls > 0:
            agent2.move(s2, s1)
        if not s2.gameover:
            agent2.move(s2, s1)

    log.append(s1.score)
    log2.append(s2.score)

    print(s1.score, s2.score, "win rate:", win / (i + 1))

print(log)
print(log2)
print(win)



