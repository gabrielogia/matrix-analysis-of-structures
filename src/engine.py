import numpy as np

from src.data import Data
from src.solvers.static import StaticSolver
from src.solvers.dynamic import DynamicSolver
from src.output import Output

class Engine():
    def __init__(self) -> None:
        self.file = ''
        self.data = Data()
        self.solver = ''
        self.output = Output()

    def start(self, filename):
        self.data.readModel(filename)
        self.data.setGlobalCoordinates()
        
        damages = np.linspace(0.01, 0.99, 100)
        
        for j in range(0, len(damages)):
            for i in range(0, len(self.data.elem) + 1):
                self.data.setLocalBarVariables(i, damages[j])
                self.data.setStructureMatrices()
                self.data.setGlobalForceVector()
                
                if (self.data.analysisType != 'dynamic'):
                    self.solver = StaticSolver(self.data)
                    
                else:
                    self.solver = DynamicSolver(self.data)
                
                self.solver.solve(i, damages[j])        
        #self.output.printResults(self.data)