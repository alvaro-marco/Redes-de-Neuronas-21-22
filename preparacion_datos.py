import pandas as pd
import numpy as np
from sklearn import preprocessing

data = pd.read_csv('./concrete.csv', header=0)
print(data)

#Normalización de los datos
#   -siguiendo la fórmula: ( Dato actual - dato mínimo ) / ( Dato máximo mínimo )
#   -para evitar que las neuronas se sobrecarguen con un peso de mayor rango

scaler = preprocessing.MinMaxScaler()
names = data.columns
d = scaler.fit_transform(data)
dataf = pd.DataFrame(d, columns=names)
dataf.head()

#dataf=((data-data.min())/(data.max()-data.min()))

#dataf = preprocessing.normalize(data, axis=0)
print(dataf)

#Separamos y aleatorizamos los datos en tres sets:
#   - Entrenamiento (0-70%), validación (70-85%) y validación (85-100%)
datos_entrenamiento, datos_validacion, datos_test = np.split(dataf.sample(frac=1), [int(.7*len(dataf)), int(.85*len(dataf))])

print(datos_entrenamiento)
print(datos_validacion)
print(datos_test)

datos_entrenamiento.to_csv('datos_entrenamiento2.csv', index=False)
datos_validacion.to_csv('datos_validacion2.csv', index=False)
datos_test.to_csv('datos_test2.csv', index=False)