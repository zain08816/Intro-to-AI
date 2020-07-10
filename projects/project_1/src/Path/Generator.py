import random
import re
from .Encoder import Encoder
from .State import State

class Generator:
    startState = None
    goalState = None

    # return type: list of states
    def getNeighbors(self, matrix, state):
        x = state.xPos
        y = state.yPos
        row_length = len(matrix)
        col_length = len(matrix[0])

        neighbor_bounds = [(x + 1, y), (x - 1, y), (x , y + 1), (x , y - 1)]
        neighbor_bounds = list(filter(lambda tuple: # keeps only valid bounds unlike -1
                             0 <= tuple[0] < row_length and
                             0 <= tuple[1] < col_length,
                             neighbor_bounds))

        result = []

        # convert from bound to the actual State object in the matrix
        for bound in neighbor_bounds:
            i = bound[0]
            j = bound[1]
            result.append(matrix[i][j])

        result = list(filter(lambda state:  state.explored == False, result)) # only consider unvisited neighbors
        return result

    def generateRandomMap(self, x, y, filename):
        matrix = self.__generateMatrix(x, y)
        self.__randomizeMap(matrix)

        # randomly selects indices to be the start
        startX = random.randint(0, x - 1)
        startY = random.randint(0, y - 1)
        matrix[startX][startY].blocked = False
        self.startState = matrix[startX][startY]

        # randomly selects indices to be the goal
        goalX = random.randint(0, x - 1)
        goalY = random.randint(0, y - 1)
        matrix[goalX][goalY].blocked = False
        self.goalState = matrix[goalX][goalY]
        encoder = Encoder()


        encoder.encode(matrix, filename, startX, startY, goalX, goalY)
        # self.__printMatrix(matrix) // for debugging
        return matrix

    # simply returns a matrix of x by y. Also init all of them to be 0
    def __generateMatrix(self, x, y):
        n = x
        m = y
        matrix = [State()] * n
        for row in range(n):
            matrix[row] = [State()] * m  # each row will have the same object, fixed in bottom code

        # Assign a new state person position & fill out its x,y attribute
        for row in range(n):
            for col in range(m):
                matrix[row][col] = State()  # new state person space
                state = matrix[row][col]
                state.xPos = row
                state.yPos = col
                state.gVal = 100000000  # "infinity" because python 3 ints have no upper bound
                state.explored = False
        return matrix

    # used for debugging
    def __printMatrix(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])

        for row in range(rows):
            for col in range(cols):
                state = matrix[row][col]
                print(state.isBlocked(), end="")  # end prevents creating a newline for every print
                print(" ", end=" ")  # True_True instead of TrueTrue
            print("")  # line break to distinct rows

    def __randomizeMap(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0])
        for row in range(rows):
            for col in range(cols):
                currentState = matrix[row][col]
                if currentState != self.startState or currentState != self.goalState:  # skip start or goal states
                    # if randomProb > 3 then it is unblocked (this ensures a 70% probability)
                    randomProbability = random.randint(1, 10)
                    if randomProbability <= 3:  # 30% chance to get <= 3 out of 10. 30% to block a Path
                        currentState.blocked = True  # 1 indicates the Path is blocked
        return matrix

    def decode(self, filename):
        f = open(filename, "r")
        line = f.readline()
        print(line)
        listOfNumbers = re.findall("[0-9]+", line)

        row = int(listOfNumbers[0])
        col = int(listOfNumbers[1])
        startX = int(listOfNumbers[2])
        startY = int(listOfNumbers[3])
        goalX = int(listOfNumbers[4])
        goalY = int(listOfNumbers[5])

        matrix = self.__generateMatrix(row, col)

        lines = f.readlines()

        col = 0

        for i in range(1, row + 1):  # need to start at 1 cuz lines[0] is blank lines
            currentLine = lines[i]
            for j in range(len(currentLine)):
                if (currentLine[j] != " " and currentLine[j] != "\n"):
                    # creating a new State() with the information in the txtfile
                    state = State()
                    state.xPos = i - 1  # first loop goes from [1,row+1) but we need it to be [0,row)
                    state.yPos = col
                    if currentLine[j] == '1':
                        state.blocked = True
                    else:
                        state.blocked = False

                    matrix[i - 1][col] = state
                    col = col + 1
            col = 0  # reset it back to the beginning for the next row

            self.startState = matrix[startX][startY]
            self.goalState = matrix[goalX][goalY]
        return matrix

    def generateAgentMatrix(self, matrix, start):
        row = len(matrix)
        col = len(matrix[0])
        newMatrix = self.__generateMatrix(row, col)

        neighbors = self.getNeighbors(matrix,start)
        for neighbor in neighbors: # looking for blocked neighbors in the actual matrix
            if(neighbor.isBlocked()):
                x = neighbor.xPos
                y = neighbor.yPos
                newMatrix[x][y] = neighbor
        return newMatrix





