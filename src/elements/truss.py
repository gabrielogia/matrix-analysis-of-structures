import numpy as np
from numpy.core.fromnumeric import transpose

class TrussElement():
    def __init__(self, id = 0, Ni = 0, Nf = 0, E = 0, A = 0, I = 0, D = 0, dirLoad = 0, Qx = 0, Qy = 0) -> None:
        self.id = int(id)
        self.Ni = int(Ni)
        self.Nf = int(Nf)
        self.E = float(E)
        self.A = float(A)
        self.I = float(I)
        self.D = float(D)
        self.dirLoad = dirLoad
        self.Qx = float(Qx)
        self.Qy = float(Qy)
        self.L = 0.0
        self.cos = 0.0
        self.sin = 0.0
        self.ml = [] #matriz de massa da barra no sistema local
        self.mg = [] #matriz de massa da barra no sistema global
        self.kl = [] #matriz de rigidez da barra no sistema local
        self.kg = [] #matriz de rigidez da barra no sistema global
        self.e = [] #vetor de espaçamento
        self.R = [] #matriz de rotacao
        self.v = [] #deslocamento nas coordenadas globais
        self.u = [] #deslocamento nas coordenadas locais
        self.q = [] #forças no sistema de coordenadas local
        self.f = [] #forças no sistema de coordenadas global

    def setEVector(self, Ni, Nf):
        self.e = Ni.coordsGlobal + Nf.coordsGlobal
        
    def setLocalMassMatrix(self):
        c = self.D*self.A*self.L/6
        
        self.ml = np.array([[2*c, 0, c, 0],
                            [0, 2*c, 0, c],
                            [c, 0, 2*c, 0],
                            [0, c, 0, 2*c]])
        
        self.mg = np.dot(np.dot(transpose(self.R), self.ml), self.R)

    def setLocalStiffnessMatrix(self):
        self.kl = np.array([[(self.E*self.A)/self.L, 0, -(self.E*self.A)/self.L, 0],
                            [0, 0, 0, 0],
                            [-(self.E*self.A)/self.L, 0, (self.E*self.A)/self.L, 0],
                            [0, 0, 0, 0]])
        
        self.kg = np.dot(np.dot(transpose(self.R), self.kl), self.R)
    
    def setRotationMatrix(self):
        self.R = np.array([[self.cos, self.sin, 0, 0],
                            [-self.sin, self.cos, 0, 0], 
                            [0, 0, self.cos, self.sin,], 
                            [0, 0, -self.sin, self.cos,]])