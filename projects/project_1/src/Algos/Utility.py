import random
import re

class Utility:
    startState = None
    goalState = None

    def getNeighbors(self, matrix, state):
        x = state.xPos
        y = state.yPos
        row_length = len(matrix)
        col_length = len(matrix[0])

        neighbors = [(x + 1, y), (x - 1, y), (x , y + 1), (x , y - 1)]

        temp = []
        res = []

        for bound in neighbors:
            if (0 <= bound[0] < row_length) and (0 <= bound[1] < col_length):
                temp.append(matrix[bound[0]][bound[1]])
        
        for b in temp:
            if b.explored == False:
                res.append(b)

        return res

    # def generateRandomMap(self, x, y, filename):
    #     matrix = self.__generateMatrix(x, y)
    #     self.__randomizeMap(matrix)


    #     startX = random.randint(0, x - 1)
    #     startY = random.randint(0, y - 1)
    #     matrix[startX][startY].blocked = False
    #     self.startState = matrix[startX][startY]


    #     goalX = random.randint(0, x - 1)
    #     goalY = random.randint(0, y - 1)
    #     matrix[goalX][goalY].blocked = False
    #     self.goalState = matrix[goalX][goalY]
    #     encoder = Encoder()


    #     encoder.encode(matrix, filename, startX, startY, goalX, goalY)
     
    #     return matrix

    def __generateMatrix(self, x, y):
        n = x
        m = y
        matrix = [State()] * n
        for row in range(n):
            matrix[row] = [State()] * m  

        for row in range(n):
            for col in range(m):
                matrix[row][col] = State() 
                state = matrix[row][col]
                state.xPos = row
                state.yPos = col
                state.gVal = 999999999  
                state.explored = False
        return matrix

    # def __randomizeMap(self, matrix):
    #     rows = len(matrix)
    #     cols = len(matrix[0])
    #     for row in range(rows):
    #         for col in range(cols):
    #             currentState = matrix[row][col]
    #             if currentState != self.startState or currentState != self.goalState: 
    #                 randomProbability = random.randint(1, 10)
    #                 if randomProbability <= 3:  
    #                     currentState.blocked = True  
    #     return matrix

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

        for i in range(1, row + 1):
            currentLine = lines[i]
            for j in range(len(currentLine)):
                if (currentLine[j] != " " and currentLine[j] != "\n"):
                    state = State()
                    state.xPos = i - 1
                    state.yPos = col
                    if currentLine[j] == '1':
                        state.blocked = True
                    else:
                        state.blocked = False

                    matrix[i - 1][col] = state
                    col = col + 1
            col = 0 

            self.startState = matrix[startX][startY]
            self.goalState = matrix[goalX][goalY]
        return matrix

    def generateAgentMatrix(self, matrix, start):
        row = len(matrix)
        col = len(matrix[0])
        newMatrix = self.__generateMatrix(row, col)

        neighbors = self.getNeighbors(matrix,start)
        for neighbor in neighbors:
            if(neighbor.isBlocked()):
                x = neighbor.xPos
                y = neighbor.yPos
                newMatrix[x][y] = neighbor
        return newMatrix



class State:
    xPos = None
    yPos = None
    parent = None
    next = None
    blocked = False
    explored = False
    gVal = 0
    hVal = 0
    fVal = 0
    newHVal = 0
    search = 0


    def isBlocked(self):
        return self.blocked

    def isExplored(self):
        return self.explored

    def inBound(self, width, height):
        x = self.xPos
        y = self.yPos

        result = 0 <= x < width and 0 <= y < height
        return result

    def __lt__(self, other):
        return self.fVal < other.fVal

class Encoder:
    def encode(self, matrix, filename, startX, startY, goalX, goalY):
        rows = len(matrix)
        cols = len(matrix[0])
        f = open(filename, "w+")

    
        f.write(str(rows) +"x" + str(cols) +
                " start("+str(startX)+","+str(startY)+")" +
                " goal(" + str(goalX) + "," + str(goalY) + ")" + "\n" )
        f.write("\n")



        for row in range(rows):
            for col in range(cols):
                state = matrix[row][col]
                if(state.isBlocked()): 
                    f.write("1 ")
                else:
                    f.write("0 ")
            f.write("\n") 
        f.close()

    def sol_encode(self, matrix, filename):
        rows = len(matrix)
        cols = len(matrix[0])
        f = open(filename, "w+")

        for row in range(rows):
            for col in range(cols):
                if matrix[row][col] == '~':
                    f.write("  ")
                else:
                    state = matrix[row][col]
                    if (state.isBlocked()): 
                        f.write("1 ")
                    else:
                        f.write("0 ")
            f.write("\n")  
        f.close()

class Writer():


    # def print_path_to(self,state):
    #     if state.parent == None:
    #         print("("+str(state.xPos) + "," + str(state.yPos)+")", end = "")
    #     else:
    #         self.print_path_to(state.parent)
    #         print("-> ("+str(state.xPos) + "," + str(state.yPos)+")", end ="")

    def generate_sol_file(self, matrix,state, sol_name):
        encoder = Encoder()

        while state:
            x = state.xPos
            y = state.yPos
            matrix[x][y] = '~'
            state = state.parent
        encoder.sol_encode(matrix,sol_name)


