import sys 
from copy import deepcopy
from collections import defaultdict

sys.setrecursionlimit(10**7) 


intial_depth = 0
symbols = ['0','X']
possible_ans = [1,-1,0]

all_possible_stats = dict()

depth_d_nodes = defaultdict(int)
 
def evalaute_state(state):
	if (state[0][0] and state[1][1] and state[2][2]) and state[0][0] == state[1][1] == state[2][2]:
		return True 

	if (state[0][2] and state[1][1] and state[2][0]) and state[0][2] == state[1][1] == state[2][0]:
		return True

	for i in range(3):
		if (state[i][0] and state[i][1] and state[i][2]) and state[i][0] == state[i][1] == state[i][2]:
			return True 
	for i in range(3):
		if (state[0][i] and state[1][i] and state[2][i]) and state[0][i] == state[1][i] == state[2][i]:
			return True 

	return False

def give_me_hashable(state):
	l = []
	for i in range(3):
		for j in range(3):
			l.append(state[i][j])
	return tuple(l)

cnt = 0
total_visited_nodes = 0
def recursive_func(state,depth):
	global cnt, total_visited_nodes
	hashable_state = give_me_hashable(state)

	if hashable_state in all_possible_stats:
		return all_possible_stats[hashable_state]

	total_visited_nodes += 1
	if evalaute_state(state):
		all_possible_stats[hashable_state] = possible_ans[(depth%2)^1]
		return all_possible_stats[hashable_state]

	depth_d_nodes[depth-intial_depth] += 1
	flag = False
	get_winning_state = False
	all_possible_ans = []
	for i in range(3):
		for j in range(3):
			if state[i][j] == None:
				flag = True
				state[i][j] = symbols[depth%2]
				ans = recursive_func(deepcopy(state),depth+1)
				state[i][j] = None

				all_possible_ans.append(ans)

				if ans == possible_ans[depth%2]:
					cnt += 1
					get_winning_state = True
					break 
		if get_winning_state:
			break

	if not flag:
		# It indicates that there is no empty place in state and evalaute function also responded false --> Draw state
		all_possible_stats[hashable_state] = 0
	elif possible_ans[depth%2] in all_possible_ans:
		# If possible to win 
		all_possible_stats[hashable_state] = possible_ans[depth%2]
	elif possible_ans[-1] in all_possible_ans:
		# If couldn't win the game, try to draw
		all_possible_stats[hashable_state] = possible_ans[-1]
	else:
		# No chance --> loss 
		all_possible_stats[hashable_state] = possible_ans[(depth%2)^1]

	return all_possible_stats[hashable_state]



# inital_state = [[None for _ in range(3)]for _ in range(3)]

inital_state = []

for i in range(3):
	l = list(input())
	k = []
	for i in l:
		if i == ' ':
			k.append(None)
		else:
			k.append(i)
			intial_depth +=1
	inital_state.append(k)
ans = recursive_func(inital_state,intial_depth)

if ans == 0:
	print("If Match will be played optimally it should be Draw")
elif ans == -1:
	print("Match will be in favour of 'X'")
else:
	print("Match will be in favour of '0")

print(depth_d_nodes)
print(cnt)
print(total_visited_nodes)
# SAMPLE INPUT 

# 0X0
# 0 0
# X X 