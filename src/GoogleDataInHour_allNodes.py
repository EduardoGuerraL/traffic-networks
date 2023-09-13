import csv
from PIL import Image
import imageio
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime

def obtener_nombres_con_H_M_sinFDS(lista_nombres,  hora_exacta=None, rango_horas=None):
    nombres_coincidentes = []
    patron = r"/\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(?:\.png)?"

    for nombre in lista_nombres:
        match = re.search(patron, nombre)
        if match:
            fecha_str = match.group(0).split(".")[0].split("/")[1]
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d_%H-%M")

            hora_minutos_str = match.group(0).split(".")[0].split("_")[1]
            hora = int(hora_minutos_str.split("-")[0])
            minutos = int(hora_minutos_str.split("-")[1])

            if fecha.weekday() < 5:
                if hora_exacta is not None:
                    if hora == hora_exacta[0] and minutos == hora_exacta[1]:
                        nombres_coincidentes.append(nombre)
                elif rango_horas is not None:
                    hora_inicial = rango_horas[0]
                    hora_final = rango_horas[1]

                    for hora_in in range(hora_inicial, hora_final):
                        for minuto_in in range(0, 60, 15):
                            if hora == hora_in and minutos == minuto_in:
                                nombres_coincidentes.append(nombre)
                else:
                    nombres_coincidentes.append(nombre)


    return nombres_coincidentes

def graficar_listas_en_columnas(lista_de_listas):
    num_sublistas = len(lista_de_listas)

    plt.figure(figsize=(10, 6))
    for i, sublista in enumerate(lista_de_listas):
        x_values = [i] * len(sublista)
        y_values = sublista
        plt.scatter(x_values, y_values, label=f'Lista {i}')
    
    plt.tight_layout()
    plt.show()
##########################################################################################################################

#NETWORK COMPLEJA

#observacional
datos_obs = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")


columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(8, 30))
datos_new = datos_obs[columnas_elejidas].values.tolist()

#graficar_listas_en_columnas(datos_new)
datos = datos_new

medianas = [np.median(lista) for lista in datos]
iqr_lower = [np.percentile(lista, 25) for lista in datos]
iqr_upper = [np.percentile(lista, 75) for lista in datos]
iqr = [upper - lower for lower, upper in zip(iqr_lower, iqr_upper)]

plt.figure(figsize=(10, 6))
plt.bar(range(len(datos)), iqr, bottom=iqr_lower, color='skyblue', label='IQR')
plt.scatter(range(len(datos)), medianas, color='red', label='Mediana', zorder=5)

plt.xticks(range(len(datos)), [f'Lista {i+1}' for i in range(len(datos))])
plt.tight_layout()

plt.show()