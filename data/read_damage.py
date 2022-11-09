import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 36})
plt.rcParams.update({"font.family": "Palatino Linotype"})

k = 10

damages = np.linspace(0.01, 0.99, 200)
a = []
b = []
c = []

for i in damages:
    a.append((k**i - 1)/(k - 1))
    b.append(1/(1 + (i/(i - 1))**-2))
    c.append(i)

plt.plot(a, 'b.-', lw=2)
plt.plot(b, 'r.-', lw=2)
plt.plot(c, 'k.-', lw=2)
plt.grid(1)
plt.legend(["$D_1(x)$", "$D_2(x)$", "$D_3(x)$"])
plt.show()