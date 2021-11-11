import numpy as np
from numpy.core.fromnumeric import transpose

class Solver():
    def __init__(self, data) -> None:
        self.d = []
        self.data = data

    def setReactionsValues(self):
        self.data.R = np.zeros((self.data.degreesRestrained))

        for i in range(len(self.data.bars)):
            for j in range(len(self.data.bars[i].e)):
                if (self.data.bars[i].e[j] > self.data.degreesFree):
                    self.data.R[self.data.bars[i].e[j] - self.data.degreesFree - 1] = self.data.bars[i].q[j]
        
        print(self.data.R)

    def calculateForcesGlobalCoordinateSystem(self):
        for i in range(len(self.data.bars)):
            self.data.bars[i].q =  np.dot(transpose(self.data.bars[i].R), self.data.bars[i].q)

    def calculateForcesLocalCoordinateSystem(self):
        for i in range(len(self.data.bars)):
            self.data.bars[i].q =  np.dot(self.data.bars[i].kl, self.data.bars[i].u)

    def calculateDiscplacementsGlobalCoordinateSystem(self):
        for i in range(len(self.data.bars)):
            self.data.bars[i].u = np.dot(self.data.bars[i].R, self.data.bars[i].v)

    def calculateDiscplacementsLocalCoordinateSystem(self):
        for i in range(len(self.data.bars)):
            self.data.bars[i].v = np.zeros(len(self.data.bars[i].e))
            for j in range(len(self.data.bars[i].e)):
                if (self.data.bars[i].e[j] <= self.data.degreesFree):
                    self.data.bars[i].v[j] = self.d[self.data.bars[i].e[j] - 1]

    def calculateMembersForcesAndDisplacements(self):
        self.calculateDiscplacementsLocalCoordinateSystem()
        self.calculateDiscplacementsGlobalCoordinateSystem()
        self.calculateForcesLocalCoordinateSystem()
        self.calculateForcesGlobalCoordinateSystem()

    def calculateNodalDisplacements(self):
        self.d = np.linalg.solve(self.data.K, self.data.F)
        
    def solve(self):
        self.calculateNodalDisplacements()
        self.calculateMembersForcesAndDisplacements()
        self.setReactionsValues()