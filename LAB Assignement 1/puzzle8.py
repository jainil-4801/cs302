# Solves a randomized 8-puzzle using A* algorithm with plug-in heuristics

import random
import math
from copy import deepcopy
import time
goal_state = [[1,2,3],
               [4,5,6],
               [7,8,0]]

def index(item, seq):
	ind = 0
	for state in seq:
		if state.adj_matrix == item.adj_matrix:
			return ind 
		ind += 1
	return -1

class GamePuzzle:

	def __init__(self):
		self.hval = 0
		self.depth = 0
		self.parent = None  
		self.adj_matrix = []

	def possible_moves(self):

		row,col = self.find(0)

		pos_states = []

		xy = [[-1,0],[0,-1],[1,0],[0,1]]

		for x,y in xy:
			if (row+x>-1 and row+x<3) and (col+y<3 and col+y>-1):
				pos_move = (row+x,col+y)

				state = deepcopy(self.adj_matrix)
				state[row][col],state[row+x][col+y] = state[row+x][col+y],state[row][col]
				x = GamePuzzle()
				x.adj_matrix = state
				x.parent = self
				x.depth = self.depth + 1
				pos_states.append(x)
		
		return pos_states

	def path(self):

		path_arr = []

		k = self

		while k.parent:
			path_arr.append(k.adj_matrix)
			k = k.parent
		return path_arr

	def solve(self, h):

		p_queue = [self]
		visited = []

		move_count = 0

		while len(p_queue) > 0:
			x = p_queue.pop(0)
			move_count += 1 

			if goal_state == x.adj_matrix:
				if len(visited) > 0:
					return x.path(),move_count
				else:
					return [x]

			succ = x.possible_moves()
			idx_open,idx_closed = -1,-1
			for move in succ:
				idx_open = index(move,p_queue)
				idx_closed = index(move,visited)
				hval = h(move)
				fval = hval + move.depth 

				if idx_closed == idx_open == -1:
					move.hval = hval 
					p_queue.append(move)
				elif idx_open > -1:
					copy = p_queue[idx_open]
					if fval < copy.hval + copy.depth:
						copy.hval = hval
						copy.parent = move.parent
						copy.depth = move.depth 
				elif idx_closed > -1:
					copy = visited[idx_closed]
					if fval < copy.hval + copy.depth:
						move.hval = hval 
						visited.remove(copy)
						p_queue.append(move)
			visited.append(x)
			p_queue = sorted(p_queue, key=lambda x:x.hval+x.depth)

		return [], 0

	def find(self, value):

		for row in range(3):
			for col in range(3):
				if self.adj_matrix[row][col] == value:
					return (row,col)



def manhattan(state):

	def find(value):
		for row in range(3):
			for col in range(3):
				if goal_state[row][col] == value:
					return (row,col)

	ans = 0
	for i in range(3):
		for j in range(3):
			x,y = find(state.adj_matrix[i][j])
			ans += abs(i-x)+abs(j-y)
	return ans 

def misplaced_tiles(state):

	ans = 0
	for i in range(3):
		for j in range(3):
			if goal_state[i][j] != state.adj_matrix[i][j]:
				ans +=1
	return ans 

if __name__ == "__main__":
    
    p = GamePuzzle()

    # p.adj_matrix = []
    p.adj_matrix = [[2,3,5],[4,7,6],[1,0,8]]

    # for _ in range(3):
    # 	l = list(map(int,input().split()))
    # 	p.adj_matrix.append(l)

    path,depth = p.solve(manhattan)
    path.reverse()

    print("Depth Required for Manhattan ",depth)

    for i in path:
    	print(i)


    path,depth = p.solve(not_at_correct_position)

    print("Depth Required for misplaced positions ",depth)
    path.reverse()

    for i in path:
    	print(i)


# Sample Output 
# Depth Required for Manhattan  90
# [[2, 3, 5], [4, 0, 6], [1, 7, 8]]
# [[2, 3, 5], [0, 4, 6], [1, 7, 8]]
# [[2, 3, 5], [1, 4, 6], [0, 7, 8]]
# [[2, 3, 5], [1, 4, 6], [7, 0, 8]]
# [[2, 3, 5], [1, 4, 6], [7, 8, 0]]
# [[2, 3, 5], [1, 4, 0], [7, 8, 6]]
# [[2, 3, 0], [1, 4, 5], [7, 8, 6]]
# [[2, 0, 3], [1, 4, 5], [7, 8, 6]]
# [[0, 2, 3], [1, 4, 5], [7, 8, 6]]
# [[1, 2, 3], [0, 4, 5], [7, 8, 6]]
# [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
# [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
# [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
# Depth Required for misplaced positions  155
# [[2, 3, 5], [4, 0, 6], [1, 7, 8]]
# [[2, 3, 5], [0, 4, 6], [1, 7, 8]]
# [[2, 3, 5], [1, 4, 6], [0, 7, 8]]
# [[2, 3, 5], [1, 4, 6], [7, 0, 8]]
# [[2, 3, 5], [1, 4, 6], [7, 8, 0]]
# [[2, 3, 5], [1, 4, 0], [7, 8, 6]]
# [[2, 3, 0], [1, 4, 5], [7, 8, 6]]
# [[2, 0, 3], [1, 4, 5], [7, 8, 6]]
# [[0, 2, 3], [1, 4, 5], [7, 8, 6]]
# [[1, 2, 3], [0, 4, 5], [7, 8, 6]]
# [[1, 2, 3], [4, 0, 5], [7, 8, 6]]
# [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
# [[1, 2, 3], [4, 5, 6], [7, 8, 0]]