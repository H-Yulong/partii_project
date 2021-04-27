import Agents.environment as env
import Agents.solitaire_agents as solitaire
import Agents.multiplayer_agents as multi

EPISODES = 1000
agents = [multi.MostDangerousAgent(), multi.NormalAgent(), multi.OptimalSolitaireAgent(), multi.OptimalSolitaireAgent()]
N = len(agents)


def main():
    # Initialize
    ranks = [0.0 for _ in range(N)]
    wins = [0.0 for _ in range(N)]
    logs = [[] for _ in range(N)]

    # Main loop
    for i in range(EPISODES):
        # Initial states
        states = [env.GameState(cats=[], log=False) for _ in range(N)]

        # Game simulation
        while not states[-1].gameover:
            for j in range(N):
                player_state = states.pop(j)
                while player_state.rolls > 0:
                    agents[j].move(player_state, states)
                if not player_state.gameover:
                    agents[j].move(player_state, states)
                states.insert(j, player_state)

        # Record game results: score and rank
        results = []
        for j in range(N):
            logs[j].append(states[j].score)
            results.append(states[j].score)

        sorted_results = list(results)
        sorted_results.sort()
        wins[results.index(sorted_results[0])] += 1
        for j in range(N):
            ranks[results.index(sorted_results[j])] += j + 1

        output_string = ""
        for j in range(N):
            output_string += agents[j].name + ":" + str(states[j].score) + " "
        print(output_string)

    for i in range(N):
        ranks[i] = ranks[i] / EPISODES
        wins[i] = wins[i] / EPISODES
    print(ranks)
    print(wins)


main()
