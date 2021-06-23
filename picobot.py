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
FREE = 'x'
ANY = '*'

HEIGHT = 35
WIDTH = 50

class Board():
    def __init__(self, filename):
        self.height = HEIGHT
        self.width = WIDTH
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
        i = 0
        with open(filename, 'r') as f:
            r = f.readlines()
        if len(r) > self.height:
            raise Exception
        for line in r:
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
    def surroundings(self, center):
        """
        Return string representation of the surroungs in 'NEWS' format
        """
        i = center[0]
        j = center[1]
        if i == 0 or i == self.height - 1:
            raise Exception
        if j == 0 or j == self.width - 1:
            raise Exception
        raise NotImplementedError
    
    def locateBot(self):
        """
        Return tuple (i, j) of the location of the BOT
        """
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == BOT:
                    return (i,j)
        return Exception
    
    def returnWalls(self):
        """
        Return set of tuples (i, j) of all walls
        """
        walls = set()
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == WALL:
                    walls.add((i,j))
        return walls

    def moveBot(self, direction):
        """
        Change bot's location and check for wall. Return if successful
        """
        bot = self.locateBot()
        if direction == NORTH:
            newLocation = (bot[0] + 1, bot[1])
        if direction == SOUTH:
            newLocation = (bot[0] - 1, bot[1])
        if direction == EAST:
            newLocation = (bot[0], bot[1] + 1)
        if direction == SOUTH:
            newLocation = (bot[0], bot[1] - 1)
        if newLocation[0] not in range(self.height) or newLocation[1] not in range(self.width):
            return False 
        if newLocation in self.returnWalls():
            return False
        
        raise NotImplementedError


class Rule():
    def __init__(self, state, surroundings, move, newState):
        self.state = state
        self.surroundings = surroundings
        self.move = move
        self.newState = newState
    def __repr__(self):
        return str(self.state) + ' ' + str(self.surroundings) + ' -> ' + str(self.move) + ' ' + str(self.newState)

class Player():
    def __init__(self, board, instructionsSet):
        self.Board = board
        self.instructionPATH = instructionsSet
        self.instructions = self.loadInstructions(self.instructionPATH)
        self.state = 0
    @staticmethod
    def parse(string):
        parsed = []
        tmp = str()
        for p in range(len(string)):
            if string[p] not in {' '}:
                tmp += string[p]
            else:
                parsed.append(tmp)
                tmp = str()
            if p == len(string) - 1:
                parsed.append(tmp)
                tmp = str()
        return parsed


    def loadInstructions(self, instructionsSet):
        states = set()
        instructions = set()
        with open(instructionsSet, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line[0] == '#' or line == '\n':
                continue
            print(line)
            p = self.parse(line)
            # syntax checking
            try: 
                p[0] = int(p[0])
                p[4] = int(p[4])
            except ValueError or TypeError:
                raise Exception
            if len(p) != 5:
                print(p, len(p))
                raise Exception
            if not isinstance(p[0], int):
                raise Exception
            if not isinstance(p[1], str):
                raise Exception
            if len(p[1]) != 4:
                raise Exception
            for dir in p[1]:
                if dir not in {NORTH, SOUTH, EAST, WEST, ANY, FREE}:
                    raise Exception
            if not p[2] == '->':
                raise Exception
            if p[3] not in {NORTH, SOUTH, EAST, WEST}:
                raise Exception
            if not isinstance(p[4], int):
                raise Exception
            instructions.add(Rule(p[0], p[1], p[3], p[4]))
            states.add(p[0])

        if 0 not in states:
            raise Exception
        for rule1 in instructions:
            for rule2 in instructions:
                if rule1 == rule2:
                    continue
                if rule1.state == rule2.state:
                    print (rule1, rule2, end='')
                    if rule1.surroundings == rule2.surroundings:
                        raise Exception
                    different = False
                    for i in range(4):
                        r1 = rule1.surroundings[i]
                        r2 = rule2.surroundings[i]
                        print(r1, r2)
                        if r1 in {NORTH, SOUTH, EAST, WEST} and r2 in {NORTH, SOUTH, EAST, WEST} and r1 != r2:
                            raise Exception
                        if r1 in {NORTH, SOUTH, EAST, WEST} and r2 == FREE:
                            different = True 
                            break
                        if r1 == FREE and r2 in {NORTH, SOUTH, EAST, WEST}:
                            different = True
                            break
                        print(' ' + str(different))
                    if not different:
                        raise Exception
        print('Finished loading from file')
        return instructions

    def step(self):
        print(self.instructions)
        surroundings = self.Board.surroundings(self.Board.locateBot())
        c = 0
        for instruction in self.instructions:
            different = False
            if self.state != instruction.state:
                continue
            for i in range (4):
                r = instruction.surroundings[i] 
                if r == ANY:
                    continue
                if r not in {NORTH, SOUTH, EAST, WEST, FREE}:
                    raise Exception
                if r == surroundings[i]:
                    continue
                different = True
                break
            if different:
                continue
            c += 1
            ins = instruction
        if c != 1:
            raise NameError("no instruction avaliabe or duplicate instruction")
        if not isinstance(ins, Rule):
            raise Exception
        print(ins)
        if not self.Board.moveBot(i.move):
            return False
        self.state = i.newState
        return True

def main():
    b = Board('layout')
    p = Player(b, 'instructions')
    print(b)

if __name__ == '__main__':
    main()

        
