from types import prepare_class


class WriteFrame():
    def __init__(self, data) -> None:
        self.printInit()
        self.printDisplacements(data)
        self.printForcesInLocalCoord(data)   
        self.printSupportReactions(data)
        
    def printInit(self):
        print('#'*69)
        print("#", end="")
        print(" "*24, end="")
        print("Results of Analysis", end="")
        print(" "*24, end="")
        print("#")
        print('#'*69, end="\n\n")
        
    def printDisplacements(self, data):
        print(" "*22, end="")
        print("- Nodes Displacements -", end="")
        print(" "*24, end="\n\n")
        
        print("Node No.", end="")
        print(" "*4, end="")
        print("X Translation [m]", end="")
        print(" "*4, end="")
        print("Y Translation [m]", end="")
        print(" "*4, end="")
        print("Rotation [rad]")
        
        print("--------", end="")
        print(" "*4, end="")
        print("-----------------", end="")
        print(" "*4, end="")
        print("-----------------", end="")
        print(" "*4, end="")
        print("--------------")
        
        for i in range(0, len(data.nodes)):
            for j in range(0, len(data.elem)):
                if (data.nodes[i].id == data.elem[j].Ni):
                    print("    %i    " %(data.nodes[i].id), end="")
                    
                    if (data.elem[j].v[0] < 0):
                        print(" "*7, end="")
                    else:
                        print(" "*8, end="")
                    print("%.6f" %(data.elem[j].v[0]), end="")
                    
                    if (data.elem[j].v[1] < 0):
                        print(" "*11, end="")
                    else:
                        print(" "*12, end="")
                    print("%.6f" %(data.elem[j].v[1]), end="")
                    
                    if (data.elem[j].v[2] < 0):
                        print(" "*11, end="")
                    else:
                        print(" "*12, end="")
                    print("%.6f" %(data.elem[j].v[2]))
                    break
                
                elif (data.nodes[i].id == data.elem[j].Nf):
                    print("    %i    " %(data.nodes[i].id), end="")
                    
                    if (data.elem[j].v[3] < 0):
                        print(" "*7, end="")
                    else:
                        print(" "*8, end="")
                    print("%.6f" %(data.elem[j].v[3]), end="")
                    
                    if (data.elem[j].v[4] < 0):
                        print(" "*11, end="")
                    else:
                        print(" "*12, end="")
                    print("%.6f" %(data.elem[j].v[4]), end="")
                    
                    if (data.elem[j].v[5] < 0):
                        print(" "*11, end="")
                    else:
                        print(" "*12, end="")
                    print("%.6f" %(data.elem[j].v[5]))
                    break

    def printForcesInLocalCoord(self, data):
        print("")
        print(" "*12, end="")
        print("- Member End Forces in Local Coordinates -", end="")
        print(" "*12, end="\n\n")
        
        print("Bar", end="")
        print(" "*4, end="")
        print("Node", end="")
        print(" "*4, end="")
        print("Axial Force [kN]", end="")
        print(" "*4, end="")
        print("Shear Force [kN]", end="")
        print(" "*4, end="")
        print("Moment [kN*m]")
        
        print("---", end="")
        print(" "*4, end="")
        print("----", end="")
        print(" "*4, end="")
        print("-"*16, end="")
        print(" "*4, end="")
        print("-"*16, end="")
        print(" "*4, end="")
        print("-"*13)
        
        for i in range(0, len(data.elem)):
            print(" %i " %(data.elem[i].id), end="")
            
            print(" "*6, end="")
            print("%i" %(data.elem[i].Ni), end="")
            
            # if (data.elem[i].sin == 1):
            #     self.writeForcesChanged(data.elem[i])
            # else:
            self.writeForces(data.elem[i])
                
    def writeForcesChanged(self, elem):
        aux = elem.f[0]
        elem.f[0] = elem.f[1]
        elem.f[1] = aux
        
        aux = elem.f[3]
        elem.f[3] = elem.f[4]
        elem.f[4] = aux
        
        self.writeForces(elem)
    
    def writeForces(self, elem):
        if (elem.q[0] < 0):
            print(" "*10, end="")
        else:
            print(" "*9, end="")
        print("%.3f" %(-elem.q[0]), end="")
        
        if (elem.q[1] < 0):
            print(" "*13, end="")
        else:
            print(" "*12, end="")
        print("%.3f" %(elem.q[1]), end="")
        
        if (elem.q[2] < 0):
            print(" "*13, end="")
        else:
            print(" "*12, end="")
        print("%.3f" %(elem.q[2]))
        
        print(" "*9, end="")
        print("%i" %(elem.Nf), end="")
        
        if (elem.q[3] < 0):
            print(" "*9, end="")
        else:
            print(" "*10, end="")
        print("%.3f" %(elem.q[3]), end="")
        
        if (elem.q[4] < 0):
            print(" "*12, end="")
        else:
            print(" "*13, end="")
        print("%.3f" %(-elem.q[4]), end="")
        
        if (elem.q[5] < 0):
            print(" "*12, end="")
        else:
            print(" "*13, end="")
        print("%.3f" %(elem.q[5]))        

    def printSupportReactions(self, data):
        print()
        print(" "*23, end="")
        print("- Support Reactions -", end="")
        print(" "*24, end="\n\n")
        
        print("Node No.", end="")
        print(" "*8, end="")
        print("X Force [kN]", end="")
        print(" "*8, end="")
        print("Y Force [kN]", end="")
        print(" "*8, end="")
        print("Moment [kN*m]")
        
        print("--------", end="")
        print(" "*8, end="")
        print("------------", end="")
        print(" "*8, end="")
        print("------------", end="")
        print(" "*8, end="")
        print("-------------")
        
        i = 0
        while (i < (len(data.R)-1)):
            for j in range(0, len(data.nodes)):
                if (data.nodes[j].supX == 1 or data.nodes[j].supY == 1 or data.nodes[j].supZ == 1):
                    print("   %i   " %(data.nodes[j].id), end="")
                    
                    if (data.nodes[j].supX == 1):
                        print("          %.3f        " %(data.R[i]), end="")
                        i = i + 1
                    else:
                        print("          0.000       ", end="")
                        
                    if (data.nodes[j].supY == 1):
                        print("      %.3f        " %(data.R[i]), end="")
                        i = i + 1
                    else:
                        print("      0.000        ", end="")
                        
                    if (data.nodes[j].supZ == 1):
                        print("      %.3f        " %(data.R[i]))
                        i = i + 1
                    else:
                        print("      0.000        ")