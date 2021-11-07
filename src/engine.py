from src.data import Data
from src.solver import Solver

class Engine():
    def __init__(self) -> None:
        self.file = ''
        self.data = Data()
        self.solver = Solver()

    def start(self, filename):
        self.data.readModel(filename)
        self.data.setGlobalCoordinates()
        #RECOMEÇAR A PARTIR DAQUI
        #self.data.setLocalBarVariables()
        #self.data.setStructureStiffnessMatrix()
        #self.solver.solve(self.data)
        
        #faltou fazer os vetores locais e global de forças