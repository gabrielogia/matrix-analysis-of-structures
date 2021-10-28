import math
import numpy as np
from src.node import Node
from src.bar import Bar

class Data():
    def __init__(self) -> None:
        self.nodes = []
        self.bars = []
        self.K = [] #matriz de rigidez da estrutura no sistema global

    def readModel(self, filename):
        with open('data/' + filename) as f:
            marker = None

            for line in f:

                if (line == "#NODES\n"):
                    marker = "NODES"
                    continue
                
                if (line == "#BARS\n"):
                    marker = "BARS"
                    continue

                if (line == "\n"):
                    marker = None
                    continue

                if (marker == "NODES"):
                    string = line.split("   ")
                    string[len(string) - 1] = string[len(string) - 1].split('\n')[0]
                    
                    self.nodes.append(Node((string[0]), (string[1]), (string[2]), (string[3]), (string[4]), (string[5]), (string[6]), 
                                        (string[7]), (string[8]), (string[9]), (string[10]), (string[11])))
                    
                if (marker == "BARS"):
                    string = line.split("   ")
                    string[len(string) - 1] = string[len(string) - 1].split('\n')[0]
                    
                    self.bars.append(Bar((string[0]), (string[1]), (string[2]), (string[3]), (string[4]), (string[5]), (string[6]), 
                                        (string[7]), (string[8]), (string[9]), (string[10])))

    def calculateBarLength(self):
        for i in range(len(self.bars)):
            self.bars[i].L = math.sqrt((self.nodes[self.bars[i].Nf - 1].x - self.nodes[self.bars[i].Ni - 1].x)**2 + (self.nodes[self.bars[i].Nf - 1].y - self.nodes[self.bars[i].Ni - 1].y)**2)
            self.bars[i].cos = (self.nodes[self.bars[i].Nf - 1].x - self.nodes[self.bars[i].Ni - 1].x)/self.bars[i].L
            self.bars[i].sin = (self.nodes[self.bars[i].Nf - 1].y - self.nodes[self.bars[i].Ni - 1].y)/self.bars[i].L

    def setLocalBarVariables(self):
        for i in range(len(self.bars)):
            self.bars[i].setEVector(self.nodes[self.bars[i].Ni - 1], self.nodes[self.bars[i].Nf - 1])
            self.bars[i].setRotationMatrix()
            self.bars[i].setLocalStiffnessMatrix()
    
    def setStructureStiffnessMatrix(self):
        self.K = np.zeros((len(self.nodes)*3, len(self.nodes)*3))

        for bar in self.bars:
            for i in range(6):
                for j in range(6):
                    self.K[bar.e[i] - 1][bar.e[j] - 1] = self.K[bar.e[i] - 1][bar.e[j] - 1] + bar.kg[i][j]

        for i in range(len(self.K)):
            for j in range(len(self.K[i])):
                print("%f   " %(self.K[i][j]), end="")
            print('\n')