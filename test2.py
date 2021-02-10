import yahtzee_agent as y
import lib


def generateGame():
    return [lib.roll([]) for _ in range(13)]


def main():
    # Params
    episodes = 100
    score = []
    score2 = []
    score3 = []

    # Agents
    agent = y.SingleNNAgent("Data/new_module4.pt")
    agent2 = y.SingleBlindAgent()
    agent3 = y.SingleBestAgent("Data/output.txt")

    # Dice generation
    initial_dice = generateGame()
    print(initial_dice)

    # Agents running
    for i in range(episodes):
        state = y.GameState(cats=[], log=False)
        round_no = 0
        while not state.gameover:
            if state.rolls == 3:
                state.roll(initial_dice[round_no])
                round_no += 1
            else:
                agent.move(state)
        score.append(state.score)

        state = y.GameState(cats=[], log=False)
        round_no = 0
        while not state.gameover:
            if state.rolls == 3:
                state.roll(initial_dice[round_no])
                round_no += 1
            else:
                agent2.move(state)
        score2.append(state.score)

        state = y.GameState(cats=[], log=False)
        round_no = 0
        while not state.gameover:
            if state.rolls == 3:
                state.roll(initial_dice[round_no])
                round_no += 1
            else:
                agent3.move(state)
        score3.append(state.score)

        print(i)

    print("NN: ", sum(score) / episodes)
    print("Blind: ", sum(score2) / episodes)
    print("Best: ", sum(score3) / episodes)

    print("NN Ratio: ", sum(score) / sum(score3) )
    print("Blind Ratio: ", sum(score2) / sum(score3))


main()
