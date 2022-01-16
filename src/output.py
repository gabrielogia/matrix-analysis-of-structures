import sys
from pathlib import Path
from src.write.truss import WriteTruss
from src.write.frame import WriteFrame

class Output():
    def __init__(self) -> None:
        self.model = ''
    
    def printResults(self, data):
        Path("bin/output/").mkdir(parents=True, exist_ok=True)
        
        file_path = 'bin/output/results_' + data.filename
        sys.stdout = open(file_path, "w")
        
        if (data.model == 'frame'):
            self.model = WriteFrame(data)
        else:
            self.model = WriteTruss(data)