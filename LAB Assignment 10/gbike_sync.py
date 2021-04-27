import numpy as np
import matplotlib.pyplot as plt
import math
import tqdm
from functools import partial
import time
import itertools
import seaborn as sbn

MAX_GBIKE = 20
MAX_MOVE = 5
MOVE_COST = -2
ADDITIONAL_PARK_COST = -4

RENT_REWARD = 10
RENTAL_EXPEC_FIRST_LOC = 3
RENTAL_EXPEC_SECOND_LOC = 4
RETURNS_FIRST_LOC = 3
RETURNS_SECOND_LOC = 2

pBackup = {}
def poisson(x, lam):
    global pBackup
    key = (x ,lam)
    if key not in pBackup.keys():
        pBackup[key] = np.exp(-lam) * pow(lam, x) / math.factorial(x)
    return pBackup[key]

states = []
for i in range(MAX_GBIKE + 1):
    for j in range(MAX_GBIKE + 1):
        states.append([i, j])


class PolicyIteration:
    def __init__(self, truncate, delta=1e-1, gamma=0.9):
        self.TRUNCATE = truncate
        self.actions = np.arange(-MAX_MOVE, MAX_MOVE + 1)
        self.inverse_actions = {el: ind[0] for ind, el in np.ndenumerate(self.actions)}
        self.values = np.zeros((MAX_GBIKE + 1, MAX_GBIKE + 1))
        self.policy = np.zeros(self.values.shape, dtype=np.int)
        self.delta = delta
        self.gamma = gamma

    def solve(self):
        iterations = 0
        while True:
            self.values = self.policy_evaluation(self.values, self.policy)
            
            policy_change, self.policy = self.policy_improvement(self.actions, self.values, self.policy)
            # no more policy change possible 
            if policy_change == 0:
                break
            iterations += 1
       

    # out-place
    def policy_evaluation(self, values, policy):

        global MAX_GBIKE
        while True:
            new_values = np.copy(values)
            k = np.arange(MAX_GBIKE + 1)
            # cartesian product
            all_states = ((i, j) for i, j in itertools.product(k, k))

            results = []
            cook = partial(self.expected_return_pe, policy, values)
            results = map(cook, all_states)

            for v, i, j in results:
                new_values[i, j] = v

            difference = np.abs(new_values - values).sum()
            print(f'Difference: {difference}')
            values = new_values
            if difference < self.delta:
                print(f'Values are converged!')
                return values

    def policy_improvement(self, actions, values, policy):
        new_policy = np.copy(policy)

        expected_action_returns = np.zeros((MAX_GBIKE + 1, MAX_GBIKE + 1, np.size(actions)))
        cooks = dict()
        for action in actions:
            k = np.arange(MAX_GBIKE + 1)
            all_states = ((i, j) for i, j in itertools.product(k, k))
            cooks[action] = partial(self.expected_return_pi, values, action)
            results = map(cooks[action], all_states)
            for v, i, j, a in results:
                expected_action_returns[i, j, self.inverse_actions[a]] = v
        
        for i,j in states:
            new_policy[i, j] = actions[np.argmax(expected_action_returns[i, j])]

        policy_change = (new_policy != policy).sum()
        return policy_change, new_policy

    # O(n^4) computation for all possible requests and returns
    def bellman(self, values, action, state):
        expected_return = 0
        if self.solve_extension:
            if action > 0:
                # Free bus to the second location
                expected_return += MOVE_COST * (action - 1)
            else:
                expected_return += MOVE_COST * abs(action)
        else:
            expected_return += MOVE_COST * abs(action)

        for req1 in range(0, self.TRUNCATE):
            for req2 in range(0, self.TRUNCATE):
                # moving gbikes
                gbike_location_one = max(int(min(state[0] - action, MAX_GBIKE)),0)
                gbike_location_two = max(int(min(state[1] + action, MAX_GBIKE)),0)

                # valid rental requests should be less than actual # of 
                real_rental_first_loc = min(gbike_location_one, req1)
                real_rental_second_loc = min(gbike_location_two, req2)

                # get credits for renting
                reward = (real_rental_first_loc + real_rental_second_loc) * RENT_REWARD

                if self.solve_extension:
                    if gbike_location_one >= 10:
                        reward += ADDITIONAL_PARK_COST
                    if gbike_location_two >= 10:
                        reward += ADDITIONAL_PARK_COST

                gbike_location_one -= real_rental_first_loc
                gbike_location_two -= real_rental_second_loc

                # probability for current combination of rental requests
                prob = poisson(req1, RENTAL_EXPEC_FIRST_LOC) * poisson(req2, RENTAL_EXPEC_SECOND_LOC)
                for ret1 in range(0, self.TRUNCATE):
                    for ret2 in range(0, self.TRUNCATE):
                        gbike_first_loc = min(gbike_location_one + ret1, MAX_GBIKE)
                        gbike_second_loc = min(gbike_location_two + ret2, MAX_GBIKE)
                        prob_ = poisson(ret1, RETURNS_FIRST_LOC) * poisson(ret2, RETURNS_SECOND_LOC) * prob
                        expected_return += prob_ * (reward + self.gamma * values[gbike_first_loc, gbike_second_loc])
        return expected_return

    # Expected return calculator for Policy Evaluation
    def expected_return_pe(self, policy, values, state):

        action = policy[state[0], state[1]]
        expected_return = self.bellman(values, action, state)
        return expected_return, state[0], state[1]

    # Expected return calculator for Policy Improvement
    def expected_return_pi(self, values, action, state):

        if ((action >= 0 and state[0] >= action) or (action < 0 and state[1] >= abs(action))) == False:
            return -float('inf'), state[0], state[1], action
        expected_return = self.bellman(values, action, state)
        return expected_return, state[0], state[1], action

    def plot(self):
        print(self.policy)
        fig = sbn.heatmap(np.flipud(policy), ax=axes[-1], cmap="YlGnBu")
        fig.figure()
        fig.xlim(0, MAX_GBIKE + 1)
        fig.ylim(0, MAX_GBIKE + 1)
        fig.savefig('plot_gbike_sync.png')
        fig.close()


if __name__ == '__main__':
    TRUNCATE = 9
    solver = PolicyIteration(TRUNCATE, delta=1e-1, gamma=0.9)
    solver.solve()
    solver.plot()