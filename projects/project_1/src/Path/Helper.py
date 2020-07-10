from .Encoder import Encoder
class Helper():


    def print_path_to(self,state):
        if state.parent == None:
            print("("+str(state.xPos) + "," + str(state.yPos)+")", end = "")
        else:
            self.print_path_to(state.parent)
            print("-> ("+str(state.xPos) + "," + str(state.yPos)+")", end ="")

    def generate_sol_file(self, matrix,state, sol_name):
        encoder = Encoder()

        while state:
            x = state.xPos
            y = state.yPos
            matrix[x][y] = '~'
            state = state.parent
        encoder.sol_encode(matrix,sol_name)


