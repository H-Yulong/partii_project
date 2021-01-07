import matplotlib.pyplot as plt


def bonusProb(p, bonus):
    # p = 10a + b
    a = p // 10
    b = p % 10
    result = 0.0
    result += (b + 1) / 10 * (1 - pow((9 - a) / 10, bonus+1))
    result += (9 - b) / 10 * (1 - pow((10 - a) / 10, bonus+1))

    return result


def punishProb(p,punish):
    # p = 10a + b
    a = p // 10
    b = p % 10
    result = 0.0
    result += (b + 1) / 10 * pow(a / 10, punish + 1)
    result += (9 - b) / 10 * pow((a - 1) / 10, punish + 1)
    return result


x = [i for i in range(100)]
y1 = [punishProb(i,1) for i in range(100)]
y2 = [3 * i / 5 / 100 for i in range(100)]
#y3 = [3 * punishProb(i,2) for i in range(100)]
const = [1 for i in range(100)]
l1 = plt.plot(x,y1,label = "normal")
l2 = plt.plot(x,y2,label = "extreme")
#l3 = plt.plot(x,y3,label = "three shots")
plt.plot(x,const)
plt.legend()
plt.show()
