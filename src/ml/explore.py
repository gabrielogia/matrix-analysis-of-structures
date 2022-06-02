import pandas as pd 

df = pd.read_csv('bin\src\ml\\results_complete.csv')

print(df[df['natural_frequency_1'] == 0]['elem_damaged'].unique())