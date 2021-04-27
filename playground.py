import lib
import Agents.environment as env
import Agents.solitaire_agents as solitaire

agent = solitaire.OptimalAgent()
#agent = y.SingleBlindAgent()

state1 = env.GameState(cats=[],log=True)

state1.roll([5, 5, 5, 6, 6])
agent.move(state1)





