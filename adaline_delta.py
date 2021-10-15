# Importar bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Adaline():
    # Constructor
    def __init__(self, d, xi, n_muestras, wi, fac_ap,epochs, w_ajustado, Max_ciclo, Max_num_err):
        self.d = d
        self.xi = xi
        self.n_muestras = n_muestras
        self.wi = wi
        self.fac_ap = fac_ap
        self.epochs = epochs
        self.y = 0 # Salida de la red
        self.w_ajustado = w_ajustado
        self.Max_ciclo = Max_ciclo
        self.Max_num_err = Max_num_err

    def Entrenamiento(self):
        Err_act = 1 # Error de salida
        Err_cuad_act = 0 # Error cuadrático actual
        Err_ant = 0 # Error Anterior
        Err_cuad_ant = 0 # Error cuadrático anterior
        Err_cuad_med = 0 # Error cuadrático medio

        E_red = [] # Error de la red
        E_total = 0 # Error total (se va sumando)
        
        Err_count = 0 # Veces que se repite el mismo error

        while(self.epochs < Max_ciclo and Err_count < Max_num_err):
            if (Err_ant == Err_act):
                Err_count = Err_count + 1
            else:
                Err_count = 0
            Err_ant = Err_act #Copia el valor anterior del Error de Salida


            Err_cuad_ant = Err_cuad_med
            for i in range(self.n_muestras):
                self.y = sum(self.xi[i,:] * self.wi) # Cálculo de la salida de la red
                Err_cuad_act = (self.d[i] - self.y) # Cálculo del error
                self.wi = self.wi + (self.fac_ap * Err_cuad_act * self.xi[i,:])
                E_total =  E_total + ((Err_cuad_act)**2)

            # Calcular el error cuadrático medio
            Err_cuad_med = ((1/self.n_muestras) * (E_total))
            Err_act = (Err_cuad_med - Err_cuad_ant) # Error de la red
            E_red.append(np.abs(Err_act))
            self.epochs += 1
            #print(E_red)
        return self.wi, self.epochs, E_red

    def F_operacion(self):
        salida = []
        for j in range(self.n_muestras):
            self.y = sum(self.xi[j,:] * self.w_ajustado)
            salida.append(self.y)
        return salida


# Ciclo principal
if __name__ == "__main__":
    datos_entrenamiento = pd.read_csv('./datos_entrenamiento2.csv', header=0, delimiter=';') # Obtener los datos del fichero
    datos_entrenamiento = np.array(datos_entrenamiento) # Convertir los datos de la tabla de una matriz
    
    xi = datos_entrenamiento[:,0:8] # Datos de entrada xi (todas las filas, columnas 0 hasta no inclusivo 8)
    d = datos_entrenamiento[:,-1] # Valores deseados (todas las filas, ultima columna)
    n_muestras = len(d) # Número de muestras

    np.random.seed(69420)
    wi = np.random.rand(8) # Inicializamos aleatoriamente los pesos con una semilla
    
    fac_ap = 0.3 # Factor de aprendizaje

    
    epochs = 0 # Número de ciclos
    Max_ciclo = 100 # Total de ciclos
    Max_num_err = 6 # Número máximo de veces que se repite un error
    w_ajustado = [] # Array de pesos de Adaline
    
    red = Adaline(d, xi, n_muestras, wi, fac_ap,epochs, w_ajustado, Max_ciclo, Max_num_err) # Inicializar la red Adaline
    w_ajustado, epochs, error = red.Entrenamiento()
    
    
    # Dibujamos la Gráfica y sacamos los pesos por pantalla
    plt.ylabel('Error', Fontsize = 12)
    plt.xlabel('Épocas', Fontsize = 12)
    plt.title ("Adaline, Regla Delta")
    x = np.arange(epochs)
    plt.plot(x, error, 'm->', label = "Error cuadrático")
    plt.legend(loc='upper right')
    plt.show()
    print("Pesos ajustados",w_ajustado)