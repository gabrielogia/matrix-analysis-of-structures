import time

from src.engine import Engine

filename = 'dynamic/validated/tower.txt'
simulation = Engine()
start = time.time()
simulation.start(filename)
end = time.time()
print(end - start)