import numpy as np
from numpy.core.fromnumeric import transpose

class Solver():
    def __init__(self, data) -> None:
        self.d = []
        self.data = data

    def setReactionsValues(self):
        self.data.R = np.zeros((self.data.degreesRestrained))

        for i in range(len(self.data.elem)):
            for j in range(len(self.data.elem[i].e)):
                if (self.data.elem[i].e[j] > self.data.degreesFree):
                    self.data.R[self.data.elem[i].e[j] - self.data.degreesFree - 1] += self.data.elem[i].f[j]

    def calculateForcesGlobalCoordinateSystem(self):
        for i in range(len(self.data.elem)):
            self.data.elem[i].f =  np.dot(transpose(self.data.elem[i].R), self.data.elem[i].q)

    def calculateForcesLocalCoordinateSystem(self):
        for i in range(len(self.data.elem)):
            self.data.elem[i].q =  np.dot(self.data.elem[i].kl, self.data.elem[i].u)

    def calculateDiscplacementsLocalCoordinateSystem(self):
        for i in range(len(self.data.elem)):
            self.data.elem[i].u = np.dot(self.data.elem[i].R, self.data.elem[i].v)

    def calculateDiscplacementsGlobalCoordinateSystem(self):
        for i in range(len(self.data.elem)):
            self.data.elem[i].v = np.zeros(len(self.data.elem[i].e))
            for j in range(len(self.data.elem[i].e)):
                if (self.data.elem[i].e[j] <= self.data.degreesFree):
                    self.data.elem[i].v[j] = self.d[self.data.elem[i].e[j] - 1]

    def calculateMembersForcesAndDisplacements(self):
        self.calculateDiscplacementsGlobalCoordinateSystem()
        self.calculateDiscplacementsLocalCoordinateSystem()
        self.calculateForcesLocalCoordinateSystem()
        self.calculateForcesGlobalCoordinateSystem()

    def calculateNodalDisplacements(self):
        self.d = np.linalg.solve(self.data.K, self.data.F)
        
    def solve(self):
        self.calculateNodalDisplacements()
        self.calculateMembersForcesAndDisplacements()
        self.setReactionsValues()