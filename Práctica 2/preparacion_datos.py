import pandas as pd
import numpy as np
from sklearn import preprocessing

data = pd.read_csv('./vehicle.csv', header=None)

# Se separan los datos en varios conjuntos para no utilizar la columna de los tipos de coche
data_sin_tipo = data.iloc[:, 0:18]
data_solo_tipo = data.iloc[:, 18]
names = data_sin_tipo.columns
print(data_sin_tipo)
print(data_solo_tipo)

#Normalización de los datos
#   -siguiendo la fórmula: ( Dato actual - dato mínimo ) / ( Dato máximo mínimo )
#   -para evitar que las neuronas se sobrecarguen con un peso de mayor rango

scaler = preprocessing.MinMaxScaler()
d = scaler.fit_transform(data_sin_tipo)
dataf = pd.DataFrame(d, columns=names)
dataf.head()

# Se vuelve a juntar la columna del tipo de coche
dataf = dataf.join(data_solo_tipo)
print(dataf)

#Separamos y aleatorizamos los datos en dos sets:
#   - Entrenamiento (2/3) y test (1/3)
vehicleTrainValid, vehicleTest = np.split(dataf.sample(frac=1), [int((2/3)*len(dataf))])

print(vehicleTrainValid)
print(vehicleTest)

dataf.to_csv('dataf.csv', index=False)
vehicleTrainValid.to_csv('vehicleTrainValid.csv', index=False)
vehicleTest.to_csv('vehicleTest.csv', index=False)