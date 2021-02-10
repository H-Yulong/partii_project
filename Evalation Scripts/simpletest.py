import yahtzee_agent as y
import torch

agent = y.NNTwoPlayer("Data/two_player.pt")
states =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
states2 =  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
up = 0
up2 = 0
y_state = 0
y_state2 = 0
score = 0
score2 = 0
print(agent.model(torch.tensor(
            states + [up, y_state, score] + states2 + [up2, y_state2, score2],
            dtype=torch.float32)))