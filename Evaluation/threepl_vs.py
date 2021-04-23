import Agents.environment as env
import Agents.solitaire_agents as solitaire
import Agents.three_player_agents as threepl

EPISODES = 1000
K = 16


def update_elo(s1, s2, s3, r1, r2, r3):

    e12 = 1 / (1 + pow(10, (r2 - r1) / 400))
    e13 = 1 / (1 + pow(10, (r3 - r1) / 400))
    e21 = 1 / (1 + pow(10, (r1 - r2) / 400))
    e23 = 1 / (1 + pow(10, (r3 - r2) / 400))
    e31 = 1 / (1 + pow(10, (r1 - r3) / 400))
    e32 = 1 / (1 + pow(10, (r2 - r3) / 400))

    if s1 > s2:
        r1 += K * (1 - e12)
        r2 += K * (0 - e21)
    else:
        r1 += K * (0 - e12)
        r2 += K * (1 - e21)

    if s1 > s3:
        r1 += K * (1 - e13)
        r3 += K * (0 - e31)
    else:
        r1 += K * (0 - e13)
        r3 += K * (1 - e31)

    if s2 > s3:
        r2 += K * (1 - e23)
        r3 += K * (0 - e32)
    else:
        r2 += K * (0 - e23)
        r3 += K * (1 - e32)

    return r1, r2, r3


def main():
    # Set up agents
    agent = solitaire.OptimalAgent()
    agent2 = solitaire.OptimalAgent()
    agent3 = threepl.MostDangerousAgent()

    # Initialize
    r1, r2, r3 = 1500, 1500, 1500
    log, log2, log3 = [], [], []

    # Main loop
    for i in range(EPISODES):
        # Initial states
        s1 = env.GameState(cats=[], log=False)
        s2 = env.GameState(cats=[], log=False)
        s3 = env.GameState(cats=[], log=False)

        # Game simulation
        while not s3.gameover:
            while s1.rolls > 0:
                agent.move(s1)
            if not s1.gameover:
                agent.move(s1)

            while s2.rolls > 0:
                agent2.move(s2)
            if not s2.gameover:
                agent2.move(s2)

            while s3.rolls > 0:
                agent3.move(s3, s1, s2)
            if not s3.gameover:
                agent3.move(s3, s1, s2)

        # Process game results
        log.append(s1.score)
        log2.append(s2.score)
        log3.append(s3.score)

        r1, r2, r3 = update_elo(s1.score, s2.score, s3.score, r1, r2, r3)

        print(s1.score, s2.score, s3.score)
        print("Elo points:", r1, r2, r3)
        print()


main()
