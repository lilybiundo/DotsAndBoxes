import random
import time
from UCT import UCT

def think(state, quip):

	move = UCT(state, 5, verbose = False)


	return move