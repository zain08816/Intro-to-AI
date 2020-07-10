import heapq
from .Generator import Generator


class AdaptiveAstar:
    real_matrix = None  # we move in this matrix, but compute the path in the observe_matrix
    observe_matrix = None  # only tracks obstacles the agent has seem so far.

    openSet = None
    closeSet = []
    counter = 0
    o_goal = None  # goal state in the observe_matrix
    o_start = None


    # main method to call to run adaptive A star in order to get correct values


    # Init heap here
    def __init__(self):
        self.openSet = BinaryHeapQueue()

    def heuristic(self, point1, point2):  # this is the heuristic function that calculates the manhattan distance
        return abs(point1.xPos - point2.xPos) + abs(point1.yPos - point2.yPos)

    # adaptiveA Heuristic
    def adaptiveHeuristic(self, point):
        return self.o_goal.gVal - point.gVal

    def closeSetReevaluate(self):
        for state in self.closeSet:
            state.newHVal = self.adaptiveHeuristic(state)
            state.fVal = state.gVal + state.newHVal

    # adaptiveA computePath
    def computePath(self):
        gen = Generator()

        while len(self.openSet.elements) and self.o_goal.gVal > self.openSet.peek().fVal:
            tempState = self.openSet.get()
            self.closeSet.append(tempState)

            for neighbors in gen.getNeighbors(self.observe_matrix, tempState):
                if neighbors.search < self.counter:
                    neighbors.gVal = 100000000
                    neighbors.search = self.counter
                if neighbors.gVal > tempState.gVal + self.costOfState(neighbors):  # c(tempState,neighbors)
                    neighbors.gVal = tempState.gVal + self.costOfState(neighbors)
                    neighbors.parent = tempState
                    if neighbors in self.openSet.elements:
                        self.openSet.elements.remove(neighbors)

                    if neighbors.newHVal > 0:
                        neighbors.fVal = neighbors.gVal + neighbors.newHVal
                    else:
                        neighbors.hVal = self.heuristic(self.o_goal, neighbors)
                        neighbors.fVal = neighbors.gVal + neighbors.hVal

                    temp = (2 * neighbors.fVal) - neighbors.gVal
                    neighbors.fVal = temp
                    #
                    self.openSet.put(neighbors)


    def costOfState(self, state):
        if state.isBlocked():
            return 100000000  # if it is blocked, then its cost is a large number
        else:
            return 1

    def generatePath(self, start, goal):
        curr = goal
        prev = goal.parent

        while prev != None and curr != start:
            prev.next = curr
            curr = prev
            prev = prev.parent
            if prev == start:
                prev.next = curr
                break

    def clearPath(self, start, goal):
        curr = goal
        prev = goal.parent

        while prev != None and curr != start:
            curr.parent = None
            curr.next = None
            prev.next = None
            curr = prev
            prev = prev.parent
            if prev == start:
                prev.next = curr
                break

    def traverse(self, start):
        curr = start
        while curr.next != None:
            curr = curr.next

    # adaptiveAstar main method where it runs the method to get the values
    def adaptiveAstar(self, real_start, real_goal):
        reachedTarget = True
        o_start = self.o_start
        o_goal = self.o_goal
        first_start = real_start #this is used to store the very first start position to avoid infinite while loops l8r

        while real_start != real_goal:
            self.openSet.clear()
            self.counter = self.counter + 1
            o_start.gVal = 0
            o_start.search = self.counter
            o_goal.gVal = 100000000
            o_goal.search = self.counter
            self.closeSet = [] # Don't want to empty the closeSet as we need them

            if o_start.newHVal > 0:
                o_start.fVal = o_start.gVal + o_start.newHVal
            else:
                o_start.hVal = self.heuristic(self.o_goal, o_start)
                o_start.fVal = o_start.gVal + o_start.hVal
            self.openSet.put(o_start)

            self.computePath()

            if len(self.openSet.elements) == 0:
                print("Did not reach the target")
                reachedTarget = False
                break

            lastResult = self.openSet.get()
            real_agent = real_start


            self.generatePath(o_start,lastResult)


            # We are moving the agent in the observe_matrix & real_matrix simultaneously
            while o_start != None:

                x = o_start.xPos
                y = o_start.yPos
                prev_agent = real_agent #keeps track of agent's prev state in case we are currently in an obstacle
                real_agent = self.real_matrix[x][y] #the agent is now moved to where the o_agent just moved



                if real_agent.blocked == True:
                    #if agent finds a obstacle in real matrix, update that in agentMatrix
                    self.observe_matrix[real_agent.xPos][real_agent.yPos].blocked = True

                    real_agent = prev_agent # we do not want to start in a blocked state
                    o_start = self.observe_matrix[real_agent.xPos][real_agent.yPos] # safety measure
                    break
                if real_agent == real_goal: # we were able to get the agent from start to goal in reality
                    o_start = self.observe_matrix[real_agent.xPos][real_agent.yPos]
                    real_agent.parent = prev_agent
                    break
                #sometimes we backtrack to the very first start, so do not want to give the very start a parent, or else infinite while loop
                if real_agent != first_start and prev_agent != real_agent and real_agent.parent == None:
                    real_agent.parent = prev_agent
                o_start = o_start.next

            if real_agent is None:
                break

            real_start = real_agent
            # move the agent to where the start state
            # Set the start state to the current agent
            # if the agent is not at the goal state then that means

        if reachedTarget:
            print("Reached Target with Adaptive A*"+"\n")
            return real_start


    def computePathRepeatedAStart(self):
        gen = Generator()

        while len(self.openSet.elements) and self.o_goal.gVal > self.openSet.peek().fVal:
            tempState = self.openSet.get()
            self.closeSet.append(tempState)

            for neighbors in gen.getNeighbors(self.observe_matrix, tempState):
                if neighbors.search < self.counter:
                    neighbors.gVal = 100000000
                    neighbors.search = self.counter
                if neighbors.gVal > tempState.gVal + self.costOfState(neighbors):  # c(tempState,neighbors)
                    neighbors.gVal = tempState.gVal + self.costOfState(neighbors)
                    neighbors.parent = tempState
                    if neighbors in self.openSet.elements:
                        self.openSet.elements.remove(neighbors)
                    neighbors.hVal = self.heuristic(self.o_goal, neighbors)
                    neighbors.fVal = neighbors.gVal + neighbors.hVal
                    # tie breaker
                    temp = (2 * neighbors.fVal) - neighbors.gVal
                    neighbors.fVal = temp
                    #
                    self.openSet.put(neighbors)



    # repeatedAstar method
    def repeatedAstar(self, real_start, real_goal):
        reachedTarget = True
        o_start = self.o_start
        o_goal = self.o_goal
        first_start = real_start #this is used to store the very first start position to avoid infinite while loops l8r

        while real_start != real_goal:
            self.openSet.clear()
            self.counter = self.counter + 1
            o_start.gVal = 0
            o_start.search = self.counter
            o_goal.gVal = 100000000
            o_goal.search = self.counter
            self.closeSet = []
            o_start.hVal = self.heuristic(o_start, o_goal)
            o_start.fVal = o_start.gVal + o_start.hVal
            self.openSet.put(o_start)

            self.computePathRepeatedAStart()

            if len(self.openSet.elements) == 0:
                print("Did not reach the target")
                reachedTarget = False
                break

            lastResult = self.openSet.get()
            real_agent = real_start


            self.generatePath(o_start,lastResult)


            # We are moving the agent in the observe_matrix & real_matrix simultaneously
            while o_start != None:

                x = o_start.xPos
                y = o_start.yPos
                prev_agent = real_agent #keeps track of agent's prev state in case we are currently in an obstacle
                real_agent = self.real_matrix[x][y] #the agent is now moved to where the o_agent just moved



                if real_agent.blocked == True:
                    #if agent finds a obstacle in real matrix, update that in agentMatrix
                    self.observe_matrix[real_agent.xPos][real_agent.yPos].blocked = True

                    real_agent = prev_agent # we do not want to start in a blocked state
                    o_start = self.observe_matrix[real_agent.xPos][real_agent.yPos] # safety measure
                    break
                if real_agent == real_goal: # we were able to get the agent from start to goal in reality
                    o_start = self.observe_matrix[real_agent.xPos][real_agent.yPos]
                    real_agent.parent = prev_agent
                    break
                #sometimes we backtrack to the very first start, so do not want to give the very start a parent, or else infinite while loop
                if real_agent != first_start and prev_agent != real_agent and real_agent.parent == None:
                    real_agent.parent = prev_agent
                o_start = o_start.next

            if real_agent is None:
                break

            real_start = real_agent
            # move the agent to where the start state
            # Set the start state to the current agent
            # if the agent is not at the goal state then that means

        if reachedTarget:
            #print("Reached Target with Repeated Forward A*")
            return real_start


class BinaryHeapQueue:  # priority queue implementation
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item):
        heapq.heappush(self.elements, item)

    def get(self):
        return heapq.heappop(self.elements)

    def peek(self):
        return self.elements[0]
    def clear(self):
        self.elements = []
