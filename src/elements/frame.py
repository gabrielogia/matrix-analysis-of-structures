import numpy as np
from numpy.core.fromnumeric import transpose

class FrameElement():
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
        self.kl = np.array([[(self.E*self.A)/self.L, 0, 0, -(self.E*self.A)/self.L, 0, 0],
                            [0, (12*self.E*self.I)/(self.L**3), (6*self.E*self.I)/(self.L**2), 0, -(12*self.E*self.I)/(self.L**3), (6*self.E*self.I)/(self.L**2)],
                            [0, (6*self.E*self.I)/(self.L**2), (4*self.E*self.I)/(self.L), 0, -(6*self.E*self.I)/(self.L**2), (2*self.E*self.I)/(self.L)],
                            [-(self.E*self.A)/self.L, 0, 0, (self.E*self.A)/self.L, 0, 0],
                            [0, -(12*self.E*self.I)/(self.L**3), -(6*self.E*self.I)/(self.L**2), 0, (12*self.E*self.I)/(self.L**3), -(6*self.E*self.I)/(self.L**2)],
                            [0, (6*self.E*self.I)/(self.L**2), (2*self.E*self.I)/(self.L), 0, -(6*self.E*self.I)/(self.L**2), (4*self.E*self.I)/(self.L)]])
        
        self.kg = np.dot(np.dot(transpose(self.R), self.kl), self.R)
    
    def setLocalMassMatrix(self):
        c = self.D*self.A*self.L/420
        
        self.ml = np.array([[140*c, 0, 0, 70*c, 0, 0],
                            [0, 156*c, 22*self.L*c, 0, 54*c, -13*self.L*c],
                            [0, 22*self.L*c, 4*self.L*self.L*c, 0, 13*self.L*c, -3*self.L*self.L*c],
                            [70*c, 0, 0, 140*c, 0, 0],
                            [0, 54*c, 13*self.L*c, 0, 156*c, -22*self.L*c],
                            [0, -13*self.L*c,  -3*self.L*self.L*c, 0, -22*self.L*c,  4*self.L*self.L*c]])
        
        self.mg = np.dot(np.dot(transpose(self.R), self.ml), self.R)
        
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