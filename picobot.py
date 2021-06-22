import sys
import random

EMPTY = 0
CLEAR = 1
WALL = 2
BOT = 3

NORTH = 'N'
EAST = 'E'
WEST = 'W'
SOUTH = 'S'

class Board():
    def __init__(self, filename):
        self.height = 50
        self.width = 50
        self.board = []
        for i in range(self.height):
            l = []
            for j in range(self.width):
                l.append(EMPTY)
            self.board.append(l)
        self.load(filename)
        random.seed()
        i = random.randint(0, self.height - 1)
        j = random.randint(0, self.width - 1)
        while self.board[i][j] == WALL or self.board[i][j] == BOT:
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)
        self.board[i][j] = BOT
    def __repr__(self):
        print('Height, Width', self.height, self.width)
        msg = str()
        for row in self.board:
            for item in row:
                if item == EMPTY:
                    msg += '.'
                if item == WALL:
                    msg += '#'
                if item == CLEAR:
                    msg += '_'
                if item == BOT:
                    msg += 'O'
            msg += '\n'
        return msg
    def load(self, filename):
        with open(filename, 'r') as f:
            i = 0
            if len(f.readlines()) > self.height:
                raise Exception
            for line in f.readlines():
                l = []
                for item in line:
                    if item == '.':
                        l.append(EMPTY)
                    if item == '#':
                        l.append(WALL)
                    if item == '_':
                        l.append(CLEAR)
                    if item == 'O':
                        l.append(BOT)
                self.board[i] = l
                i += 1
        f.close()
    def neighboringCells(self, center):
        """
        Return dict with cardinal keys determining if wall
        """
        raise NotImplementedError
    
    def locateBot(self):
        """
        Return tuple (i. j) of the location of the BOT
        """
        raise NotImplementedError
    
    def returnWalls(self):
        """
        Return set of tuples (i, j) of all walls
        """
        raise NotImplementedError


class Player():
    def __init__(self, board, instructionsSet):
        self.Board = board
        self.instructionPATH = instructionsSet
        self.instructions = self.loadInstructions(self.instructionPATH)
    def parse(string):
        parsed = []
        tmp = str()
        for p in range(len(string)):
            
            if string[p] not in {' ', '\n'}:
                tmp += string[p]
            else:
                parsed.append(tmp)
                tmp = str()
            if p == len(string) - 1:
                parsed.append(tmp)
                tmp = str()
        return parsed


    def loadInstructions(self, instructionsSet):

        with open(instructionsSet, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            if line[0] == '#':
                continue
            p = line.parse(line)
            
        raise NotImplementedError

def main():
    b = Board('layout')
    p = Player(b, 'instructions')
    print(repr(b))

main()

        
