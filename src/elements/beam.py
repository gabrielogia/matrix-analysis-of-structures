import numpy as np
from numpy.core.fromnumeric import transpose

class BeamElement():
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
        self.qf = [] #forças distribuidas convertidas para nodais no sistema de coordenadas local
        self.qfg = [] #forças distribuidas convertidas para nodais no sistema de coordenadas global
        self.f = [] #forças no sistema de coordenadas global

    def setEVector(self, Ni, Nf):
        self.e = Ni.coordsGlobal + Nf.coordsGlobal

    def setLocalStiffnessMatrix(self):
        c = self.E*self.I/(self.L**3)
        
        self.kl = c*np.array([[12, 6*self.L, -12, 6*self.L],
                            [6*self.L, 4*self.L**2, -6*self.L, 2*self.L**2],
                            [-12, -6*self.L, 12, -6*self.L],
                            [6*self.L, 2*self.L**2, -6*self.L, 4*self.L**2]])
        
        self.kg = self.kl
    
    def setLocalMassMatrix(self):
        c = self.D*self.A*self.L/420
        
        self.ml = c*np.array([[156, 22*self.L, 54, -13*self.L],
                            [22*self.L, 4*self.L**2, 13*self.L, -3*self.L**2],
                            [54, 13*self.L, 156, -22*self.L],
                            [-13*self.L, -3*self.L**2, -22*self.L, 4*self.L**2]])
        
        self.mg = self.ml
        
    def setRotationMatrix(self):
        self.R = np.array([[self.cos, self.sin, 0, 0, 0, 0],
                            [-self.sin, self.cos, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0], 
                            [0, 0, 0, self.cos, self.sin, 0], 
                            [0, 0, 0, -self.sin, self.cos, 0],
                            [0, 0, 0, 0, 0, 1]])
    
    def setFixedEndForceVector(self):
        self.qf = np.array([-self.Qx*self.L/2, -self.Qy*self.L/2, (-self.Qy*self.L**2)/12, -self.Qx*self.L/2, -self.Qy*self.L/2, (self.Qy*self.L**2)/12])
        
        if (self.dirLoad == 'local'):
            self.qfg = np.dot(transpose(self.R), self.qf)