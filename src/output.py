class Output():
    def __init__(self) -> None:
        pass

    def printResults(self, data):
        for i in range(1, len(data.globalCoordinates), 2):
            for j in range(0, len(data.bars)):
                for k in range(1, len(data.bars[j].e), 2):
                    if (data.bars[j].e[k-1] == data.globalCoordinates[i-1] and data.bars[j].e[k] == data.globalCoordinates[i]):
                        print(int(i/2 + 1), data.globalCoordinates[i-1], data.globalCoordinates[i])
                        break