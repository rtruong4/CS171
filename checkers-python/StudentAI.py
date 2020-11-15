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

        rootNode = Node(board = self.board, color = self.color)
        newNode = self.mctSearch(rootNode) #Returns a node
        move = newNode.move #Move is a node type
        self.board.make_move(move,self.color)
        return move





  
    def mctSearch(self, root):
        currentTime = time.time()

        while (time.time() - currentTime) < 2 and len(root.board.get_all_possible_moves(self.color)) > 0:
            leaf = self.tree_policy(root)
            simResult = self.rollout(leaf)
            self.backpropogate(leaf, simResult)


        return self.bestMove(root)




    def bestMove(self, node):
        maxVisits = 0
        newNode = node
        for i in node.children:
            if i.visits > maxVisits:
                maxVisits = i.visits
                newNode = i

        return newNode

    def checkFullExpand(self, node):
        counter = 0
        allowedMoves = node.board.get_all_possible_moves(node.color)

        for index in range(len(allowedMoves)):
            for inner_index in range(len(allowedMoves[index])):
                counter += 1

        return len(node.children) == counter

    def tree_policy(self, node):
        while not self.is_terminal(node.board, node.color):
            if not self.checkFullExpand(node):

                allowedMoves = node.board.get_all_possible_moves(node.color)
                #allowedmoves[0][0]
                newMove = 0

                for index in range(len(allowedMoves)):
                    for inner_index in range(len(allowedMoves[index])):
                        move = allowedMoves[index][inner_index]
                        if move not in node.visitedMoves:
                            newMove = move


                node.visitedMoves.append(newMove)
                newNode = node.addChild(newMove, node.board, self.color)

                return newNode

            else:
                return self.chooseBestChild(node)

        return node




      



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



    def is_terminal(self, board, color):

        return not len(board.get_all_possible_moves(color)) > 0

    def rollout(self, node):
        """From the given board, simulate a random game until win, loss, or tie and return the appropriate value"""
        boardCopy = copy.deepcopy(node.board)
        currColor = 1
        color = self.color
        while not self.is_terminal(boardCopy, color):
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
        if winner == self.color:
            return 1
        elif winner == self.opponent[self.color]:
            return 0
        elif winner == -1:
            return 0.5
        else:
            return 0


    def backpropogate(self, node, result):
        #Update the current move with the simulation result
        if node.parent == None: return #Stop backpropogating at root node
        node.visits += 1
        node.wins += result
        self.backpropogate(node.parent, result) #Recursively call backpropogate function





class Node():

    def __init__(self,  board, color, move = None, parent = None):
        self.board = board
        self.move = move #This is the move used to get to this state
        self.children = []
        self.parent = parent
        self.visits = 1
        self.wins = 0
        self.color = color
        self.visitedMoves = [] #visitedMoves is a list of move objects



    def addChild(self, move, prevBoard, color):
        #Adds a new child to this node
        bCopy = copy.deepcopy((prevBoard))
        bCopy.make_move(move, color)
        newChild = Node(bCopy, color, move, parent = self)
        self.children.append(newChild)
        return newChild


    def hasChild(self):
        #Sees if the child has a node
        return len(self.children) > 0



