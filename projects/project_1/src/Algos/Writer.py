# class Writer():


#     # def print_path_to(self,state):
#     #     if state.parent == None:
#     #         print("("+str(state.xPos) + "," + str(state.yPos)+")", end = "")
#     #     else:
#     #         self.print_path_to(state.parent)
#     #         print("-> ("+str(state.xPos) + "," + str(state.yPos)+")", end ="")

#     def generate_sol_file(self, matrix,state, sol_name):
#         encoder = Encoder()

#         while state:
#             x = state.xPos
#             y = state.yPos
#             matrix[x][y] = '~'
#             state = state.parent
#         encoder.sol_encode(matrix,sol_name)


# class Encoder:
#     def encode(self, matrix, filename, startX, startY, goalX, goalY):
#         rows = len(matrix)
#         cols = len(matrix[0])
#         f = open(filename, "w+")

    
#         f.write(str(rows) +"x" + str(cols) +
#                 " start("+str(startX)+","+str(startY)+")" +
#                 " goal(" + str(goalX) + "," + str(goalY) + ")" + "\n" )
#         f.write("\n")



#         for row in range(rows):
#             for col in range(cols):
#                 state = matrix[row][col]
#                 if(state.isBlocked()): 
#                     f.write("1 ")
#                 else:
#                     f.write("0 ")
#             f.write("\n") 
#         f.close()

#     def sol_encode(self, matrix, filename):
#         rows = len(matrix)
#         cols = len(matrix[0])
#         f = open(filename, "w+")

#         for row in range(rows):
#             for col in range(cols):
#                 if matrix[row][col] == '~':
#                     f.write("' ")
#                 else:
#                     state = matrix[row][col]
#                     if (state.isBlocked()): 
#                         f.write("1 ")
#                     else:
#                         f.write("0 ")
#             f.write("\n")  
#         f.close()