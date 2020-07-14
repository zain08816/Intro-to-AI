import heapq
from .Utility import Utility


class AdaptiveAstar:
    real_matrix = None  
    observe_matrix = None 

    openSet = None
    closeSet = []
    counter = 0
    o_goal = None  
    o_start = None



    def __init__(self):
        self.openSet = BinaryHeapQueue()

    def heuristic(self, point1, point2): 
        return abs(point1.xPos - point2.xPos) + abs(point1.yPos - point2.yPos)


    def adaptiveHeuristic(self, point):
        return self.o_goal.gVal - point.gVal

    def closeSetReevaluate(self):
        for state in self.closeSet:
            state.newHVal = self.adaptiveHeuristic(state)
            state.fVal = state.gVal + state.newHVal


    def computePath(self):
        gen = Utility()

        while len(self.openSet.elements) and self.o_goal.gVal > self.openSet.peek().fVal:
            tempState = self.openSet.get()
            self.closeSet.append(tempState)

            for neighbors in gen.getNeighbors(self.observe_matrix, tempState):
                if neighbors.search < self.counter:
                    neighbors.gVal = 99999999
                    neighbors.search = self.counter
                if neighbors.gVal > tempState.gVal + self.costOfState(neighbors):  
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
            return 99999999 
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



    def adaptiveAstar(self, real_start, real_goal):
        reachedTarget = True
        o_start = self.o_start
        o_goal = self.o_goal
        first_start = real_start 

        while real_start != real_goal:
            self.openSet.clear()
            self.counter = self.counter + 1
            o_start.gVal = 0
            o_start.search = self.counter
            o_goal.gVal = 99999999
            o_goal.search = self.counter
            self.closeSet = [] 

            if o_start.newHVal > 0:
                o_start.fVal = o_start.gVal + o_start.newHVal
            else:
                o_start.hVal = self.heuristic(self.o_goal, o_start)
                o_start.fVal = o_start.gVal + o_start.hVal
            self.openSet.put(o_start)

            self.computePath()

            if len(self.openSet.elements) == 0:
                print("I cannot reach the target")
                reachedTarget = False
                break

            lastResult = self.openSet.get()
            real_agent = real_start


            self.generatePath(o_start,lastResult)


            while o_start != None:

                x = o_start.xPos
                y = o_start.yPos
                prev_agent = real_agent 
                real_agent = self.real_matrix[x][y] 



                if real_agent.blocked == True:
                    self.observe_matrix[real_agent.xPos][real_agent.yPos].blocked = True

                    real_agent = prev_agent 
                    o_start = self.observe_matrix[real_agent.xPos][real_agent.yPos]
                    break
                if real_agent == real_goal: 
                    o_start = self.observe_matrix[real_agent.xPos][real_agent.yPos]
                    real_agent.parent = prev_agent
                    break
                if real_agent != first_start and prev_agent != real_agent and real_agent.parent == None:
                    real_agent.parent = prev_agent
                o_start = o_start.next

            if real_agent is None:
                break

            real_start = real_agent

        if reachedTarget:
            print("I reached the target with Adaptive A*"+"\n")
            return real_start


    def computePathRepeatedAStart(self):
        gen = Utility()

        while len(self.openSet.elements) and self.o_goal.gVal > self.openSet.peek().fVal:
            tempState = self.openSet.get()
            self.closeSet.append(tempState)

            for neighbors in gen.getNeighbors(self.observe_matrix, tempState):
                if neighbors.search < self.counter:
                    neighbors.gVal = 9999999
                    neighbors.search = self.counter
                if neighbors.gVal > tempState.gVal + self.costOfState(neighbors):  
                    neighbors.gVal = tempState.gVal + self.costOfState(neighbors)
                    neighbors.parent = tempState
                    if neighbors in self.openSet.elements:
                        self.openSet.elements.remove(neighbors)
                    neighbors.hVal = self.heuristic(self.o_goal, neighbors)
                    neighbors.fVal = neighbors.gVal + neighbors.hVal
                
                    temp = (2 * neighbors.fVal) - neighbors.gVal
                    neighbors.fVal = temp
                
                    self.openSet.put(neighbors)




    def repeatedAstar(self, real_start, real_goal):
        reachedTarget = True
        o_start = self.o_start
        o_goal = self.o_goal
        first_start = real_start

        while real_start != real_goal:
            self.openSet.clear()
            self.counter = self.counter + 1
            o_start.gVal = 0
            o_start.search = self.counter
            o_goal.gVal = 99999999
            o_goal.search = self.counter
            self.closeSet = []
            o_start.hVal = self.heuristic(o_start, o_goal)
            o_start.fVal = o_start.gVal + o_start.hVal
            self.openSet.put(o_start)

            self.computePathRepeatedAStart()

            if len(self.openSet.elements) == 0:
                print("I cannot reach the target")
                reachedTarget = False
                break

            lastResult = self.openSet.get()
            real_agent = real_start


            self.generatePath(o_start,lastResult)

            while o_start != None:

                x = o_start.xPos
                y = o_start.yPos
                prev_agent = real_agent 
                real_agent = self.real_matrix[x][y] 



                if real_agent.blocked == True:
                    self.observe_matrix[real_agent.xPos][real_agent.yPos].blocked = True

                    real_agent = prev_agent 
                    o_start = self.observe_matrix[real_agent.xPos][real_agent.yPos] 
                    break
                if real_agent == real_goal:
                    o_start = self.observe_matrix[real_agent.xPos][real_agent.yPos]
                    real_agent.parent = prev_agent
                    break

                if real_agent != first_start and prev_agent != real_agent and real_agent.parent == None:
                    real_agent.parent = prev_agent
                o_start = o_start.next

            if real_agent is None:
                break

            real_start = real_agent


        if reachedTarget:
            return real_start


class BinaryHeapQueue: 
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
