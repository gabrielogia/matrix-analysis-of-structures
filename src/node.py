class Node():
    def __init__(self, id, x, y, supX, supY, supZ, kX, kY, kZ, Fx, Fy, Fz, model) -> None:
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

        if (model == 'truss'):
            self.coordsGlobal = 2*[0]
        else:
            self.coordsGlobal = 3*[0]

    def countDegrees(self):
        f = 0
        r = 0

        if (self.supX == 0):
            f += 1
        else:
            r += 1

        if (self.supY == 0):
            f += 1
        else:
            r += 1

        if (self.supZ == 0):
            f += 1
        elif (self.supZ == 1):
            r += 1

        return f, r

    def setFreeGlobalCoordinates(self, k):
        if (self.supX == 0):
            self.coordsGlobal[0] = k
            k += 1

        if (self.supY == 0):
            self.coordsGlobal[1] = k
            k += 1

        if (self.supZ == 0):
            self.coordsGlobal[2] = k
            k += 1

        return k

    def setRestrainedGlobalCoordinates(self, k):
        if (self.supX == 1):
            self.coordsGlobal[0] = k
            k += 1

        if (self.supY == 1):
            self.coordsGlobal[1] = k
            k += 1

        if (self.supZ == 1):
            self.coordsGlobal[2] = k
            k += 1

        return k