import time
import random
from math import sqrt, log

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.score = 0.0
        self.visits = 0.0
        self.untriedMoves = state.get_moves() # future child nodes
        self.playerTurn = state.get_whos_turn()

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.score/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.score += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.score) + "/" + str(self.visits) # + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

def UCT(rootstate, rolloutDepth = int('inf'), dur = 1, verbose = False):
    """ Conduct a UCT search for dur second(s) starting from rootstate.
        Return the best move from the rootstate."""

    rootnode = Node(state = rootstate)
    debugStr = "rootState is " + str(rootstate)

    me = rootstate.get_whos_turn()

    debugStr += ", it is " + str(me) + "'s turn.\n"

    def outcome(score):
        if me == 'red':
            return score['red'] - score['blue']
        else:
            return score['blue'] - score['red']
        """if me == 'red':
            myscore = score['red'] - score['blue']
        else:
            myscore = score['blue'] - score['red']

        if myscore > 0:
            return 1
        if myscore == 0:
            return 0
        else:
            return -1"""

    t_start = time.time()
    t_deadline = t_start + dur

    iterations = 0;

    while True:
        iterations += 1

        #MCTS
        node = rootnode
        state = rootstate.copy()

        while node.untriedMoves == [] and node.childNodes != []:
            # debugStr += "\tAll movies tried, selecting a child.\n"
            # debugStr += rootnode.TreeToString(1)
            node = node.UCTSelectChild()
            state.apply_move(node.move)

        debugStr += "\tSelected node " + str(node.move) + ".\n"

        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            state.apply_move(m)
            node = node.AddChild(m, state)

        debugStr += "\t\tCreating child " + str(node.move) + ".\n"

        depth = 0
        while state.get_moves() != [] and depth < rolloutDepth:
            """
            moves = state.get_moves()

            best_move = moves[0]
            best_expectation = float('-inf')

            for move in moves:

                rollout_state = state.copy()

                rollout_state.apply_move(move)

                score = outcome(rollout_state.get_score())

                if score > best_expectation:
                    best_expectation = score
                    best_move = move
            
            state.apply_move(best_move)
            """
            state.apply_move(random.choice(state.get_moves()))
            depth+=1

        gamescore = outcome(state.get_score())
        debugStr += "\t\tSimulation score is " + str(gamescore) + ".\n"
        while node != None:
            if node.parentNode != None:
               print node.parentNode.playerTurn
               if node.parentNode.playerTurn != me:
                  gamescore = -gamescore
            
            node.Update(gamescore)
            node = node.parentNode




        #end MCTS

        t_now = time.time()
        if t_now > t_deadline:
            break

    sample_rate = float(iterations)/(t_now - t_start)
    print "%s samples per second" % (sample_rate)
    #print rootnode.TreeToString(0)
    rootnode.childNodes.sort(key = lambda c: c.score/c.visits)
    for c in rootnode.childNodes:
        print "S: " + str(c.score) + " V: " + str(c.visits) + " S/V: " + str(c.score/c.visits) + " Move: " + str(c.move)

    movelist = sorted(rootnode.childNodes, key = lambda c: c.score/c.visits)
    print "Selected move = " + str(movelist[-1].move)
    debugStr += "Selecting move " + str(movelist[-1].move)
    if (verbose): print debugStr
    return movelist[-1].move

