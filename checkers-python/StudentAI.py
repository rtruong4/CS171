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
        global counter
        counter = 0
        countTime = 0
        global rollTime
        rollTime = 0
        global numNodes
        numNodes = 0
        while (time.time() - currentTime) < 1:
            counter+= 1
            leaf = self.tree_policy(root)
            simResult = self.rollout(leaf)
            self.backpropogate(leaf, simResult)
        #raise ValueError(counter)
        return self.bestMove(root)




    def bestMove(self, root):
        max = -1
        newNode = None
        for i in root.children:
            if i.visits >= max:
                max = i.visits
                newNode = i
        return newNode


    def checkNotFullExpand(self, node):
        # possibleMoves = 0
        # allowedMoves = node.board.get_all_possible_moves(node.color)
        #
        # for index in range(len(allowedMoves)):
        #     for inner_index in range(len(allowedMoves[index])):
        #         possibleMoves += 1
        #
        # return len(node.children) < possibleMoves

        #return len(node.unvisitedMoves) > 0 and len(node.children) != node.amtMoves

        return len(node.children) < node.amtMoves

        #return len(node.unvisitedMoves) != 0 and len(node.children) != 0



    def is_not_terminal(self, board, color):
        #return len(board.get_all_possible_moves(color)) > 0
        return board.is_win(color) == 0 and board.is_win(self.getOppositeColor(color)) == 0

    def tree_policy(self, node):
        global rollTime
        currNode = node
        while self.is_not_terminal(currNode.board, currNode.color):
            if self.checkNotFullExpand(currNode):
                # allowedMoves = currNode.board.get_all_possible_moves(currNode.color)
                #
                # listOfUnvisited = []
                # for index in range(len(allowedMoves)):
                #     for inner_index in range(len(allowedMoves[index])):
                #         move = allowedMoves[index][inner_index]
                #         if move not in currNode.visitedMoves:
                #             listOfUnvisited.append(move)
                #
                # newMove = random.choice(listOfUnvisited)
                # currNode.visitedMoves.append(newMove)
                #
                # bCopy = copy.deepcopy((currNode.board))
                # bCopy.make_move(newMove, currNode.color)
                # newNode = Node(bCopy, self.getOppositeColor(currNode.color), move = newMove, parent = currNode)
                # currNode.addChild(newNode)
                # return newNode

                #allowedMoves = currNode.board.get_all_possible_moves(currNode.color)
                newMoveIndex = randint(0, len(currNode.unvisitedMoves) - 1)

                newMove = currNode.unvisitedMoves.pop(newMoveIndex)

                bCopy = copy.deepcopy((currNode.board))

                bCopy.make_move(newMove, currNode.color)
                #bCopy.make_move(newMove, self.getOppositeColor(currNode.color))

                newNode = Node(bCopy, self.getOppositeColor(currNode.color), move=newMove, parent=currNode)

                #newNode = Node(bCopy, (currNode.color), move=newMove, parent=currNode)
                currNode.addChild(newNode)

                return newNode

            else:
                if len(currNode.children) == 0:
                    raise ValueError(len(currNode.unvisitedMoves))
                currNode = self.chooseBestChild(currNode)


        return currNode
        #raise ValueError




      



    # def chooseBestChild(self, node, constant = 1.414):
    def chooseBestChild(self, node, constant = 1.414):
        #Choose the best child based on UCB formula
        score = -1 #Keeps track of best UCB value
        bestChild = None  #List of nodes in case the UCB value is tied in different children

        for child in node.children:
            explore = float(math.sqrt(((math.log(node.visits))/float(child.visits))))
            x = float(child.wins/child.visits)
            ucb = x + (constant * explore)

            if ucb >= score:
                bestChild = child
                score = ucb
        # if bestChild is not None:
        #     return bestChild
        # else:
        #     return random.choice(node.children)
        if bestChild == None:
            raise ValueError("Best Child is none")
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
        global rollTime
        boardCopy = copy.deepcopy(node.board)
        currColor = node.color

        allowedMoves = boardCopy.get_all_possible_moves(currColor)



        while len(allowedMoves) > 0:

            move = random.choice(random.choice(allowedMoves))

            boardCopy.make_move(move, currColor)

            currColor = self.getOppositeColor(currColor)

            allowedMoves = boardCopy.get_all_possible_moves(currColor)

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
            currColor = node.color
            # if node.color == self.color:
            # #if node.color == self.opponent[self.color]:
            # #If the color of the node is our color
            #     if result == node.color:
            #         node.visits += 1
            #     elif result == self.getOppositeColor(node.color):
            #         node.wins += 1
            #         node.visits += 1
            #     elif result == -1:
            #         node.wins += 0.5
            #         node.visits += 1
            #     else:
            #         raise ValueError
            # #elif node.color == self.color:
            # elif node.color == self.opponent[self.color]:
            # #If the color of the node is the opposite color
            #     if result == node.color:
            #         node.visits += 1
            #     elif result == self.getOppositeColor(node.color):
            #         node.wins += 1
            #         node.visits += 1
            #     elif result == -1:
            #         node.wins += 0.5
            #         node.visits += 1
            #     else:
            #         raise ValueError
            # else:
            #     raise ValueError
            # if result == node.color:
            #     node.visits += 1
            # elif result == self.getOppositeColor(node.color):
            #     node.wins += 1
            #     node.visits += 1
            # elif result == -1:
            #     node.wins += 0.5
            #     node.visits += 1
            # else:
            #      raise ValueError


            # if result == node.color:
            #     node.visits += 1
            # elif result == self.getOppositeColor(node.color):
            #     node.wins += 1
            #     node.visits += 1
            # elif result == -1:
            #     node.wins += 0.5
            #     node.visits += 1
            # else:
            #      raise ValueError

            node.visits += 1
            if result == self.getOppositeColor(currColor):
                node.wins += 1
            elif result == -1:
                node.wins += 0.5
            elif result == currColor:
                node.wins += 0
            else:
                 raise ValueError(currColor)
            node = node.parent


        #This section is for updating the root node
        node.visits += 1
        if result == self.getOppositeColor(currColor):
            node.wins += 1
        elif result == -1:
            node.wins += 0.5
        elif result == currColor:
            node.wins += 0
        else:
            raise ValueError

        return


class Node():

    def __init__(self,  board, color, move = None, parent = None):
        self.board = board
        self.move = move #This is the move used to get to this state
        self.children = []
        self.parent = parent
        self.visits = 0
        self.wins = 0
        self.color = color
        self.unvisitedMoves = self.flatten(board.get_all_possible_moves(color)) #unvisitedMoves is a list of move objects
        self.amtMoves = len(self.unvisitedMoves)
        #self.visitedMoves = []


    def getOppositeColor(self, color):
        if color == 2:
            return 1
        elif color == 1:
            return 2
        else:
            raise ValueError

    def flatten(self, list):
        flatList = []
        global counter
        # if len(list) == 0:
        #     raise ValueError(self.color, len(self.board.get_all_possible_moves((self.color))), counter, len(self.board.get_all_possible_moves((self.getOppositeColor(self.color)))))
        for sub in list:
            for item in sub:
                flatList.append(item)
        return flatList

    def addChild(self, node):
        #Adds a new child to this node

        global numNodes
        self.children.append(node)
        numNodes += 1


    def hasChild(self):
        #Sees if the child has a node
        return len(self.children) > 0



