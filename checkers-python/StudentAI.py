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

        rootNode = Node(self.board)
        newMove = self.mctSearch(rootNode) #Returns a node
        move = newMove #Move is a node type
        self.board.make_move(move,self.color)
        return move





  
    def mctSearch(self, root):
        currentTime = time.time()

        while (time.time() - currentTime) < 2 and len(root.board.get_all_possible_moves(self.color)) > 0:
            leaf = self.traverse(root)
            simResult = self.simulate(leaf)
            self.backpropogate(leaf, simResult)


        return self.bestMove(root)



    def checkFullExpand(self, node):
        return len(node.board.get_all_possible_moves(self.color)) == len(list(node.children))

    # def tree_policy(self, node):
    #     while not self.is_terminal(node.board):
    #         if not self.checkFullExpand(node):
    #             allowedMoves = node.board.get_all_possible_moves(self.color)
    #
    #             index = randint(0, len(allowedMoves) - 1)
    #             inner_index = randint(0, len(allowedMoves[index]) - 1)
    #             move = allowedMoves[index][inner_index]
    #
    #             newBoard = node.board.make_move(move, self.color)





      
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



    def is_terminal(self, board):
        return not len(board.get_all_possible_moves) > 0

    def rollout(self, node):
        """From the given board, simulate a random game until win, loss, or tie and return the appropriate value"""
        boardCopy = copy.deepcopy(node.board)
        currColor = 1
        while not self.is_terminal(boardCopy):
            if currColor == 1:
                color = self.color
            elif currColor == -1:
                color = self.opponent[self.color]

            allowedMoves = boardCopy.get_all_possible_moves(color)

            index = randint(0, len(allowedMoves) - 1)
            inner_index = randint(0, len(allowedMoves[index]) - 1)
            move = allowedMoves[index][inner_index]

            boardCopy.make_move(move, color)
            color *= -1

        winner = boardCopy.is_win(self.color)
        if winner is not None:
            if winner == self.color:
                return 1
            elif winner == self.opponent[self.color]:
                return 0
            elif winner == -1:
                return 0.5







class Node():

    def __init__(self, board, parent = None):
        self.board = board
        self.children = []
        self.parent = parent
        self.visits = 1
        self.wins = 0



    def addChild(self, board):
        #Adds a new child to this node
        newChild = Node(board, parent = self)
        self.children.append(node)


    def hasChild(self):
        #Sees if the child has a node
        return len(self.children) > 0



