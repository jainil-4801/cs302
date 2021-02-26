import math
import numpy as np
import matplotlib.pyplot as plt

class Coordinate:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	@staticmethod
	def get_distance(a, b):
		return np.sqrt((np.abs(a.x - b.x))**2 + (np.abs(a.y - b.y))**2)

	@staticmethod
	def get_total_distance(coords):
		dist = 0

		for first, second in zip(coords[: -1], coords[1:]):
			dist += Coordinate.get_distance(first, second)
		dist += Coordinate.get_distance(coords[0], coords[-1])

		return dist
	
	@staticmethod
	def get_changed_distance(coords,r1,r2):
		# Distance before swapping of r1 and r2

		n = len(coords)

		before_swapping = Coordinate.get_distance(coords[r1],coords[(r1-1)%n])+Coordinate.get_distance(coords[r1],coords[(r1+1)%n])+Coordinate.get_distance(coords[r2],coords[(r2+1)%n])+Coordinate.get_distance(coords[r2],coords[(r2-1)%n])

		after_swapping = Coordinate.get_distance(coords[r1],coords[(r2+1)%n])+Coordinate.get_distance(coords[r1],coords[(r2-1)%n])+Coordinate.get_distance(coords[r2],coords[(r1+1)%n])+Coordinate.get_distance(coords[r2],coords[(r1-1)%n])

		return before_swapping - after_swapping 




if __name__ == '__main__':

	coords = []

	with open('rajcoor26.txt') as f:
		data = f.readlines()
		total_data = data[5]

		print('Total Co-ordinates',total_data)

		index = 8
		while(True):	
			if data[index].startswith('EOF'):
				break	
			row = data[index].split()
			coords.append(Coordinate(int(row[1]),int(row[2])))
			index += 1
	
	fig = plt.figure(figsize=(10,5))
	ax1 = fig.add_subplot(121)
	ax2 = fig.add_subplot(122)

	for first, second in zip(coords[: -1], coords[1:]):
		ax1.plot([first.x, second.x], [first.y, second.y],'b')
	ax1.plot([coords[0].x, coords[-1].x],[coords[0].y, coords[-1].y],'b')

	for c in coords:
		ax1.plot(c.x,c.y,'ro')


	# simulated annealing algorithm 

	cost0 = Coordinate.get_total_distance(coords)
	cost11,cords = cost0,coords.copy()
	factor = 0.99
	cost0,coords,cnt,costp = cost11,cords.copy(),0,10**7
	T = 11
	T1 = T
	cor = []
	while True:
		T = T*factor 
		flag = False 
		for j in range(3000):
			# Excahnge two coordinates and get a neighbour 
			r1, r2 = np.random.randint(0, len(coords), size = 2)

			if abs(r1-r2) <=1 or (r1==0 and r2==len(coords)-1) or (r1==len(coords)-1 and r2==0):
				continue

			diff = Coordinate.get_changed_distance(coords,r1,r2)

			cost1 = cost0 - diff

			if cost1 < cost0:
				cost0 = cost1 
				coords[r1],coords[r2] = coords[r2], coords[r1]
			else:
				x = np.random.uniform()
				if x < np.exp((cost0-cost1)/T):
					cost0 = cost1
					coords[r1],coords[r2] = coords[r2], coords[r1]
		
		if abs(cost0 - costp) < 0.00001:
			cnt += 1
			if cnt>20 or cost0 < 235:
				break
		else:
			cnt = 0
		if costp > cost0:
			print(cost0)
			cor = coords.copy()
			costp = cost0


			
	print(f"Min cost at temperature {T1} is {cost0}")
	
	coords = cor.copy()

	# Plot the result 

	for first, second in zip(coords[: -1], coords[1:]):
		ax2.plot([first.x, second.x], [first.y, second.y],'b')
	ax2.plot([coords[0].x, coords[-1].x],[coords[0].y, coords[-1].y],'b')

	for c in coords:
		ax2.plot(c.x,c.y,'ro')

	plt.savefig("mygraph.png")


# [1]*10**10