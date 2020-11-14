from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import random
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
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move


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



