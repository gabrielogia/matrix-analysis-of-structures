import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('bin\data\\test.csv')
print(df)

plt.plot(df['x'], df['y'], '.')
plt.show()