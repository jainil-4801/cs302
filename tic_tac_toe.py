
from collections import defaultdict
from copy import deepcopy

def evalaute_state(state):
	if (state[0][0] and state[1][1] and state[2][2]) and state[0][0] == state[1][1] == state[2][2]:
		return True 

	if (states[0][2] and state[1][1] and state[2][0]) and states[0][2] == state[1][1] == state[2][0]:
		return True

	for i in range(3):
		if (state[i][0] and state[i][1] and state[i][2]) and state[i][0] == state[i][1] == state[i][2]:
			return True 
	for i in range(3):
		if (state[0][i] and state[1][i] and state[2][i]) and state[0][i] == state[1][i] == state[2][i]:
			return True 

	return False

mat = [[None for _ in range(3)]for _ in range(3)]

states = [mat]

symbol = '0'

d = defaultdict(int)

for depth in range(9):
	print(depth,len(states))
	new_states = []
	for state in states:
		if evalaute_state(state):
			d[symbol] += 1
			continue 
		for i in range(3):
			for j in range(3):
				if state[i][j] == None:
					new_state = deepcopy(state)
					new_state[i][j] = symbol
					new_states.append(new_state)
	states = deepcopy(new_states)
	if symbol == '0':
		symbol = 'X'
	else:
		symbol = '0'
print(d)
