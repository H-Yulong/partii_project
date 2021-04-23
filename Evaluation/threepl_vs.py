import Agents.environment as env
import Agents.solitaire_agents as solitaire
import Agents.two_player_agents as twopl
import Agents.three_player_agents as threepl

# Set up agents
agent = solitaire.OptimalAgent()
agent2 = solitaire.OptimalAgent()
agent3 = solitaire.OptimalAgent()

# Initialize
episodes = 10

r1, r2, r3 = 1500, 1500, 1500
k = 16

log, log2, log3 = [], [], []

# Main loop
for i in range(episodes):
    s1 = env.GameState(cats=[], log=False)
    s2 = env.GameState(cats=[], log=False)
    s3 = env.GameState(cats=[], log=False)

