import pandas as pd
import numpy as np
data = pd.read_csv('./concrete.csv', header=0)

#Normalización de los datos
#   -siguiendo la fórmula: ( Dato actual - dato mínimo ) / ( Dato máximo mínimo )
#   -para evitar que las neuronas se sobrecargen con un peso de mayor rango

dataf=((data-data.min())/(data.max()-data.min()))

#Separamos y aleatorizamos los datos en tres sets:
#   - Entrenamiento (0-70%), validación (70-85%) y validación (85-100%)
datos_entrenamiento, datos_validacion, datos_test = np.split(dataf.sample(frac=1), [int(.7*len(dataf)), int(.85*len(dataf))])

print(datos_entrenamiento)
print(datos_validacion)
print(datos_test)