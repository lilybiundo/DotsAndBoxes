import random
import time
from UCT_new import uctsearch

def think(state, quip):

	move = uctsearch(state, 5)


	return move