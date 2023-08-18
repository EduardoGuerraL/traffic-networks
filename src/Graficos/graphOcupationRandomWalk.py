import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random

def graph(indice_i):
    # Datos de red Simple
    #df = pd.read_csv("data/DataNetwork/StreetAsNode/SimpleNet_states_10mA_500BT_10mS_streets.csv")
    #df_max = pd.read_csv("data/DataNetwork/StreetAsNode/SimpleNet_max_ocupation_per_streets.csv")
    
    # Datos de red Detallada
    df = pd.read_csv("data/DataNetwork/StreetAsNode/estado_ejes_500M_10msteps.csv")
    df_max = pd.read_csv("data/DataNetwork/StreetAsNode/ComplexNet_Max_ocupation_per_strets.csv")

    # Seleccionar la columna del índice específico
    data_street = df.iloc[indice_i][1:]
    max_car_in_street = df_max.iloc[indice_i][1]

    plt.rc('font', size=18)
    # Dibuja la recta roja horizontal
    plt.axhline(y=max_car_in_street, color='red', linestyle='-')
    # Etiqueta la recta con 'Max'
    plt.text(0.5, max_car_in_street + 0.1, 'Max', color='red', fontsize=18)

    data_time = [int(val) for val in data_street.index]
    ## Graficar el avance en el tiempo del índice i
    plt.plot(data_time, data_street.values)
    plt.xlabel('')
    plt.ylabel('autos en calle')
    plt.title(f'Calle {indice_i}')

    # Mostrar solo el primer, último y valor medio del intervalo
    marcadores = [data_time[0], data_time[-1], data_time[len(data_time)//2]]
    etiquetas = [f'{val:.1e}' for val in marcadores]

    plt.xticks(marcadores, etiquetas)

    #dibujar linea promedio de datos
    promedio = round(np.mean(data_street), 1)
    plt.axhline(y=promedio, color='red', linestyle='-')
    # Etiqueta la recta con 'Min'
    plt.text(0.5, promedio + 0.1, 'Mean', color='red', fontsize=18)

    plt.tight_layout()  # Elimina espacios en los bordes
    plt.show()

for i in range(10):
    x = random.randint(0, 500)
    print(x)
    graph(x)