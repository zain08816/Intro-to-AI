from Algos.RepeatedAstar import RepeatedAstar
from Algos.Utility import Utility
from Algos.Utility import State
from Algos.Utility import Writer
from Algos.AdaptiveAstar import AdaptiveAstar
import time
import sys

def executeForwardAStar(fileName, write=True):
    util = Utility()
    matrix = util.decode(fileName)

    start = util.startState
    goal = util.goalState

    agent_matrix = util.generateAgentMatrix(matrix, start)
    
    agent_start = agent_matrix[start.xPos][start.yPos]
    agent_goal = agent_matrix[goal.xPos][goal.yPos]
    algo = RepeatedAstar()

    algo.real_matrix = matrix
    algo.observe_matrix = agent_matrix
    algo.o_start = agent_start
    algo.o_goal = agent_goal

    state = algo.repeatedAstar(start, goal)

    if write:    
        writer = Writer()
        writer.generate_sol_file(matrix, state, "Forward_A*_sol")

def executeBackwardsAStar(fileName, write=True):
    util = Utility()
    matrix = util.decode(fileName)

    start = util.goalState
    goal = util.startState

    agent_matrix = util.generateAgentMatrix(matrix, start)

    agent_start = agent_matrix[start.xPos][start.yPos]
    agent_goal = agent_matrix[goal.xPos][goal.yPos]
    algo = RepeatedAstar()

    algo.real_matrix = matrix
    algo.observe_matrix = agent_matrix
    algo.o_start = agent_start
    algo.o_goal = agent_goal

    state = algo.repeatedAstar(start, goal)

    if write:
        writer = Writer()
        writer.generate_sol_file(matrix, state, "Backwards_A*_sol")

def executeAdaptiveAStar(fileName, write=True):
    util = Utility()
    matrix = util.decode(fileName)

    start = util.startState
    goal = util.goalState

    agent_matrix = util.generateAgentMatrix(matrix, start)

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

    if state:
        #startTime = time.time()
        state = algo.adaptiveAstar(start, goal)
        #endTime = time.time()
        #print("Time " + str(endTime - startTime))

    if write:
        writer = Writer()
        writer.generate_sol_file(matrix, state, "Adaptive_A*_sol")


if __name__ == '__main__':

        startTimeF = time.time()
        for i in range(50):
            executeForwardAStar("resources/map"+str(i))
        endTimeF = time.time()

        startTimeB = time.time()
        for i in range(50):
            executeAdaptiveAStar("resources/map"+str(i), False)
        endTimeB = time.time()

        print("Time to complete Forward A*: ", str(endTimeF - startTimeF)+"s")
        print("Time to complete Adaptive A*: ", str(endTimeB - startTimeB)+"s")

        print(sys.getsizeof(bool()))

        # for i in range(1):
        #     print("Executing Adaptive on Map" + str(i))
        #     executeAdaptiveAStar("resources/map"+str(i))
            


        # for i in range(10):
        #     print("Executing Forward on Map"+str(i))
        #     executeForwardAStar("resources/map"+str(i))
        #     print("Executing Backwards on Map" + str(i))
        #     executeBackwardsAStar("resources/map"+str(i))
        #     print("Executing Adaptive on Map" + str(i))
        #     executeAdaptiveAStar("resources/map"+str(i))




