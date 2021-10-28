class Node():
    def __init__(self, id, x, y, supX, supY, supZ, kX, kY, kZ, Fx, Fy, Fz) -> None:
        self.id = int(id)  
        self.x = float(x)  
        self.y = float(y)   
        self.supX = int(supX)   
        self.supY = int(supY)   
        self.supZ = int(supZ)     
        self.kX = float(kX)   
        self.kY = float(kY)   
        self.kY = float(kZ)  
        self.Fx = float(Fx)  
        self.Fy = float(Fy)  
        self.Fz = float(Fz)
        self.coordsGlobal = [self.id*3 - 2, self.id*3 - 1, self.id*3]