import pandas as pd
import numpy as np

damages = np.linspace(0.01, 0.99, 100)
a = 10
damage_type = 'linear_beam'

df = pd.DataFrame()
for i in range(len(damages)):
    damage = damages[i]
    #damage = (a**damages[i] - 1)/(a - 1)
    #damage = 1/(1 + ((3*damages[i])/(damages[i] - 1))**-2)
    file_path = 'bin\data\\results_' + str(damage) + '.csv'
    aux = pd.read_csv(file_path)
    df = df.append(aux).reset_index(drop=True)
    
df.to_csv('bin\src\ml\\results_complete_'+ damage_type + '.csv', index=False)