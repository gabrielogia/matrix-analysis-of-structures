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
        self.data.setLocalBarVariables()
        self.data.setStructureMatrices()
        self.data.setGlobalForceVector()
        
        if (self.data.analysisType != 'dynamic'):
            self.solver = StaticSolver(self.data)
            
        else:
            self.solver = DynamicSolver(self.data)
            
        self.solver.solve()        
        #self.output.printResults(self.data)