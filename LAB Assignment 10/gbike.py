import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import math
from scipy.stats import poisson

matplotlib.use('Agg')

# maximum # of gbikes in each location
MAX_GBIKE = 20

MAX_MOVE_OF_GBIKE = 5

RENTAL_REQUEST_FIRST_LOC = 3

RENTAL_REQUEST_SECOND_LOC = 4

RETURNS_FIRST_LOC = 3

RETURNS_SECOND_LOC = 2

GAMMA = 0.9

RENTAL_CREDIT = 10

MOVE_GBIKE_COST = 2

# positive means first to second and negtaive means second to first 
actions = np.arange(-MAX_MOVE_OF_GBIKE, MAX_MOVE_OF_GBIKE + 1)

POISSON_UPPER_BOUND = 11 # upper bound to poisson distribution

value = np.zeros((MAX_GBIKE + 1, MAX_GBIKE + 1))
policy = np.zeros(value.shape, dtype=np.int)


# backup or caching the poisson value because it may use next iteration

pBackup = dict()

def poisson_dist(x, lam):
    global pBackup
    key = (x ,lam)
    if key not in pBackup.keys():
        pBackup[key] = poisson.pmf(x, lam)
    return pBackup[key]

def expected_return(state, action, state_value):
    # cost for moving bikes
    returns = float(-(MOVE_GBIKE_COST * abs(action)))

    # moving gbike
    NUM_OF_GBIKE_FIRST_LOC = int(max(min(state[0] - action, MAX_GBIKE),0))
    NUM_OF_GBIKE_SECOND_LOC = int(max(min(state[1] + action, MAX_GBIKE),0))

    # go through all possible rental requests
    for rental_request_first_loc in range(POISSON_UPPER_BOUND):
        for rental_request_second_loc in range(POISSON_UPPER_BOUND):
            # probability for current combination of rental requests
            prob = poisson_dist(rental_request_first_loc, RENTAL_REQUEST_FIRST_LOC) * poisson_dist(rental_request_second_loc, RENTAL_REQUEST_SECOND_LOC)

            # valid rental requests should be less than actual # of gbike
            valid_rental_first_loc = min(NUM_OF_GBIKE_FIRST_LOC, rental_request_first_loc)
            valid_rental_second_loc = min(NUM_OF_GBIKE_SECOND_LOC, rental_request_second_loc)

            # get credits for renting
            reward = (valid_rental_first_loc + valid_rental_second_loc) * RENTAL_CREDIT
            GBIKE_LOCATION_ONE = NUM_OF_GBIKE_FIRST_LOC - valid_rental_first_loc
            GBIKE_LOCATION_TWO = NUM_OF_GBIKE_SECOND_LOC - valid_rental_second_loc

            returned_location_one = RETURNS_FIRST_LOC
            returned_location_two = RETURNS_SECOND_LOC
            GBIKE_LOCATION_ONE = min(GBIKE_LOCATION_ONE + returned_location_one, MAX_GBIKE)
            GBIKE_LOCATION_TWO = min(GBIKE_LOCATION_TWO + returned_location_two, MAX_GBIKE)
            returns += prob * (reward + GAMMA * state_value[GBIKE_LOCATION_ONE, GBIKE_LOCATION_TWO])
        return returns

def policy_evaluation():
    global value
    while True:
        old_value = value.copy()
        for i in range(MAX_GBIKE + 1):
            for j in range(MAX_GBIKE + 1):
                new_state_value = expected_return([i, j], policy[i, j], value)
                value[i, j] = new_state_value
        max_value_change = abs(old_value - value).max()
        print('max value change {}'.format(max_value_change))
        if max_value_change < 1e-4:
            break

def policy_improvement():
    global policy
    policy_not_improvable = True
    for i in range(MAX_GBIKE + 1):
        for j in range(MAX_GBIKE + 1):
            old_action = policy[i, j]
            action_returns = []
            for action in actions:
                if (0 <= action <= i) or (-j <= action <= 0):
                    action_returns.append(expected_return([i, j], action, value))
                else:
                    action_returns.append(-np.inf)
            new_action = actions[np.argmax(action_returns)]
            policy[i, j] = new_action
            if policy_not_improvable and old_action != new_action:
                policy_not_improvable = False
    print('policy stable {}'.format(policy_not_improvable))

    return policy_not_improvable


def main():
    iterations = 0
    _, axes = plt.subplots(2, 3, figsize=(40, 20))
    plt.subplots_adjust(wspace=0.1, hspace=0.2)
    axes = axes.flatten()
    while True:
        fig = sns.heatmap(np.flipud(policy), cmap="YlGnBu", ax=axes[iterations])
        fig.set_ylabel('# gbike at first location', fontsize=30)
        fig.set_yticks(list(reversed(range(MAX_GBIKE + 1))))
        fig.set_xlabel('# gbike at second location', fontsize=30)
        fig.set_title('policy {}'.format(iterations), fontsize=30)

        # policy evaluation (in-place) No need to take other matrix for storing and saving 
        policy_evaluation()

        # policy improvement
        
        policy_not_improvable = policy_improvement()

        if policy_not_improvable:
            # we got the optimal policy as nothing can be improved now and 
            fig = sns.heatmap(np.flipud(value), cmap="YlGnBu", ax=axes[-1])
            fig.set_ylabel('# gbike at first location', fontsize=30)
            fig.set_yticks(list(reversed(range(MAX_GBIKE + 1))))
            fig.set_xlabel('# gbike at second location', fontsize=30)
            fig.set_title('optimal value', fontsize=30)
            break

        iterations += 1

    plt.savefig('figure_gbike.png')
    plt.close()

if __name__ == '__main__':
    main()