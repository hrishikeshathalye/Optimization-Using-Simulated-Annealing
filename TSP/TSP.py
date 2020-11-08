import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import random

def animateTSP(history, points):
    key_frames_mult = len(history) // 1500
    fig, ax = plt.subplots()
    ''' path is a line coming through all the nodes '''
    line, = plt.plot([], [], lw=2)
    def init():
        ''' initialize node dots on graph '''
        x = [points[i][0] for i in history[0]]
        y = [points[i][1] for i in history[0]]
        plt.plot(x, y, 'ro')

        ''' draw axes slighty bigger  '''
        extra_x = (max(x) - min(x)) * 0.05
        extra_y = (max(y) - min(y)) * 0.05
        ax.set_xlim(min(x) - extra_x, max(x) + extra_x)
        ax.set_ylim(min(y) - extra_y, max(y) + extra_y)

        '''initialize solution to be empty '''
        line.set_data([], [])
        return line,

    def update(frame):
        ''' for every frame update the solution on the graph '''
        x = [points[i, 0] for i in history[frame] + [history[frame][0]]]
        y = [points[i, 1] for i in history[frame] + [history[frame][0]]]
        line.set_data(x, y)
        return line

    ''' animate precalulated solutions '''
    init()
    ani = FuncAnimation(fig, update, frames=range(0, len(history), 10), interval=1, repeat=False)
    plt.show()

def nearestNeighbours(distMatrix):
    '''
    Computes solution using nearest neighbour strategy
    '''
    initialNode = random.randint(0, len(distMatrix)-1)
    resultList = [initialNode]
    currnode = initialNode

    visitList = list(range(len(distMatrix)))
    visitList.remove(initialNode)

    while visitList:
        nearestNeighbour = min([(distMatrix[currnode][j], j) for j in visitList], key=lambda tmp: tmp[0])
        currnode = nearestNeighbour[1]
        visitList.remove(currnode)
        resultList.append(currnode)

    return resultList

def getDistMatrix(coords):
    '''
    Create the distance matrix
    '''
    return np.sqrt((np.square(coords[:, np.newaxis] - coords).sum(axis=2)))

#Returning a list of tuples of coordinates
def randomMapGen(width, height, numberOfNodes):
    yCoordinates = np.random.randint(height, size=numberOfNodes)
    xCoordinates = np.random.randint(width, size=numberOfNodes)
    return np.array(list(zip(xCoordinates, yCoordinates)))

class TSPSolver:
    def __init__(self, coords, startingTemp, finalTemp, alpha):
        self.coords = coords
        self.numPoints = len(coords)
        self.currTemp = startingTemp
        self.finalTemp = finalTemp
        self.alpha = alpha
        self.currIteration = 1

        self.distMatrix = getDistMatrix(coords)
        self.currSoln = nearestNeighbours(self.distMatrix)
        self.bestSoln = self.currSoln
        self.solutions = [self.currSoln]

        self.currCost = self.costOfSolution(self.currSoln)
        self.initialCost = self.currCost
        self.minCost = self.currCost
        self.costList = [self.currCost]
        print('Initial Cost (Nearest Neighbours Solution): ', self.currCost)

    def probFunction(self, cost):
        return 1/(1+np.exp(-cost/self.currTemp))
    
    def costOfSolution(self, solution):
        return sum([self.distMatrix[i, j] for i, j in zip(solution, solution[1:] + [solution[0]])])

    def acceptSoln(self, candidateSoln):
        candidateSolutionCost = self.costOfSolution(candidateSoln)
        if(candidateSolutionCost < self.currCost):
            self.currCost = candidateSolutionCost
            self.currSoln = candidateSoln
            if candidateSolutionCost < self.minCost:
                self.minCost = candidateSolutionCost
                self.bestSoln = candidateSoln
        else:
            if(random.random() <= self.probFunction(candidateSolutionCost)):
                self.currCost = candidateSolutionCost
                self.currSoln = candidateSoln
        self.costList.append(self.currCost)
        self.solutions.append(self.currSoln.copy())

    def simulatedAnnealing(self):
        '''
        Uses 2 opt heuristic combined with simulated annealing for accepting solution
        '''
        while (self.currTemp-0.0001 >= self.finalTemp):
            for i in range(0, 1+math.ceil(self.currTemp/10)):
                candidateSoln = self.currSoln
                point1 = random.randint(2, self.numPoints - 1)
                point2 = point1 + random.randint(0, self.numPoints - point1)
                candidateSoln[point1: point2] = list(reversed(candidateSoln[point1: point2]))
                self.acceptSoln(candidateSoln)
                self.currTemp *= self.alpha
                self.currIteration += 1

        print('Minimum Cost Of Tour: ', self.minCost)

    def animateSolutions(self):
        animateTSP(self.solutions, self.coords)

    def plotLearning(self):
        plt.plot([i for i in range(len(self.costList))], self.costList)
        line_init = plt.axhline(y=self.initialCost, color='r', linestyle='--')
        line_min = plt.axhline(y=self.minCost, color='g', linestyle='--')
        plt.legend([line_init, line_min], ['Initial Cost', 'Final Cost'])
        plt.ylabel('Cost')
        plt.xlabel('Iteration')
        plt.show()

if __name__ == "__main__":
    '''set the simulated annealing algorithm params'''
    print("Set Following Parameters:")
    gridHeight = float(input("Grid Height:\n"))
    gridWidth = float(input("Grid Width:\n"))
    numberOfNodes = int(input("Number of nodes:\n"))
    initialTemp = float(input("Initial Temperature:\n"))
    finalTemp = float(input("Final Temperature:\n"))
    # innerIter = int(input("No of times to run inner loop:\n"))
    alpha = float(input("Temperature reduction parameter (alpha):\n"))
    #Random nodes generated in the domain
    TSPmap = randomMapGen(gridWidth, gridHeight, numberOfNodes)
    s = TSPSolver(TSPmap, initialTemp, finalTemp, alpha)
    s.simulatedAnnealing()
    s.animateSolutions()
    s.plotLearning()
