import random
import time
from math import sqrt, log

class Node:
	def __init__(self, state, p = None, m = None):
		self.parent = p
		self.children = []
		self.movelist = state.get_moves()
		self.unvisitedMoves = state.get_moves()
		self.score = 0.0
		self.visited = 0.0
		self.turn = state.get_whos_turn()
		self.move = m

	def AddChild(self, move, state):
		n = Node(state, self, move)
		self.children.append(n)
		self.unvisitedMoves.remove(move)
		return n

	def SelectChild(self):
		best_score = '-inf'
		if self.children == []:
			raise Exception('In SelectChild: self.children is empty')
		best_child = self.children[0]

		for c in self.children:
			#print "c.score: " + str(c.score) + " c.visited: " + str(c.visited) + " self.visited: " + str(self.visited)
			child_score = c.score/c.visited + .3 * sqrt(2*log(self.visited)/c.visited)
			if child_score > best_score:
				best_score = child_score
				best_child = c

		return best_child

	def Update(self, scorediff):
		self.visited += 1
		self.score += scorediff


def uctsearch(rootstate, rolloutDepth, timeMax = 1, verbose = False):
	t_start = time.time()
	t_now = t_start
	t_deadline = t_start + timeMax

	me = rootstate.get_whos_turn()
	you = 'red'
	if me == you:
		you = 'blue'

	iterations = 0

	rootnode = Node(rootstate)
	rootnode.visited += 1

	while t_now < t_deadline:
		iterations += 1
		node = rootnode
		state = rootstate

		#selection
		# if we've created all of our child nodes, choose one of them.
		# otherwise, stay at this node.
		while node.unvisitedMoves == [] and node.movelist != []:
			node = node.SelectChild()
			state.apply_move(node.move)


		# expansion
		# choose an unexplored move, and create a child node from it
		if node.unvisitedMoves != []:
			m = random.choice(node.unvisitedMoves)
			state.apply_move(m)
			node = node.AddChild(m, state)

		# simulation
		# run a simulation from the newly created child node
		while state.get_moves() != []:
			m = random.choice(state.get_moves())
			state.apply_move(m)


		#backpropagation
		# send the results of the simulation up the tree
		scores = state.get_score()
		"""simResult = scores[me] - scores[you]
		while node != None:
			node.Update(simResult)
			node = node.parent"""
		while node != None:
			if node.parent != None:
				if node.parent.turn == me:
					simResult = scores[me] - scores[you]
				else:
					simResult = scores[you] - scores[me]
				node.Update(simResult)
			node = node.parent





		t_now = time.time()

	sample_rate = float(iterations)/(t_now - t_start)
	print "%s samples per second" % (sample_rate)

	best_move = rootnode.children[0].move
	best_avg_score = float('-inf')

	for c in rootnode.children:
		if c.score/c.visited > best_avg_score:
			best_avg_score = c.score/c.visited
			best_move = c.move

	return best_move
