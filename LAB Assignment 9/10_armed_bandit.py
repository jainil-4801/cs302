###Q-2)10 -armed bandit

import random
import numpy as np
import matplotlib.pyplot as plt


# --- Bandit ---
class Bandit(object):
  def __init__(self, N):
    self.N = N
    expRewards = np.array([10] * self.N)
    self.expRewards = expRewards

  def actions(self):
    result = []
    for i in range(0, self.N):
      result.append(i)
      return result

  def increment_reward(self):
    v = np.random.normal(0, 0.01, 10)
    self.expRewards = self.expRewards + v

  def reward(self, action):
    result = []
    n = random.gauss(0, 1)
    result = self.expRewards[action]
    return result
def eGreedy(myBandit, epsilon, max_iteration):
  # Initialization
    Q = [0]*myBandit.N
    count = [0]*myBandit.N
    epsilon = epsilon
    r = 0
    R = []
    R_avg = [0]*1
    max_iter = max_iteration
    # Incremental Implementation
    for iter in range(1,max_iter):
        if random.random() > epsilon:
            action = Q.index(max(Q)) # Exploit/ Greed
        else:
            action = random.choice(myBandit.actions()) # Explore
        r = myBandit.reward(action)
        myBandit.increment_reward()
        R.append(r)
        count[action] = count[action]+1
        Q[action] = Q[action]+(r - Q[action])/count[action]
        R_avg.append(R_avg[iter-1] + (r-R_avg[iter-1])/iter)

    return Q, R_avg, R
myBandit = Bandit(N=10)
Q,R_avg, R = eGreedy(myBandit, 0.2, 60000)

plt.plot(R_avg)
plt.xlabel("Number of iterations")
plt.ylabel("Rewards")

plt.show()
