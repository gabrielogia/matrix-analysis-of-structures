import sys
from pathlib import Path

class Output():
    def __init__(self) -> None:
        pass
    
    def printEnd(self):
        print("\n")
        print('#'*43)
        print("#", end="")
        print(" "*13, end="")
        print("End of Analysis", end="")
        print(" "*13, end="")
        print("#")
        print('#'*43, end="\n\n")
    
    def printInit(self):
        print('#'*43)
        print("#", end="")
        print(" "*11, end="")
        print("Results of Analysis", end="")
        print(" "*11, end="")
        print("#")
        print('#'*43, end="\n\n")
        
    def printSupportReactions(self, data):
        print("")
        print(" "*10, end="")
        print("- Support Reactions -", end="")
        print(" "*9, end="\n\n")
        
        print(" Node No.", end="")
        print(" "*8, end="")
        print("X Force", end="")
        print(" "*8, end="")
        print("Y Force")
        
        print(" --------", end="")
        print(" "*7, end="")
        print("---------", end="")
        print(" "*6, end="")
        print("---------")
        
        for i in range(1, len(data.globalCoordinates), 2):
            if (data.globalCoordinates[i] > data.degreesFree):
                for j in range(0, len(data.elem)):
                    found = False
                    for k in range(1, len(data.elem[j].e), 2):
                        if (data.elem[j].e[k-1] == data.globalCoordinates[i-1] and data.elem[j].e[k] == data.globalCoordinates[i]):
                            print("    %i    " %(int(i/2 + 1)), end="")
                            print(" "*8, end="")
                            if (data.elem[j].e[k-1] - data.degreesFree - 1 < 0):
                                print("0.0000", end="")
                                print(" "*9, end="") 
                                print("%.5f" %(data.R[data.elem[j].e[k] - data.degreesFree - 1]))
                            elif (data.elem[j].e[k] - data.degreesFree - 1 < 0):
                                print("%.5f" %(data.R[data.elem[j].e[k-1] - data.degreesFree - 1])) 
                                print(" "*9, end="")
                                print("0.0000")
                            else:
                                print("%.3f" %(data.R[data.elem[j].e[k-1] - data.degreesFree - 1]), end="") 
                                print(" "*9, end="") 
                                print("%.3f" %(data.R[data.elem[j].e[k] - data.degreesFree - 1])) 
                            found = True
                            break
                    
                    if (found):
                        break
                    
    def printelemForces(self, data):
        print("")
        print(" "*10, end="")
        print("- Member Axial Forces -", end="")
        print(" "*9, end="\n\n")
        
        print(" "*10, end="")
        print("Member", end="")
        print(" "*6, end="")
        print("Axial Force")
        
        print(" "*10, end="")
        print("------", end="")
        print(" "*6, end="")
        print("-----------")
        
        for i in range(0, len(data.elem)):
            if(i < 9):
                print(" "*12, end="")
            else:
                print(" "*11, end="")
            print("%i" %data.elem[i].id, end="")
            print(" "*10, end="")
            if (data.elem[i].q[0] < 0):
                print("%.3f (T)" %(abs(data.elem[i].q[0])))
            else:
                print("%.3f (C)" %(abs(data.elem[i].q[0])))
    
    def printDisplacements(self, data):
        print(" "*10, end="")
        print("- Nodes Displacements -", end="")
        print(" "*10, end="\n\n")
        
        print(" Node No.", end="")
        print(" "*4, end="")
        print("X Translation", end="")
        print(" "*4, end="")
        print("Y Translation")
        
        print(" --------", end="")
        print(" "*4, end="")
        print("-------------", end="")
        print(" "*4, end="")
        print("-------------")
        
        for i in range(1, len(data.globalCoordinates), 2):
            for j in range(0, len(data.elem)):
                found = False
                for k in range(1, len(data.elem[j].e), 2):
                    if (data.elem[j].e[k-1] == data.globalCoordinates[i-1] and data.elem[j].e[k] == data.globalCoordinates[i]):
                        print("    %i    " %(int(i/2 + 1)), end="")
                        print(" "*7, end="")
                        print("%.6f" %(data.elem[j].v[k-1]), end="")
                        print(" "*8, end="")
                        print("%.6f" %(data.elem[j].v[k]))
                        found = True
                        break
                
                if (found):
                    break

    def printResults(self, data):
        Path("output/").mkdir(parents=True, exist_ok=True)
        
        file_path = 'output/results_' + data.filename
        sys.stdout = open(file_path, "w")
        
        self.printInit()
        self.printDisplacements(data)
        self.printelemForces(data)
        self.printSupportReactions(data)
        self.printEnd()