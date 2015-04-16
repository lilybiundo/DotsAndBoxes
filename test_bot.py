import random
import time
from math import sqrt, log



class Node:
	def __init__(self, state, p = None, m = None):
		self.parent = p
		self.children = []
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
		def ucb(c):
			return c.score/c.visited + 10 * sqrt(2*log(self.visited)/c.visited)
		return max(self.children,key=ucb)

	def Update(self, scorediff):
		self.visited += 1
		self.score += scorediff

	def dump(self):
		summary = {
				'children': {str(c.move): c.dump() for c in self.children},
				'score': self.score,
				'visited': self.visited,
				'turn': self.turn,
				'um': self.unvisitedMoves,
		}
		return summary

#import yaml

def uctsearch(rootstate, rolloutDepth = int('inf'), timeMax = 1, verbose = False):
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
	
	debugStr = "SimResults: "

	while t_now < t_deadline:
		iterations += 1
		debugStr += "(I: " + str(iterations)
		node = rootnode
		state = rootstate.copy()
		#print ""

		#selection
		# if we've created all of our child nodes, choose one of them.
		# otherwise, stay at this node.
		while not node.unvisitedMoves and node.children:
			node = node.SelectChild()
			state.apply_move(node.move)
			#print "selecting", node.move


		# expansion
		# choose an unexplored move, and create a child node from it
		if node.unvisitedMoves:
			m = random.choice(node.unvisitedMoves)
			state.apply_move(m)
			node = node.AddChild(m, state)
			#print "expanding", m

		# simulation
		# run a simulation from the newly created child node
		depth = 0
		while state.get_moves() != [] and depth < rolloutDepth:
			m = random.choice(state.get_moves())
			state.apply_move(m)
			depth += 1
			#print "rollingout", m


		#backpropagation
		# send the results of the simulation up the tree
		scores = state.get_score()
		while node != None:
			if node.parent != None:
				if node.parent.turn == me:
					simResult = scores[me] - scores[you]
				else:
					simResult = scores[you] - scores[me]
				debugStr += "T: " + node.parent.turn + " R: " + str(simResult)
				node.Update(simResult)
			else:
				node.visited += 1
			node = node.parent

		t_now = time.time()
		debugStr += ")"

	sample_rate = float(iterations)/(t_now - t_start)
	print "%s samples per second" % (sample_rate)
	#print debugStr
	def avg_score(c):
		return float(c.score)/c.visited

	print rootnode.visited
	print sorted([(c.score/c.visited, c.score,c.visited) for c in rootnode.children])[-1]

	return max(rootnode.children,key=avg_score).move


def think(state, quip):

  move = uctsearch(state, 5)


  return move
