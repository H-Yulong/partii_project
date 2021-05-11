import Agents.environment as env
import Agents.multiplayer_agents as multi

# Initialize parameters and agents
EPISODES = 1000
normal = multi.NormalAgent()
agents = [normal, multi.OptimalSolitaireAgent(), normal, normal, normal]
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
        if not states[2].gameover:
            print("Wrong!")
            return

        # Record game results: score and rank
        results = []
        for j in range(N):
            logs[j].append(states[j].score)
            results.append(states[j].score)

        sorted_results = list(results)
        sorted_results.sort(reverse=True)
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

    # Save results
    file = open("../Experiment Data/5pl_data.txt", "w")
    for i in range(N):
        file.write(agents[i].name + "\n")
        file.write(str(logs[i]) + "\n")
    file.close()


main()
