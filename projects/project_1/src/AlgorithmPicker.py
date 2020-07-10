from Path.RepeatedAstar import RepeatedAstar
from Path.Generator import Generator
from Path.Helper import Helper
from Path.AdaptiveAstar import AdaptiveAstar
import time


class AlgorithmPicker:

    gen = Generator()
    def executeForwardAstar(self,fileName):
        matrix = self.gen.decode(fileName)

        start = self.gen.startState
        goal = self.gen.goalState

        agent_matrix = self.gen.generateAgentMatrix(matrix, start)
        
        agent_start = agent_matrix[start.xPos][start.yPos]
        agent_goal = agent_matrix[goal.xPos][goal.yPos]
        algo = RepeatedAstar()

        algo.real_matrix = matrix
        algo.observe_matrix = agent_matrix
        algo.o_start = agent_start
        algo.o_goal = agent_goal

        state = algo.repeatedAstar(start, goal)

        helper = Helper()
        helper.generate_sol_file(matrix, state, "Forward_A*_sol")

    def executeBackwardsAStar(self, fileName):
        matrix = self.gen.decode(fileName)

        start = self.gen.goalState
        goal = self.gen.startState

        agent_matrix = self.gen.generateAgentMatrix(matrix, start)

        agent_start = agent_matrix[start.xPos][start.yPos]
        agent_goal = agent_matrix[goal.xPos][goal.yPos]
        algo = RepeatedAstar()

        algo.real_matrix = matrix
        algo.observe_matrix = agent_matrix
        algo.o_start = agent_start
        algo.o_goal = agent_goal

        state = algo.repeatedAstar(start, goal)

        helper = Helper()
        helper.generate_sol_file(matrix, state, "Backwards_A*_sol")

    def executeAdaptiveAStar(self, fileName):
        matrix = self.gen.decode(fileName)

        start = self.gen.goalState
        goal = self.gen.startState

        agent_matrix = self.gen.generateAgentMatrix(matrix, start)

        agent_start = agent_matrix[start.xPos][start.yPos]
        agent_goal = agent_matrix[goal.xPos][goal.yPos]

        algo = AdaptiveAstar()

        algo.real_matrix = matrix
        algo.observe_matrix = agent_matrix
        algo.o_start = agent_start
        algo.o_goal = agent_goal

       # startTime = time.time()
        state = algo.repeatedAstar(start, goal)
        #endTime = time.time()
        #print("Time " + str(endTime - startTime))

        algo.closeSetReevaluate()
        # algo.clearPath(start, goal)

        if state:
            #startTime = time.time()
            state = algo.adaptiveAstar(start, goal)
            #endTime = time.time()
            #print("Time " + str(endTime - startTime))

        helper = Helper()
        helper.generate_sol_file(matrix, state, "Adaptive_A*_sol")

