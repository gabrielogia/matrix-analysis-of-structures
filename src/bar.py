import numpy as np
from numpy.core.fromnumeric import transpose

class Bar():
    def __init__(self, id, Ni, Nf, E, A, I, dirLoad, Qx, Qy) -> None:
        self.id = int(id)
        self.Ni = int(Ni)
        self.Nf = int(Nf)
        self.E = float(E)
        self.A = float(A)
        self.I = float(I)
        self.dirLoad = dirLoad
        self.Qx = float(Qx)
        self.Qy = float(Qy)
        self.L = 0.0
        self.cos = 0.0
        self.sin = 0.0
        self.kl = [] #matriz de rigidez da barra no sistema local
        self.kg = [] #matriz de rigidez da barra no sistema global
        self.e = [] #vetor de espaçamento
        self.R = [] #matriz de rotacao
        self.fl = [0]*6 #vetor de forças nas coordenadas locais
        self.fg = [0]*6 #vetor de forças nas coordenadas globais

    def setEVector(self, Ni, Nf):
        self.e = Ni.coordsGlobal + Nf.coordsGlobal

    def setLocalStiffnessMatrix(self):
        self.kl = np.array([[self.E*self.A/self.L, 0, 0, -self.E*self.A/self.L, 0, 0],
                            [0, 12*self.E*self.I/(self.L**3), 6*self.E*self.I/(self.L**2), 0, -12*self.E*self.I/(self.L**3), 6*self.E*self.I/(self.L**2)],
                            [0, 6*self.E*self.I/(self.L**2), 4*self.E*self.I/(self.L), 0, -6*self.E*self.I/(self.L**2), 2*self.E*self.I/(self.L)],
                            [-self.E*self.A/self.L, 0, 0, self.E*self.A/self.L, 0, 0],
                            [0, -12*self.E*self.I/(self.L**3), -6*self.E*self.I/(self.L**2), 0, 12*self.E*self.I/(self.L**3), -6*self.E*self.I/(self.L**2)],
                            [0, 6*self.E*self.I/(self.L**2), 2*self.E*self.I/(self.L), 0, -6*self.E*self.I/(self.L**2), 4*self.E*self.I/(self.L)]])
        
        self.kg = np.dot(np.dot(transpose(self.R), self.kl), self.R)
    
    def setRotationMatrix(self):
        self.R = np.array([[self.cos, self.sin, 0, 0, 0, 0], 
                            [-self.sin, self.cos, 0, 0, 0, 0], 
                            [0, 0, 1, 0, 0 ,0], 
                            [0, 0, 0, self.cos, self.sin, 0], 
                            [0, 0, 0, -self.sin, self.cos, 0], 
                            [0, 0, 0, 0, 0, 1]])

    def setLocalForces(self):
        if (self.dirLoad == 'Global'):
            self.fl = np.array([0, self.Qy*self.L/2, (self.Qy*self.L*self.L)/12, 0, self.Qy*self.L/2, -(self.Qy*self.L*self.L)/12])
            self.fg = np.dot(transpose(self.R), self.fl) #faltou utilizar a transposta de R
        else:
            print(self.fl)