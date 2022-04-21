from numpy import float32
import pandas as pd

from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder

df = pd.read_csv('bin\src\ml\\results_complete.csv')

scaler = StandardScaler()
hot_encoder = OneHotEncoder(sparse=False)

X_train, X_test, y_train, y_test = train_test_split(df.drop(['elem_damaged', 'damage'], axis=1), df['elem_damaged'], test_size=0.20, random_state=41)

X_train = scaler.fit_transform(X_train)

y_train = hot_encoder.fit_transform(y_train.values.reshape(-1, 1))

model = keras.Sequential()
model.add(keras.Input(shape=(126)))
model.add(keras.layers.Dense(250, activation='relu'))
model.add(keras.layers.Dense(250, activation='relu'))
model.add(keras.layers.Dense(250, activation='relu'))
model.add(keras.layers.Dense(129, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=2000)