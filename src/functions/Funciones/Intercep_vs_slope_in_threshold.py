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
"R2_mean"=
"R2_median"
"R2_max"
"P_mean"
"P_median"
"P_max"
"stdDev_mean"
"stdDev_median"
"stdDev_max"
"""

"""
## Columnas de datos Computacionales
#"BC"
#"CC"
#"DC"
#"DiBC"
#"DiCC"
#"DiDC"
#"MaxOcupation"
#"mean_state_RW"
#"mean_state_RW_lim"
#"mean_state_RWM"
#"mean_state_RWM_lim"
"""


names = ["BC",
        "CC",
        "DC",
        "DiBC",
        "DiCC",
        "DiDC",
        "MaxOcupation",
        "mean_state_RW",
        "mean_state_RW_lim",
        "mean_state_RWM",
        "mean_state_RWM_lim"
]

#name = "BC"
tipo = "mean"

for name in names:

    tresholds = [0,40,60,80,100,120,140,160,170]
    num_rows = 3  # Número de filas en la cuadrícula
    num_cols = len(tresholds) // num_rows  # Número de columnas en la cuadrícula

    # Crear una figura con una cuadrícula de subgráficos
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(num_cols * 8, num_rows * 6))

    for i, treshold in enumerate(tresholds):
        treshold = str(treshold)
        name_datos = "Thresholds/Threshold" + treshold + "/" + name + "/datos_" + name + "_treshold_" + treshold + "complex.dat"
        df = pd.read_csv(name_datos)

        # Obtener los datos para graficar
        X = df["Pendientes_"+str(tipo)]
        Y = df["Intercepto_"+str(tipo)]
        S = df["R2_"+str(tipo)].apply(lambda x: x**2)
        promedio_ocupacion_total = df["mean_total_ocupation"]

        # Calcular las coordenadas de la fila y la columna actual en la cuadrícula
        row = i // num_cols
        col = i % num_cols

        # Crear un gráfico de dispersión con colores basados en la lista promedio_ocupacion_total
        scatter = axs[row, col].scatter(X, Y, c=promedio_ocupacion_total,s = S*80/max(S), cmap='turbo', marker='o', label=rf'MaxR^2 = {round(max(S),2)}')

        # Agregar barra de color
        cbar = fig.colorbar(scatter, ax=axs[row, col])
        cbar.set_label('mean total ocupation', fontsize=10)

        # Etiquetas y título
        axs[row, col].set_xlabel(r'$m$', fontsize=10)
        axs[row, col].set_ylabel(r'$b$', fontsize=10)
        axs[row, col].set_title(rf'${name}$, T = {treshold}', fontsize=10)

        # Agregar leyenda al gráfico
        axs[row, col].legend()

        axs[row, col].tick_params(labelsize=10)

    # Ajustar el espaciado entre subgráficos
    plt.tight_layout()

    # Ajustar el espaciado entre subgráficos y la distancia desde la parte superior
    plt.subplots_adjust(hspace=0.4, wspace=0.15, top=0.97)


    # Mostrar el gráfico con la cuadrícula de imágenes
    #plt.savefig("Parametros_"+str(name)+"_"+str(tipo)+".png",bbox_inches='tight')
    plt.show()

    """
    for treshold in tresholds:
        treshold = str(treshold)
        name_datos = "Thresholds/Threshold"+str(treshold)+"/"+str(name)+"/datos_"+str(name)+"_treshold_"+str(treshold)+"complex.dat"
        df = pd.read_csv(name_datos)

        ## Datos_ocupados para graficar:
        
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

        X = df["Pendientes_mean"]
        Y = df["Intercepto_mean"]
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
        plt.title(rf'${name}$, T = {treshold}',  fontsize=20)


        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)

        plt.tight_layout()
        # Mostrar el gráfico
        plt.show()

    """