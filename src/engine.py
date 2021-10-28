from data import Data

class Engine():
    def __init__(self) -> None:
        self.file = ''
        self.Data = Data()

    def start(self, filename):
        self.Data.readModel(filename)
        self.Data.calculateBarLength()
        self.Data.setLocalBarVariables()
        self.Data.setStructureStiffnessMatrix()
        #faltou fazer os vetores locais e global de forças