import pandas as pd
import numpy as np

damages = np.linspace(0.01, 0.99, 100)

df = pd.DataFrame()
for i in range(len(damages)):
    aux = pd.read_csv('bin\data\\results_' + str(damages[i]) + '.csv')
    df = df.append(aux).reset_index(drop=True)
    
df.to_csv('bin\src\ml\\results_complete.csv', index=False)