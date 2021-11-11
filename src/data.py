import math
import numpy as np
from src.node import Node
from src.bar import Bar

class Data():
    def __init__(self) -> None:
        self.globalCoordinates = []
        self.degreesFree = 0
        self.degreesRestrained = 0
        self.model = ""
        self.nodes = []
        self.bars = []
        self.K = [] #matriz de rigidez da estrutura no sistema global
        self.F = [] #vetor de forças no sistema global
        self.R = [] #vetor de reações no sistema global

    def readModel(self, filename):
        with open('data/' + filename) as f:
            marker = None

            for line in f:
                if (line == "#MODEL\n"):
                    marker = "MODEL"
                    continue
                
                if (line == "#NODES\n"):
                    marker = "NODES"
                    continue
                
                if (line == "#BARS\n"):
                    marker = "BARS"
                    continue

                if (line == "\n"):
                    marker = None
                    continue

                if (marker == "MODEL"):
                    self.model = line.split('\n')[0]

                if (marker == "NODES"):
                    string = line.split(",")
                    string[len(string) - 1] = string[len(string) - 1].split('\n')[0]
                    
                    self.nodes.append(Node((string[0]), (string[1]), (string[2]), (string[3]), (string[4]), (string[5]), (string[6]), 
                                        (string[7]), (string[8]), (string[9]), (string[10]), (string[11]), self.model))
                    
                if (marker == "BARS"):
                    string = line.split(",")
                    string[len(string) - 1] = string[len(string) - 1].split('\n')[0]
                    
                    self.bars.append(Bar((string[0]), (string[1]), (string[2]), (string[3]), (string[4]), (string[5]), (string[6]), 
                                        (string[7]), (string[8])))

    def setGlobalCoordinates(self):
        degreesFree = 0
        degreesRestrained = 0

        if (self.model == 'truss'):
            self.globalCoordinates = [0]*(len(self.nodes)*2)
        else:
            self.globalCoordinates = [0]*(len(self.nodes)*3)

        for i in range(0, len(self.nodes)):
            f, r = self.nodes[i].countDegrees()
            degreesFree += f
            degreesRestrained += r

        k = 1
        for i in range(0, len(self.nodes)):
            k = self.nodes[i].setFreeGlobalCoordinates(k)

        k = 1 + degreesFree
        for i in range(0, len(self.nodes)):
            k = self.nodes[i].setRestrainedGlobalCoordinates(k)

        for i in range(0, len(self.nodes)):
            self.globalCoordinates[2*i] = self.nodes[i].coordsGlobal[0]
            self.globalCoordinates[2*i+1] = self.nodes[i].coordsGlobal[1]

        self.degreesFree = degreesFree
        self.degreesRestrained = degreesRestrained

    def setGlobalForceVector(self):
        self.F = np.array([0]*self.degreesFree)
        
        for i in range(len(self.nodes)):
            if (self.nodes[i].coordsGlobal[0] <= self.degreesFree):
                self.F[self.nodes[i].coordsGlobal[0] - 1] = self.nodes[i].Fx

            if (self.nodes[i].coordsGlobal[1] <= self.degreesFree):
                self.F[self.nodes[i].coordsGlobal[1] - 1] = self.nodes[i].Fy
    
    def setLocalBarVariables(self):
        for i in range(len(self.bars)):
            self.bars[i].L = math.sqrt((self.nodes[self.bars[i].Nf - 1].x - self.nodes[self.bars[i].Ni - 1].x)**2 + (self.nodes[self.bars[i].Nf - 1].y - self.nodes[self.bars[i].Ni - 1].y)**2)
            self.bars[i].cos = (self.nodes[self.bars[i].Nf - 1].x - self.nodes[self.bars[i].Ni - 1].x)/self.bars[i].L
            self.bars[i].sin = (self.nodes[self.bars[i].Nf - 1].y - self.nodes[self.bars[i].Ni - 1].y)/self.bars[i].L
            self.bars[i].setEVector(self.nodes[self.bars[i].Ni - 1], self.nodes[self.bars[i].Nf - 1])
            self.bars[i].setRotationMatrix()
            self.bars[i].setLocalStiffnessMatrix()
    
    def setStructureStiffnessMatrix(self):
        self.K = np.zeros((self.degreesFree, self.degreesFree))

        for bar in self.bars:
            for i in range(len(bar.e)):
                for j in range(len(bar.e)):
                    if (bar.e[i] <= self.degreesFree and bar.e[j] <= self.degreesFree):
                        self.K[bar.e[i] - 1][bar.e[j] - 1] = self.K[bar.e[i] - 1][bar.e[j] - 1] + bar.kg[i][j]

        # for i in range(len(self.K)):
        #     for j in range(len(self.K[i])):
        #         print("%.2f   " %(self.K[i][j]), end="")
        #     print('\n')