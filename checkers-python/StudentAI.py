from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import random
import copy
import time
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color]) #A move is given to us and we need to update it on our local board
        else:
            self.color = 1


        newMove = self.mctSearch(self.board)
        move = newMove
        self.board.make_move(move,self.color)
        return move





  
    def mctSearch(self, root):
        currentTime = time.time()

        while (time.time() - currentTime) < 15 and len(root.get_all_possible_moves) > 0:
            leaf = self.traverse(root)
            simResult = self.simulate(leaf)
            self.backpropogate(leaf, simResult)


        return self.bestMove(root)


    def traverse(self, node):
        #Find next node to traverse
        if not node.hasChild():
            return node #Return current node if there are no child nodes
        else:
            for child in node.childrenList:
                if child.visits == 1:
                    return child #Return child that has not been visited
            return self.chooseBestChild(node) #Return best child if all children are visited


    def bestMove(self, node):

        def visitNum(n):
            return n.wins/n.visits

        return max(node.children, key = visitNum)
      
      
    def backpropogate(self, node, result):
        #Update the current move with the simulation result
        if node.parent == None: return #Stop backpropogating at root node
        node.visits += 1
        node.wins += result
        self.backpropogate(node.parent) #Recursively call backpropogate function


    def chooseBestChild(self, node, constant = 1):
        #Choose the best child based on UCB formula
        score = 0 #Keeps track of best UCB value
        childrenList = [] #List of nodes in case the UCB value is tied in different children
        for child in node.children:
            explore = math.sqrt(math.log(node.visits)/float(child.visits))
            x = child.wins/child.visits
            ucb = x + (constant * explore)

            if ucb == score:
                childrenList.append(child)
            elif ucb > score:
                childrenList.clear()
                childrenList.append(child)
                score = ucb

        return random.choice(childrenList)




    def simulate(self, node):

        """From the given board, simulate a random game until win, loss, or tie and return the appropriate value"""
        boardState = copy.deepcopy(node.board)


        while True:
            allowedMoves = boardState.get_all_possible_moves(self.color)

            if len(allowedMoves) == 0:
                winner = boardState.is_win(self.color)
                if winner is not None:
                    if winner == self.color:
                        return 1
                    elif winner == self.opponent[self.color]:
                        return 0
                    elif winner == -1:
                        return 0.5
                    #If winner == 0 do nothing

            randomMove = random.choice(allowedMoves)
            boardState.make_move(randomMove, self.color)




class Node():

    def __init__(self, board, parent = None):
        self.board = board
        self.children = []
        self.parent = parent
        self.visits = 1
        self.wins = 0



    def addChild(self, node):
        #Adds a new child to this node
        node.parent = self
        self.children.append(node)


    def hasChild(self):
        #Sees if the child has a node
        return len(self.children) > 0



