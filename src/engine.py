import numpy as np
import multiprocessing

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
    
    def test_multiproc(self, dano):
        a = 10
        damage = (a**dano - 1)/(a - 1)
        #damage = 1/(1 + (dano/(dano - 1))**-2)
        damage = 1/(1 + ((3*dano)/(dano - 1))**-2)
        #damage = dano
        
        for i in range(0, len(self.data.elem) + 1):
            self.data.setLocalBarVariables(i, damage)
            self.data.setStructureMatrices()
            self.data.setGlobalForceVector()
            
            if (self.data.analysisType != 'dynamic'):
                self.solver = StaticSolver(self.data)
                
            else:
                self.solver = DynamicSolver(self.data)
            
            self.solver.solve(i, damage)        
        #self.output.printResults(self.data)

    def start(self, filename):
        self.data.readModel(filename)
        self.data.setGlobalCoordinates()
        
        damages = np.linspace(0.01, 0.99, 200)
        
        for i in range(0, len(damages), 5):
            danos = damages[i:i+5]
        
            pool = multiprocessing.Pool(5)
            pool.map(self.test_multiproc, danos)
            pool.close()