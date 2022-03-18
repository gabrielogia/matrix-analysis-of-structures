import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_und = pd.read_csv('bin\data\saida1.csv', header=None)
df_d = pd.read_csv('bin\data\saida2.csv', header=None)

df = abs((df_und - df_d)).max(numeric_only=True).values

# aux = []
# for i in range(0, len(df)):
#     if (i%2==0):
#         aux.append(df[i])
        
# print(df)

plt.plot(df, '.-')
plt.grid(1)
plt.show()