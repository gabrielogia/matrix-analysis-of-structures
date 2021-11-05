import numpy as np

class Solver():
    def __init__(self) -> None:
        self.Kll = []
        self.Kfl = []
        self.Fl = []
        self.Ff = []
        self.Dl = []
        self.freeCoords = []
        self.lockedCoords = []

    def calculateFf(self):
        self.Ff = np.dot(self.Kfl, self.Dl)

    def setKfl(self, data):
        self.Kfl = np.zeros((len(self.lockedCoords), len(self.freeCoords)))
        
        for i in range(0, len(self.lockedCoords)):
            for j in range(0, len(self.freeCoords)):
                self.Kfl[i][j] = data.K[self.lockedCoords[i] - 1][self.freeCoords[j] - 1]

    def calculateDl(self):
        self.Dl = np.linalg.solve(self.Kll, self.Fl)

    def setFl(self, data):
        self.Fl = np.zeros(len(self.freeCoords))

        for i in range(0, len(self.freeCoords)):
            self.Fl[i] = data.F[self.freeCoords[i] - 1]

    def setKll(self, data):
        self.Kll = np.zeros((len(self.freeCoords), len(self.freeCoords)))
        
        for i in range(0, len(self.freeCoords)):
            for j in range(0, len(self.freeCoords)):
                self.Kll[i][j] = data.K[self.freeCoords[i] - 1][self.freeCoords[j] - 1]

    def setDisplacementRestriction(self, data):
        for i in range(len(data.nodes)):
            if (data.nodes[i].supX == 1):
                self.lockedCoords.append(data.nodes[i].coordsGlobal[0])
            else:
                self.freeCoords.append(data.nodes[i].coordsGlobal[0])

            if (data.nodes[i].supY == 1):
                self.lockedCoords.append(data.nodes[i].coordsGlobal[1])
            else:
                self.freeCoords.append(data.nodes[i].coordsGlobal[1])

            if (data.nodes[i].supZ == 1):
                self.lockedCoords.append(data.nodes[i].coordsGlobal[2])
            else:
                self.freeCoords.append(data.nodes[i].coordsGlobal[2])

    def solve(self, data):
        self.setDisplacementRestriction(data)
        self.setKll(data)
        self.setFl(data)
        self.calculateDl()
        self.setKfl(data)
        self.calculateFf()

        print(self.Kll)
        print(self.Fl)
        print(self.Dl)
        print(self.Kfl)
        print(self.Ff)