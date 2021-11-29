# 
# Programming Assignment 2, CS640
#
# A Gomoku (Gobang) Game
#
# Adapted from CS111
# By Yiwen Gu
#
# You need to implement an AI Player for Gomoku
# A Random Player is provided for you
# 
#

from pa2_gomoku import Player



import copy
import math
import random

class AIPlayer(Player):
    """ a subclass of Player that looks ahead some number of moves and 
    strategically determines its best next move.
    """
    
                    ###################################
                    ### SCORING THE BOARD MECHANISM ###
                    ###################################
    # note to self
    # board.slots represents rows instead of columns (pepega)
    # (0,1) = board.slots[0][1]
    
    def scoresFor(self,board):
        self.xCount = {5:0,(4,0):0,(4,1):0,(3,0):0,(3,1):0,(2,0):0,(2,1):0,(1,0):0,(1,1):0}
        self.oCount = {5:0,(4,0):0,(4,1):0,(3,0):0,(3,1):0,(2,0):0,(2,1):0,(1,0):0,(1,1):0}
        self.detectRow(board)
        self.detectCol(board)
        self.detectDia(board)
        return self.calculate(self.xCount,self.oCount)
    
    def calculate(self,xc,oc):
        s = 0
        if self.checker == 'X':
            for k in oc:
                if k == 5 and oc[k]>0:
                    return 10000000
                elif k == (4,0) or k == (4,1) :
                    s+=oc[k]*100000
                elif k == (3,0):
                    s+=oc[k]*1000
                elif k == (3,1) or k == (2,0):
                    s+=oc[k]*10
                elif k == (2,1) or k == (1,0):
                    s+=oc[k]*1
            for k in xc:
                if k == 5 and xc[k]>0:
                    return -10000000
                elif k == (4,0):
                    s-=xc[k]*5000
                elif k == (3,0):
                    s-=xc[k]*500
                elif k == (4,1):
                    s-=xc[k]*30
                elif k == (3,1) or k == (2,0):
                    s-=xc[k]*10
                elif k == (2,1) or k == (1,0):
                    s-=xc[k]*1
        elif self.checker == 'O':
            for k in oc:
                if k== 5 and oc[k]>0:
                    return 10000000
                elif k == (4,0):
                    s+=oc[k]*5000
                elif k == (3,0):
                    s+=oc[k]*50
                elif k == (4,1):
                    s+=oc[k]*30
                elif k == (3,1) or k == (2,0):
                    s+=oc[k]*10
                elif k == (2,1) or k == (1,0):
                    s+=oc[k]*1
            for k in xc:
                if k == 5 and xc[k]>0:
                    return -10000000
                elif k == (4,1) or k == (4,0):
                    s-=xc[k]*100000
                elif k == (3,0):
                    s-=xc[k]*1000
                elif k == (3,1) or k== (2,0):
                    s-=xc[k]*10
                elif k == (2,1) or k == (1,0):
                    s-=xc[k]*1
        return s
    
        
    def detectRow(self,board):
        # pass in each row of the board to detectLine
        for row in board.slots:
            self.detectLine(row)
            
    def detectCol(self,board):
        # pass in each column in the board to detectLine
        c = []
        for col in range(len(board.slots[0])):
            for row in range(len(board.slots)):
                c.append(board.slots[row][col])
            self.detectLine(c)
            
    def detectDia(self,board):
        # pass in each diagonal in the board to detectLine
        diagonals = self.detForwardDiagonal(board) + self.detBackwardDiagonal(board)
        for dia in diagonals:
            self.detectLine(dia)
            
    
    # getting diagonals by ofsetting and taking columns
    def detForwardDiagonal(self,board):
        offset = [None] * (len(board.slots)-1)
        offsettedBoard = [offset[:i] + r+ offset[i:] for i,r in enumerate(board.slots)]
        return [[c for c in r if not c is None] for r in zip(*offsettedBoard)]

    def detBackwardDiagonal(self,board):
        offset = [None] * (len(board.slots)-1)
        offsettedBoard = [offset[i:] + r+ offset[:i] for i,r in enumerate(board.slots)]
        return [[c for c in r if not c is None] for r in zip(*offsettedBoard)]
        
            
    def detectLine(self,line):
        strLine = self.transfer(line,'X')
        self.detect(strLine,'x')
        strLine = self.transfer(line,'O')
        self.detect(strLine,'o')
        
    def transfer(self,line,checker):
        # changes formatting to either open or blocked or gapped strings
        if checker == 'X':
            strLine = 'o'
        elif checker == 'O':
            strLine = 'x'
        for s in line:
            if s == ' ':
                strLine += '0'
            elif s == 'O':
                strLine += 'o'
            elif s == 'X':
                strLine += 'x'
        if checker == 'X':
            strLine += 'o'
        elif checker == 'O':
            strLine += 'x'
        return strLine
    
    def detect(self,strLine,checker):
        while strLine.find(checker)!= -1:
            gap = 0
            start = strLine.find(checker)
            block = 0
            if strLine[start-1] not in ['0', checker]:
                block = 1
            sRest = strLine[start+1:]
            run = 1
            for i in range(len(sRest)):
                if sRest[i] == checker:
                    run+=1
                elif sRest[i] == '0':
                    if sRest[i+1] == checker and run != 4 and (run ==2 and sRest[i+2]!= checker) and run<6:
                        gap += 1
                        continue
                    else:
                        break
                else:
                    block += 1
                    break
            strLine = strLine[start + gap + run:]
            if block < 2:
                self.update(checker,run,block)
                
    def update(self,checker,run,block):
        if checker == 'x':
            if run == 5:
                self.xCount[5]+=1
            elif run < 6:
                self.xCount[(run,block)]+=1
        elif checker == 'o':
            if run == 5:
                self.oCount[5]+=1
            elif run < 6:
                self.oCount[(run,block)]+=1

    # minimax alg
    def minimax(self,board):
        scores = []
        testboard = copy.deepcopy(board)
        # do a turn, compute scores
        for row in range(len(testboard.slots)):
            for col in range(len(testboard.slots[0])):
                if testboard.can_add_to(row,col):
                    testboard.add_checker(self.checker,row,col)
                    scores.append((self.scoresFor(testboard),row,col))
                    testboard = copy.deepcopy(board)
                    
        # if i am the mazimizing player
        if self.checker == 'O':
            val = -math.inf
            res = []
            for tup in scores:
                if tup[0]>val:
                    val = tup[0]
                    res = [(tup[1], tup[2])]
                elif tup[0] == val:
                    res += [(tup[1], tup[2])]
            row,col = random.choice(res)
        else:
            val = math.inf
            res = []
            for tup in scores:
                if tup[0]<val:
                    val = tup[0]
                    res = [(tup[1], tup[2])]
                elif tup[0] == val:
                    res += [(tup[1], tup[2])]
            row,col = random.choice(res)
        return row,col

    def next_move(self, board):
        """ returns the called AIPlayer's next move for a game on
            the specified Board object. 
            input: board is a Board object for the game that the called
                     Player is playing.
            return: row, col are the coordinated of a vacant location on the board 
        """
        self.num_moves += 1
        assert(board.is_full() == False)
        row, col = self.minimax(board)
        return (row,col)