import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 18})

x = np.linspace(0.01, 0.99, 100)
print(x)
d1 = []
d2 = []
d3 = []
d4 = []

for i in range(len(x)):
    d1.append(x[i])
    d2.append((10**x[i] - 1)/9)
    d3.append(1/(1 + ((3*x[i])/(x[i] - 1))**-2))
    d4.append(1/(1 + ((x[i])/(x[i] - 1))**-2))
    
plt.plot(x, d1)
plt.plot(x, d2)
plt.plot(x, d3)
plt.plot(x, d4)
plt.legend([r'$D_1(x)$', r'$D_2(x)$', r'$D_3(x)$', r'$D_4(x)$'])
plt.xlabel(r'$X$')
plt.ylabel(r'$Damage$')
plt.grid(1)
plt.show()