from src.data import Data
from src.solver import Solver

class Engine():
    def __init__(self) -> None:
        self.file = ''
        self.data = Data()
        self.solver = Solver(self.data)

    def start(self, filename):
        self.data.readModel(filename)
        self.data.setGlobalCoordinates()
        self.data.setGlobalForceVector()
        self.data.setLocalBarVariables()
        self.data.setStructureStiffnessMatrix()
        self.solver.solve()