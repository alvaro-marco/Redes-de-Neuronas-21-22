# Importar bibliotecas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Adaline():
    # Constructor
    def __init__(self, d, xi, n_muestras, d_val, xi_val, n_muestras_val, wi, fac_ap,epochs, umbral, w_ajustado, Max_ciclo, Max_num_err, Max_pos_val):
        self.d = d
        self.xi = xi
        self.n_muestras = n_muestras
        self.wi = wi
        self.fac_ap = fac_ap
        self.epochs = epochs
        self.umbral = umbral
        self.y = 0                          # Salida de la red entrenamiento
        self.w_ajustado = w_ajustado
        self.Max_ciclo = Max_ciclo
        self.Max_num_err = Max_num_err
        #Variables del conjunto de validación
        self.d_val = d_val
        self.xi_val = xi_val
        self.n_muestras_val = n_muestras_val
        self.y_val = 0                      # Salida de la red validación
        self.Max_pos_val = Max_pos_val

    def Entrenamiento(self):
        Err_act_ent = 1 # Error de salida
        Err_cuad_act_ent = 0 # Error cuadrático actual
        Err_ant_ent = 0 # Error Anterior
        Err_cuad_ant_ent = 0 # Error cuadrático anterior
        Err_cuad_med_ent = 0 # Error cuadrático medio

        E_red_ent = [] # Error de la red
        E_total_ent = 0 # Error total (se va sumando)
        
        Err_count_ent = 0 # Veces que se repite el mismo error
        
        Err_act_val = 1 # Error de salida
        Err_cuad_act_val = 0 # Error cuadrático actual
        Err_ant_val = 0 # Error Anterior
        Err_cuad_ant_val = 0 # Error cuadrático anterior
        Err_cuad_med_val = 0 # Error cuadrático medio

        E_red_val = [] # Error de la red
        E_total_val = 0 # Error total (se va sumando)
        
        Err_count_val = 0 # Veces que se repite el mismo error

        counter = 0
        max_counter = Max_pos_val

        while(counter < max_counter and self.epochs < Max_ciclo and Err_count_ent < Max_num_err):
            if (Err_ant_ent == Err_act_ent):
                Err_count_ent = Err_count_ent + 1
            else:
                Err_count_ent = 0
            Err_ant_ent = Err_act_ent # Copia el valor anterior del Error de Salida

            if (Err_ant_val == Err_act_val):
                Err_count_val = Err_count_val + 1
            else:
                Err_count_val = 0
            Err_ant_val = Err_act_val # Copia el valor anterior del Error de Salida


            Err_cuad_ant_ent = Err_cuad_med_ent
            Err_cuad_ant_val = Err_cuad_med_val

            for i in range(self.n_muestras):
                self.y = sum(self.xi[i,:] * self.wi) + umbral # Cálculo de la salida de la red
                Err_cuad_act_ent = (self.d[i] - self.y) # Cálculo del error
                self.wi = self.wi + (self.fac_ap * Err_cuad_act_ent * self.xi[i,:])
                self.umbral = self.umbral = (self.fac_ap * Err_cuad_act_ent)
                E_total_ent =  E_total_ent + ((Err_cuad_act_ent)**2)

            for j in range(self.n_muestras_val):
                self.y = sum(self.xi_val[j,:] * self.wi) + umbral # Cálculo de la salida de la red para el conjunto de validación
                Err_cuad_act_val = (self.d[j] - self.y) # Cálculo del error de validación
                E_total_val =  E_total_val + ((Err_cuad_act_val)**2)


            # Calcular el error cuadrático medio
            Err_cuad_med_ent = ((1/self.n_muestras) * (E_total_ent))
            Err_act_ent = (Err_cuad_med_ent - Err_cuad_ant_ent) # Error de la red
            E_red_ent.append(np.abs(Err_act_ent))
            Err_cuad_med_val = ((1/self.n_muestras_val) * (E_total_val))
            Err_act_val = (Err_cuad_med_val - Err_cuad_ant_val) # Error de la red
            E_red_val.append(np.abs(Err_act_val))
            print(self.epochs, Err_act_val, Err_ant_val, (Err_act_val-Err_ant_val))
            self.epochs += 1
            if (Err_act_val - Err_ant_val) > 0: #Comprueba que el error anterior no sea menor con un contador
                counter =counter +1
                
        return self.wi, self.epochs, E_red_ent, E_red_val

    def F_operacion(self):
        salida = []
        for j in range(self.n_muestras):
            self.y = sum(self.xi[j,:] * self.w_ajustado)
            salida.append(self.y)
        return salida


# Ciclo principal
if __name__ == "__main__":
    datos_entrenamiento = np.array(pd.read_csv('./datos_entrenamiento2.csv', header=0, delimiter=';')) # Obtener los datos de entrenamiento del fichero y pasarlos a una matriz
    datos_validacion = np.array(pd.read_csv('./datos_validacion2.csv', header=0, delimiter=';')) # Convertir los datos de validación de la tabla de una matriz
    
    xi_ent = datos_entrenamiento[:,0:8] # Datos de entrada xi (todas las filas, columnas 0 hasta no inclusivo 8)
    des_ent = datos_entrenamiento[:,-1] # Valores deseados (todas las filas, ultima columna)
    n_muestras_ent = len(des_ent) # Número de muestras

    xi_val = datos_validacion[:,0:8] # Datos de entrada xi (todas las filas, columnas 0 hasta no inclusivo 8)
    des_val = datos_validacion[:,-1] # Valores deseados (todas las filas, ultima columna)
    n_muestras_val = len(des_val) # Número de muestras
    #print(xi_val)

    np.random.seed(69420)
    wi = np.random.rand(8) # Inicializamos aleatoriamente los pesos con una semilla
    
    fac_ap = 0.0001 # Factor de aprendizaje

    umbral = 0.5
    
    ciclos = 0 # Número de ciclos
    Max_ciclo = 500 # Total de ciclos
    Max_num_err = 5 # Número máximo de veces que se repite un error
    w_ajustado = [] # Array de pesos de Adaline
    Max_pos_val = 20
    
    red = Adaline(des_ent, xi_ent, n_muestras_ent, des_val, xi_val, n_muestras_val, wi, fac_ap,ciclos, umbral, w_ajustado, Max_ciclo, Max_num_err, Max_pos_val) # Inicializar la red Adaline
    w_ajustado, ciclos, error_ent, error_val = red.Entrenamiento()
    
    
    # Dibujamos la Gráfica y sacamos los pesos por pantalla
    plt.ylabel('Error cuadrático medio', Fontsize = 12)
    plt.xlabel('Ciclos', Fontsize = 12)
    plt.title ("Adaline")
    x = np.arange(ciclos)
    plt.plot(x, error_ent, 'm->', label = "Error de entrenamiento", color = "green")
    plt.plot(x, error_val, 'm->', label = "Error de validación", color = "red")
    plt.legend(loc='upper right')
    plt.show()
    print("Pesos ajustados", w_ajustado)