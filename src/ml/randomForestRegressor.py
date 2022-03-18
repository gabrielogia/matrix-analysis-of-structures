import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('bin\src\ml\\results_complete.csv')

print(df)

scaler = StandardScaler()

X_train, X_test, y_train, y_test = train_test_split(df.drop(['elem_damaged', 'damage'], axis=1), df['damage'], test_size=0.20, random_state=41)

X_train = scaler.fit_transform(X_train)

log_reg = RandomForestRegressor(n_jobs=4)
log_reg.fit(X_train, y_train)
predictions = log_reg.predict(scaler.transform(X_test))

print(len(predictions))

plt.plot(y_test.values)
plt.plot(predictions)
#plt.plot(y_test.values - predictions)
plt.grid(1)
plt.show()