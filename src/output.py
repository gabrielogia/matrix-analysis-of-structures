class Output():
    def __init__(self) -> None:
        pass

    def printResults(self, data):
        for i in range(len(data.nodes)):
            if (data.nodes[i].coordsGlobal[0] > data.degreesFree):
                print("Node: %i" %(data.nodes[i].id))
                print(data.R[data.nodes[i].coordsGlobal[0] - 1 - data.degreesFree])

            if (data.nodes[i].coordsGlobal[1] > data.degreesFree):
                print("Node: %i" %(data.nodes[i].id))
                print(data.R[data.nodes[i].coordsGlobal[1] - 1 - data.degreesFree])