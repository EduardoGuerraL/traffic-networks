"""
Necesitamos saber cuantos datos hay por instante de tiempo, es decir, cuantas imagenes se sacaron del mismo instante de tiempo.
"""
from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales
from functions.basics import CrearCarpeta, reescalar_lista_de_listas, obtener_nombres_con_H_M_sinFDS, crearNintervalosOrdenados
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

datos_obs = pd.read_csv(Datos_observacionales[0])
hora_inicial, hora_final = 0, 24

N_de_datos = []
for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):

        columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
        N_de_datos.append(len(columnas_elejidas))

def plot_time_vs_data(data_count):
    # Crear lista de instantes de tiempo cada 15 minutos
    time_intervals = [f"{hour:02d}:{minute:02d}" for hour in range(0, 24) for minute in range(0, 60, 15)]

    # Graficar
    plt.figure(figsize=(8, 4))  # Tamaño del gráfico ajustado para un espacio limitado
    plt.plot(data_count, marker='o', linestyle='-')  # Graficar los datos
    plt.title('Instante de Tiempo vs. Número de Datos', fontsize=14)
    plt.xlabel('Instante de Tiempo', fontsize=12)
    plt.ylabel('Número de Datos', fontsize=12)
    
    # Mostrar solo algunos valores en el eje x
    x_indices = list(range(0, len(time_intervals), len(time_intervals) // 5))  # Mostrar un valor por cada 5 intervalos
    plt.xticks(x_indices, [time_intervals[i] for i in x_indices], rotation=45, ha='right', fontsize=10)
    
    plt.yticks(fontsize=10)  # Reducir el tamaño de las etiquetas del eje y
    plt.grid(True)
    plt.tight_layout()
    plt.show()

print(np.mean(N_de_datos))
plot_time_vs_data(N_de_datos)