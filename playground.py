import lib
import Agents.environment as env
import Agents.solitaire_agents as solitaire

f = open("Experiment Data/3pl_data2.txt")

wins = [0,0,0]
data = [[],[],[]]

for i in range(3):
    f.readline()
    string = f.readline()
    string = string[1:-2]
    result = string.split(", ")
    for j in range(len(result)):
        result[j] = int(result[j])
    data[i] = result

for i in range(len(data[0])):
    maxi = max(data[0][i], data[1][i], data[2][i])
    if data[0][i] == maxi:
        wins[0] += 1
    elif data[1][i] == maxi:
        wins[1] += 1
    else:
        wins[2] += 1

for i in range(3):
    wins[i] = wins[i] / 1000

print(wins)




