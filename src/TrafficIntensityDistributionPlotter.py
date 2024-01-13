"""
Muestra la distribucion de datos (intensidad de trafico promedio de cada calle)

"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis
import pandas as pd
from functions.basics import reescalar_lista_de_listas, obtener_nombres_con_H_M_sinFDS, plot_distribution
from functions.RutasDeArchivos import Datos_observacionales

# Generar datos de una distribución normal

datos_obs = pd.read_csv(Datos_observacionales[0])

hora_inicial, hora_final = 0, 24
for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):

        columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
        data_observacional = datos_obs[columnas_elejidas].values.tolist()
        
        ## Reescalando los data_observacional de 0 a 1
        data_observacional = reescalar_lista_de_listas(data_observacional, 255)

        data = [np.mean(data) for data in data_observacional]

        plot_distribution(data, name = "TI")

        # Calcular algunos estadísticos
        percentiles = np.percentile(data, [25, 50, 75, 90, 95])
        skewness = skew(data)
        kurt = kurtosis(data)

        print("Percentiles (25th, 50th, 75th, 90th, 95th):", percentiles)
        print("Coeficiente de asimetría:", skewness)
        print("Curtosis:", kurt)