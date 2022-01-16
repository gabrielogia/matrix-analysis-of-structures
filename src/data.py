import math
import numpy as np
from src.node import Node
from src.elements.truss import TrussElement
from src.elements.frame import FrameElement

class Data():
    def __init__(self) -> None:
        self.globalCoordinates = []
        self.degreesFree = 0
        self.degreesRestrained = 0
        self.model = ""
        self.nodes = []
        self.elem = []
        self.K = [] #matriz de rigidez da estrutura no sistema global
        self.F = [] #vetor de forças no sistema global
        self.R = [] #vetor de reações no sistema global
        self.filename = ""

    def readModel(self, filename):
        self.filename = filename
        
        with open('bin/data/' + filename) as f:
            marker = None

            for line in f:
                if (line == "#MODEL\n"):
                    marker = "MODEL"
                    continue
                
                if (line == "#NODES\n"):
                    marker = "NODES"
                    continue
                
                if (line == "#ELEMENTS\n"):
                    marker = "ELEMENTS"
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
                    
                if (marker == "ELEMENTS"):
                    string = line.split(",")
                    string[len(string) - 1] = string[len(string) - 1].split('\n')[0]
                    
                    if (self.model == 'truss'):
                        self.elem.append(TrussElement((string[0]), (string[1]), (string[2]), (string[3]), (string[4]), (string[5]), (string[6]), 
                                        (string[7]), (string[8])))
                                    
                    elif (self.model == 'frame'):
                        self.elem.append(FrameElement((string[0]), (string[1]), (string[2]), (string[3]), (string[4]), (string[5]), (string[6]), 
                                        (string[7]), (string[8])))

                    elif (self.model == 'grid'):
                        pass

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
        self.F = np.array([0]*self.degreesFree, dtype=float)
        
        for i in range(len(self.nodes)):
            if (self.nodes[i].coordsGlobal[0] <= self.degreesFree):
                self.F[self.nodes[i].coordsGlobal[0] - 1] = self.nodes[i].Fx

            if (self.nodes[i].coordsGlobal[1] <= self.degreesFree):
                self.F[self.nodes[i].coordsGlobal[1] - 1] = self.nodes[i].Fy
            
            if (self.model == 'frame'):    
                if (self.nodes[i].coordsGlobal[2] <= self.degreesFree):
                    self.F[self.nodes[i].coordsGlobal[2] - 1] = self.nodes[i].Fz
    
    def setLocalBarVariables(self):
        for i in range(len(self.elem)):
            self.elem[i].L = math.sqrt((self.nodes[self.elem[i].Nf - 1].x - self.nodes[self.elem[i].Ni - 1].x)**2 + (self.nodes[self.elem[i].Nf - 1].y - self.nodes[self.elem[i].Ni - 1].y)**2)
            self.elem[i].cos = (self.nodes[self.elem[i].Nf - 1].x - self.nodes[self.elem[i].Ni - 1].x)/self.elem[i].L
            self.elem[i].sin = (self.nodes[self.elem[i].Nf - 1].y - self.nodes[self.elem[i].Ni - 1].y)/self.elem[i].L
            self.elem[i].setEVector(self.nodes[self.elem[i].Ni - 1], self.nodes[self.elem[i].Nf - 1])
            self.elem[i].setRotationMatrix()
            self.elem[i].setLocalStiffnessMatrix()
            
            if (self.model == 'frame'):
                self.elem[i].setFixedEndForceVector()
    
    def setStructureStiffnessMatrix(self):
        self.K = np.zeros((self.degreesFree, self.degreesFree))

        for bar in self.elem:
            for i in range(len(bar.e)):
                for j in range(len(bar.e)):
                    if (bar.e[i] <= self.degreesFree and bar.e[j] <= self.degreesFree):
                        self.K[bar.e[i] - 1][bar.e[j] - 1] = self.K[bar.e[i] - 1][bar.e[j] - 1] + bar.kg[i][j]