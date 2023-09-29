import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Función para convertir la hora en formato string a float
def convertir_hora(hora_string):
    partes = hora_string.split(":")
    horas = float(partes[0])
    minutos = float(partes[1]) / 60.0
    return horas + minutos

"""
## Nombres Disponibles
"mean_total_ocupation"
"Pendientes_mean"
"Pendientes_median"
"Pendientes_max"
"Intercepto_mean"
"Intercepto_median"
"Intercepto_max"
"R2_mean"]=
"R2_median"
"R2_max"
"P_mean"
"P_median"
"P_max"
"stdDev_mean"
"stdDev_median"
"stdDev_max"
"""


tresholds = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170]
name = "CC"

for treshold in tresholds:
    treshold = str(treshold)
    name_datos = "Threshold"+str(treshold)+"/"+str(name)+"/datos_"+str(name)+"_treshold_"+str(treshold)+"complex.dat"
    df = pd.read_csv(name_datos)

    ## Datos_ocupados para graficar:
    """
    ## Nombres Disponibles
    "mean_total_ocupation"
    "Pendientes_mean"
    "Pendientes_median"
    "Pendientes_max"
    "Intercepto_mean"
    "Intercepto_median"
    "Intercepto_max"
    "R2_mean"]=
    "R2_median"
    "R2_max"
    "P_mean"
    "P_median"
    "P_max"
    "stdDev_mean"
    "stdDev_median"
    "stdDev_max"
    """
    X = df["Pendientes_max"]
    Y = df["Intercepto_max"]
    promedio_ocupacion_total = df["mean_total_ocupation"]

    # Lista de horas convertidas a float
    horas = df["horas"]
    horas = np.array([convertir_hora(hora_string) for hora_string in horas])

    # Crear un gráfico de dispersión con colores basados en la lista color_data
    plt.figure(figsize=(8, 6))  # Ajustar el tamaño de la figura
    scatter = plt.scatter(X, Y, c=promedio_ocupacion_total,  cmap='turbo', marker='o', label='Datos')

    # Agregar barra de color
    cbar = plt.colorbar(scatter)
    cbar.set_label('mean total ocupation',  fontsize=20)


    # Etiquetas y título
    plt.xlabel(r'$m$',  fontsize=20)
    plt.ylabel(r'$b$',  fontsize=20)
    plt.title(rf'${name}$',  fontsize=20)


    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    plt.tight_layout()
    # Mostrar el gráfico
    plt.show()
