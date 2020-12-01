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
        rootNode.parent = None
        newNode = self.mctSearch(rootNode) #Returns a node
        move = newNode.move #Move is a node type
        self.board.make_move(move,self.color)
        return move





  
    def mctSearch(self, root):
        currentTime = time.time()
        while (time.time() - currentTime) < 15:
            leaf = self.tree_policy(root)
            simResult = self.rollout(leaf)
            self.backpropogate(leaf, simResult)

        return self.bestMove(root)




    def bestMove(self, root):
        max = 0
        newNode = None
        for i in root.children:
            if i.visits >= max:
                max = i.visits
                newNode = i
        return newNode

    def checkNotFullExpand(self, node):
        possibleMoves = 0
        allowedMoves = node.board.get_all_possible_moves(node.color)

        for index in range(len(allowedMoves)):
            for inner_index in range(len(allowedMoves[index])):
                possibleMoves += 1

        return len(node.visitedMoves) < possibleMoves


    def is_not_terminal(self, board, color):
        return len(board.get_all_possible_moves(color)) > 0
        #return board.is_win(color) == 0


    def tree_policy(self, node):
        currNode = node
        iter = 0
        while self.is_not_terminal(currNode.board, currNode.color):
            if self.checkNotFullExpand(currNode):

                allowedMoves = currNode.board.get_all_possible_moves(currNode.color)

                listOfUnvisited = []
                for index in range(len(allowedMoves)):
                    for inner_index in range(len(allowedMoves[index])):
                        move = allowedMoves[index][inner_index]
                        if move not in currNode.visitedMoves:
                            listOfUnvisited.append(move)

                newMove = random.choice(listOfUnvisited)
                currNode.visitedMoves.append(newMove)

                bCopy = copy.deepcopy((currNode.board))
                bCopy.make_move(newMove, currNode.color)
                newNode = Node(bCopy, self.getOppositeColor(currNode.color), move = newMove, parent = currNode)
                currNode.addChild(newNode)
                return newNode

            else:
                currNode = self.chooseBestChild(currNode)


        return currNode




      



    def chooseBestChild(self, node, constant = 1.414):
        #Choose the best child based on UCB formula
        score = -1 #Keeps track of best UCB value
        bestChild = None  #List of nodes in case the UCB value is tied in different children

        for child in node.children:
            explore = float(math.sqrt((math.log(node.visits))/float(child.visits)))
            x = float(child.wins/child.visits)
            ucb = x + (constant * explore)

            if ucb > score:
                bestChild = child
                score = ucb

        return bestChild






    def getOppositeColor(self, color):

        if color == 2:
            return 1
        elif color == 1:
            return 2
        else:
            raise ValueError

    def rollout(self, node):
        """From the given board, simulate a random game until win, loss, or tie and return the appropriate value"""
        boardCopy = copy.deepcopy(node.board)
        currColor = node.color
        count = 0
        while self.is_not_terminal(boardCopy, currColor):
            count += 1
            allowedMoves = boardCopy.get_all_possible_moves(currColor)

            index = randint(0, len(allowedMoves) - 1)
            inner_index = randint(0, len(allowedMoves[index]) - 1)
            move = allowedMoves[index][inner_index]



            boardCopy.make_move(move, currColor)



            currColor = self.getOppositeColor(currColor)


        return boardCopy.is_win(self.getOppositeColor(currColor))
        # winner = boardCopy.is_win(self.getOppositeColor(currColor))
        # if winner == self.color:
        #     return 1
        # elif winner == self.opponent[self.color]:
        #     return 0
        # elif winner == -1:
        #     return 0.5
        # else:
        #     raise ValueError



    def backpropogate(self, node, result):
        #Update the current move with the simulation result
        #result = 0 means the opponent won, result = 1 means that our ai won
        # while node.parent is not None:
        #     node.visits += 1
        #     node.wins += result
        #     node = node.parent
        # return


        while node.parent is not None:

            #if node.color == self.color:
            if node.color == self.opponent[self.color]:
            #If the color of the node is our color

                if result == self.opponent[self.color]:
                    node.visits += 1
                elif result == self.color:
                    node.wins += 1
                    node.visits += 1
                elif result == -1:
                    node.wins += 0.5
                    node.visits += 1
            elif node.color == self.color:
            #elif node.color == self.opponent[self.color]:
            #If the color of the node is the opposite color
                if result == self.opponent[self.color]:
                    node.wins += 1
                    node.visits += 1
                elif result == self.color:
                    node.visits += 1
                elif result == -1:
                    node.wins += 0.5
                    node.visits += 1
            else:
                raise ValueError
            node = node.parent
        return

    def amtAbove(self, node):
        count = 0
        while node.parent is not None:
            count += 1
            node = node.parent
        return count



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



    def addChild(self, node):
        #Adds a new child to this node


        self.children.append(node)



    def hasChild(self):
        #Sees if the child has a node
        return len(self.children) > 0



