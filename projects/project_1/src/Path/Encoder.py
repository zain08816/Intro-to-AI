# will convert matrix to a visual textfile

class Encoder:
    def encode(self, matrix, filename, startX, startY, goalX, goalY):
        rows = len(matrix)
        cols = len(matrix[0])
        f = open(filename, "w+")

        # formats the first line of the txtfile
        f.write(str(rows) +"x" + str(cols) +
                " start("+str(startX)+","+str(startY)+")" +
                " goal(" + str(goalX) + "," + str(goalY) + ")" + "\n" )
        f.write("\n")



        for row in range(rows):
            for col in range(cols):
                state = matrix[row][col]
                if(state.isBlocked()): # 1 represents blocked, while 0 is unblocked
                    f.write("1 ")
                else:
                    f.write("0 ")
            f.write("\n") # linebreak for each row
        f.close()

    # does not include extra information at top
    def sol_encode(self, matrix, filename):
        # need to add a way specify a location
        rows = len(matrix)
        cols = len(matrix[0])
        f = open(filename, "w+")

        for row in range(rows):
            for col in range(cols):
                if matrix[row][col] == '~':
                    f.write("' ")
                else:
                    state = matrix[row][col]
                    if (state.isBlocked()):  # 1 represents blocked, while 0 is unblocked
                        f.write("1 ")
                    else:
                        f.write("0 ")
            f.write("\n")  # linebreak for each row
        f.close()