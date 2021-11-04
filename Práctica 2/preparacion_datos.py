import pandas as pd
import numpy as np
from sklearn import preprocessing

data = pd.read_csv('./vehicle.csv', header=None)
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

dataf = dataf.join(data_solo_tipo)

#dataf=((data-data.min())/(data.max()-data.min()))

#dataf = preprocessing.normalize(data, axis=0)
print(dataf)

#Separamos y aleatorizamos los datos en tres sets:
#   - Entrenamiento (0-70%), validación (70-85%) y validación (85-100%)
vehicleTrainValid, vehicleTest = np.split(dataf.sample(frac=1), [int((2/3)*len(dataf))])

print(vehicleTrainValid)
print(vehicleTest)

dataf.to_csv('dataf.csv', index=False)
vehicleTrainValid.to_csv('vehicleTrainValid.csv', index=False)
vehicleTest.to_csv('vehicleTest.csv', index=False)