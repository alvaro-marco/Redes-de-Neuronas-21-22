# Importar bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Adaline():
    # Constructor
    def __init__(self, d, xi, n_muestras, wi, fac_ap,epochs, precision, w_ajustado):
        self.d = d
        self.xi = xi
        self.n_muestras = n_muestras
        self.wi = wi
        self.fac_ap = fac_ap
        self.epochs = epochs
        self.precision = precision
        self.y = 0 # Salida de la red
        self.w_ajustado = w_ajustado

    def Entrenamiento(self):
        E = 1 # Error de salida
        E_ac = 0 # Error actual
        E_prev = 0 # Error anterior
        Ew = 0 # Error cuadrático medio
        E_red = [] # Error de la red
        E_total = 0 # Error total

        while (np.abs(E) > self.precision):
            E_prev = Ew
            for i in range(self.n_muestras):
                self.y = sum(self.xi[i,:] * self.wi) # Cálculo de la salida de la red
                E_ac = (self.d[i] - self.y) # Cálculo del error
                self.wi = self.wi + (self.fac_ap * E_ac * self.xi[i,:])
                E_total =  E_total + ((E_ac)**2)

            # Calcular el error cuadrático medio
            Ew = ((1/self.n_muestras) * (E_total))
            E = (Ew - E_prev) # Error de la red
            E_red.append(np.abs(E))
            self.epochs += 1
        return self.wi, self.epochs, E_red

    def F_operacion(self):
        salida = []
        for j in range(self.n_muestras):
            self.y = sum(self.xi[j,:] * self.w_ajustado)
            salida.append(self.y)
        return salida


# Ciclo principal
if __name__ == "__main__":
    # leer los datos
    datos_entrenamiento = pd.read_csv('./datos_entrenamiento2.csv', header=0)
    # Convertir los datos de la tabla de una matriz
    datos_entrenamiento = np.array(datos_entrenamiento)
    # Datos de entrada xi
    xi = datos_entrenamiento[:,0:7]
    # Valores deseados
    d = datos_entrenamiento[:,8]
    # Número de muestras
    n_muestras = len(d)
    # Establecer el vector de pesos w
    wi = np.array([3.12, 2.00, 1.86, 1, 1, 1, 1])
    # Factor de aprendizaje
    fac_ap = 0.3
    # Épocas
    epochs = 0
    precision = 0.001
    w_ajustado = []
    # Inicializar la red Adaline
    red = Adaline(d, xi, n_muestras, wi, fac_ap,epochs, precision, w_ajustado)
    w_ajustado, epochs, error = red.Entrenamiento()
    # Gráfica
    plt.ylabel('Error', Fontsize = 12)
    plt.xlabel('Épocas', Fontsize = 12)
    plt.title ("Adaline, Regla Delta")
    x = np.arange(epochs)
    plt.plot(x, error, 'm->', label = "Error cuadrático")
    plt.legend(loc='upper right')
    plt.show()
    print("Pesos ajustados",w_ajustado)