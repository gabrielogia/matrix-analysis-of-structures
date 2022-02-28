import numpy as np
import matplotlib.pyplot as plt
import math

from scipy.linalg import eigh
from scipy.integrate import solve_ivp
from numpy.core.fromnumeric import transpose

class DynamicSolver():
    def __init__(self, data) -> None:
        self.data = data
        self.w = [] #autovalores
        self.v = [] #autovetores
        self.omegas = [] #frequencias naturais (rad/s)
        self.a = [] #modal vectors
        self.phi = [] #modal matrix of vectors normalized
        self.P = [] #normalized force
        self.u0 = []
        self.v0 = []
        self.q0 = []
        self.dq0 = []
        self.C = [] #proportional damping matrix
        self.zetas = [] #damping ratio
        self.r = [] #response
        
    def plotResponse(self):
        yim = np.dot(self.phi, self.r)
        
        fig, axs = plt.subplots(len(self.data.M))
        for i in range(len(axs)):
            axs[i].plot(self.data.t, yim[i])
            axs[i].set(xlabel="time [s]", ylabel='displacement '+str(i))

        plt.show()

    def sod2(self, t, u, P, omega, zeta):
        #excitation function
        if (t <= 0.25):
            F = P
        elif (t < 0.5):
            F = 2*P*(1-2*t)
        else:
            F = 0

        return [u[1], -omega*omega*u[0] - 2*zeta*omega*u[1] + F]
    
    def dynamicAnalysis(self):
        aux = []
        for i in range(len(self.data.M)):
            aux.append(solve_ivp(self.sod2, [self.data.t[0], self.data.t[len(self.data.t) - 1]], [self.q0[i], self.dq0[i]], t_eval=self.data.t, args=(self.P[i], self.omegas[i], self.zetas[i])))
        
        self.r = np.zeros((len(self.data.M), len(aux[0]['y'][0])))
        for i in range(len(self.data.M)):
            for j in range(len(aux[0]['y'][0])):
                self.r[i][j] = aux[i]['y'][0][j]
        
    def setDampingMatrix(self):
        a = 0
        b = 0
        self.C = a*self.data.M + b*self.data.K
        nom_C = np.dot(np.dot(transpose(self.phi), self.C), self.phi)
        self.zetas = np.diag((1/2)*np.dot(nom_C, np.linalg.inv(np.diag(self.omegas))))

    def setInitialConditions(self):
        self.u0 = np.zeros(len(self.data.M))
        self.v0 = np.zeros(len(self.data.M))
        
        self.P = np.dot(transpose(self.phi), self.data.F)
        self.q0 = np.dot(np.dot(transpose(self.phi), self.data.M), self.u0)
        self.dq0 = np.dot(np.dot(transpose(self.phi), self.data.M), self.v0)
    
    def setNormalizedModalMatrix(self):
        self.phi = np.zeros((len(self.a), len(self.a)))
        
        for i in range(len(self.a)):
            norm = math.sqrt(np.dot(np.dot(transpose(self.a[i]), self.data.M), self.a[i]))
            for j in range(len(self.a[i])):
                self.phi[j][i] = self.a[i][j]/norm
        
    def setModalVectors(self):
        for i in range(len(self.v)):
            aux = []
            aux.append(1)
            for j in range(1, len(self.v[i])):
                aux.append(self.v[j][i]/self.v[0][i])
            self.a.append(aux)   
        
    def setNaturalFrequencies(self):
        for i in range(len(self.w)):
            self.omegas.append(math.sqrt(self.w[i]))

    def solveEigenvalueProblem(self):
        self.w, self.v = eigh(self.data.K, self.data.M)
        
    def solve(self):
        self.solveEigenvalueProblem()
        self.setNaturalFrequencies()
        self.setModalVectors()    
        self.setNormalizedModalMatrix()
        self.setInitialConditions()
        self.setDampingMatrix()
        self.dynamicAnalysis()
        self.plotResponse()