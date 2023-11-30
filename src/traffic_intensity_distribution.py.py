import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
import pandas as pd
from functions.basics import *

def reescalar_lista_de_listas(lista_de_listas, maximo):

    lista_reescalada = []

    for lista in lista_de_listas:
        lista_reescalada.append([valor / maximo for valor in lista])

    return lista_reescalada

# Generar datos de una distribución normal

datos_obs = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")

hora_inicial, hora_final = 0, 24
for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):

        columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
        data_observacional = datos_obs[columnas_elejidas].values.tolist()
        
        ## Reescalando los data_observacional de 0 a 1
        data_observacional = reescalar_lista_de_listas(data_observacional, 255)

        data = [np.mean(data) for data in data_observacional]

        # Visualizar el histograma de la distribución
        plt.hist(data, bins=30, density=True, alpha=0.5, color='blue')
        plt.title('Distribución Normal')
        plt.xlabel('Valores')
        plt.ylabel('Frecuencia')
        plt.show()

        # Calcular algunos estadísticos
        percentiles = np.percentile(data, [25, 50, 75, 90, 95])
        skewness = skew(data)
        kurt = kurtosis(data)

        print("Percentiles (25th, 50th, 75th, 90th, 95th):", percentiles)
        print("Coeficiente de asimetría:", skewness)
        print("Curtosis:", kurt)