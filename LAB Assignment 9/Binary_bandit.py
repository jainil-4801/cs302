###Q-1)Binary bandit

import random
import matplotlib.pyplot as plt
def binaryBanditA(action):
    rand = random.random()
    p=[0.1, 0.2]
    if rand < p[action]:
        return 1
    return 0
def binaryBanditB(action):
    rand = random.random()
    p=[0.8, 0.9]
    if rand < p[action]:
        return 1
    return 0


class Bandit(object):
    def __init__(self, N):
        self.N = N

    def actions(self):
        result = []
        for i in range(self.N):
            result.append(i)
        return result


def egreedy(myBandit, epsilon, max_iteration):
    Q = [0] * myBandit.N
    count = [0] * myBandit.N
    epsilon = epsilon
    r = 0
    R = []
    R_avg = [0] * 1
    max_iter = max_iteration
    # Incremental Implementation
    for iter in range(1, max_iter):
        rew = None
        if random.random() > epsilon:
            action = Q.index(max(Q))  # Exploit/ Greed

        else:
            action = random.choice(myBandit.actions())  # Explore

        r = binaryBanditA(action)
        R.append(r)
        count[action] = count[action] + 1
        Q[action] = Q[action] + (r - Q[action]) / count[action]
        R_avg.append(R_avg[iter - 1] + (r - R_avg[iter - 1]) / iter)

    return Q, R_avg, R
bandit = Bandit(N=2)
Q, R_avg, R = egreedy(bandit, 0.1, 10000)

plt.plot(R_avg)
plt.xlabel("Number of iterations")
plt.ylabel("Rewards")

plt.show()
