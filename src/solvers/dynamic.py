import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os.path
import sys
import ast

from scipy.linalg import eigh, eig
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
        self.F = []
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
        F = P

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
        
    def setString(self):
        s = "{"
        for i in range(0, 10): #10 frequencias naturais
            s += "'natural_frequency_" + str(i+1) + "':'" + str(self.w[i]) + '\','
        for i in range(0, len(self.F)):
            aux = self.F[:, i]
            
            if (i == len(self.F) - 1):
                s += "'dof_" + str(i+1) + "':'" + str(max(abs(aux))) + '\''
            else:
                s += "'dof_" + str(i+1) + "':'" + str(max(abs(aux))) + '\','
        s += "}"
        
        return s
        
    def calculateFlexibilityMatrix(self):
        #self.F = np.dot(np.dot(self.phi, np.linalg.inv(np.diag(self.w))), transpose(self.phi))
        
        self.F = np.zeros((len(self.w), len(self.w)))
        for i in range(10): #10 frequencias naturais
            self.F += (1/self.w[i])*np.outer(self.phi[:,i], transpose(self.phi[:,i])) 

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
            self.omegas.append(math.sqrt(self.w[i])/(2*math.pi))
                  
    def solveEigenvalueProblem(self):
        self.w, self.v = eigh(self.data.K, self.data.M)
        
    def solve(self, k, damage):
        self.solveEigenvalueProblem()
        self.setNaturalFrequencies()
        self.setModalVectors()    
        self.setNormalizedModalMatrix()
        
        # K_phi = np.dot(self.data.K, self.phi)
        # M_phi = np.dot(np.dot(self.data.M, self.phi), np.diag(self.w))
        # I = np.dot(np.dot(transpose(self.phi), self.data.M), self.phi)
        #F = np.dot(np.dot(self.phi, np.linalg.inv(np.diag(self.w))), transpose(self.phi))
        # K = np.dot(np.dot(np.dot(np.dot(self.data.M, self.phi), np.diag(self.w)), transpose(self.phi)), self.data.M)
        
        # F2 = np.zeros((len(self.w), len(self.w)))
        # for i in range(len(self.w)):
        #     F2 += (1/self.w[i])*np.outer(self.phi[:,i], transpose(self.phi[:,i]))  
            
        # sumMatrix = np.zeros((len(self.w), len(self.w)))
        # for i in range(len(self.w)):
        #     sumMatrix += (self.w[i])*np.outer(self.phi[:,i], transpose(self.phi[:,i]))
        # K2 = np.dot(np.dot(self.data.M, sumMatrix), self.data.M)
        
        self.calculateFlexibilityMatrix()
        
        s = self.setString()
        df = ast.literal_eval(s)
        
        if (k == 0):
            df = pd.DataFrame(df, index=[0])
            df.to_csv('bin\data\intact_strucutre.csv', index=False)
        
        else:
            df_damaged = pd.DataFrame(df, index=[0]).apply(pd.to_numeric, errors='coerce')
            df_intact = pd.read_csv('bin\data\intact_strucutre.csv')
            df_result = df_intact - df_damaged
            df_result['elem_damaged'] = self.data.elem[k-1].id
            df_result['damage'] = 1 - damage

            file_path = 'bin\data\\results_' + str(damage) + '.csv'
            if (os.path.exists(file_path) and k > 1):
                df = pd.read_csv('bin\data\\results_' + str(damage) + '.csv')
                df = df.append(df_result)
                df.to_csv('bin\data\\results_' + str(damage) + '.csv', index=False)
            else:
                df_result.to_csv('bin\data\\results_' + str(damage) + '.csv', index=False)
            
        # file_path = 'bin\data\saida2.csv'
        # a = ""
        # sys.stdout = open(file_path, "w")
        # for i in range(len(self.F)):
        #     for j in range(len(self.F[i])):
        #             if (j == len(self.F[i]) - 1):
        #                 a += str(self.F[i][j]) + '\n'
        #             else:
        #                 a += str(self.F[i][j]) + ','
        # print(a)       

        # self.setInitialConditions()
        # self.setDampingMatrix()
        # self.dynamicAnalysis()
        # self.plotResponse()