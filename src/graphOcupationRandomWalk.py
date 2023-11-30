import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns

def graph(indice_i, name):
    # Datos de red Simple
    #df = pd.read_csv("data/DataNetwork/StreetAsNode/SimpleNet_states_10mA_500BT_10mS_streets.csv")
    #df_max = pd.read_csv("data/DataNetwork/StreetAsNode/SimpleNet_max_ocupation_per_streets.csv")
    
    # Datos de red Detallada
    df = pd.read_csv("data/DataNetwork/StreetAsNode/ResultData/ComplexNet_Ehr_10mA_500MT_UpperLimit.csv")
    df_max = pd.read_csv("data/DataNetwork/StreetAsNode/ResultData/ComplexNet_max_ocupation_per_streets.csv")

    # Crear una figura y ejes
    fig, ax = plt.subplots()
    # Ajustar el tamaño de las fuentes de los ejes X e Y
    ax.tick_params(axis='x', labelsize=18)  # Tamaño de fuente para el eje X
    ax.tick_params(axis='y', labelsize=18)  # Tamaño de fuente para el eje Y

     # Ajustar el tamaño de las fuentes en las etiquetas y títulos
    
    ax.set_xlabel(rf'${name}$', fontsize=18)
    ax.set_ylabel(rf'$P[{name}]$', fontsize=18, rotation = 0)

    # Ajustar las coordenadas de las etiquetas de los ejes X e Y
    ax.xaxis.set_label_coords(1.04, 0.04)  
    ax.yaxis.set_label_coords(0, 1.01)

    # Seleccionar la columna del índice específico
    data_street = df.iloc[indice_i][1:]
    max_car_in_street = df_max.iloc[indice_i][1]

    # Eliminar el contorno superior y derecho del gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    
    sns.axhline(y=max_car_in_street, color='red', linestyle='-')
    # Etiqueta la recta con 'Max'
    sns.text(0.5, max_car_in_street + 0.1, 'Max', color='red', fontsize=18)

    data_time = [int(val) for val in data_street.index]
    ## Graficar el avance en el tiempo del índice i
    sns.plot(data_time, data_street.values)

    # Mostrar solo el primer, último y valor medio del intervalo
    marcadores = [data_time[0], data_time[-1], data_time[len(data_time)//2]]
    etiquetas = [f'{val:.1e}' for val in marcadores]

    plt.xticks(marcadores, etiquetas)

    #dibujar linea promedio de datos
    promedio = round(np.mean(data_street), 1)
    sns.axhline(y=promedio, color='red', linestyle='-')
    # Etiqueta la recta con 'Min'
    sns.text(0.5, promedio + 0.1, 'Mean', color='red', fontsize=18)

    plt.tight_layout()  # Elimina espacios en los bordes
    plt.show()

def grapf2(indice_i):

    # Datos de red Detallada
    df = pd.read_csv("data/DataNetwork/StreetAsNode/ResultData/SimpleNet_Ehr_10mA_500MT_UpperLimit.csv")
    df_max = pd.read_csv("data/DataNetwork/StreetAsNode/ResultData/SimpleNet_max_ocupation_per_streets.csv")

    #Ajustes

    # Crear una figura y ejes
    fig, ax = plt.subplots()
    # Ajustar el tamaño de las fuentes de los ejes X e Y
    ax.tick_params(axis='x', labelsize=18)  # Tamaño de fuente para el eje X
    ax.tick_params(axis='y', labelsize=18)  # Tamaño de fuente para el eje Y
    # Ajustar el tamaño de las fuentes en las etiquetas y títulos
    ax.set_ylabel(r'$x/N$', fontsize=18, rotation = 0)
    ax.set_xlabel(r'$t$', fontsize=18)
    # Ajustar las coordenadas de las etiquetas de los ejes X e Y
    ax.xaxis.set_label_coords(1.04, 0.04)
    ax.yaxis.set_label_coords(0, 1.01)
    # Eliminar el contorno superior y derecho del gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(0,1)


    # Seleccionar la columna del índice específico
    data_street = df.iloc[indice_i][1:]
    max_car_in_street = df_max.iloc[indice_i][1]

    fraction = [i/max_car_in_street for i in data_street.values]
    data_time = [int(val) for val in data_street.index]
    promedio = np.mean(fraction)

    # Graficar
    sns.lineplot(x=data_time, y=fraction, ax=ax, color = "orangered")
    sns.lineplot(x=data_time, y=promedio, color='blue', ax=ax)

    # Mostrar solo el primer, último y valor medio del intervalo
    marcadores = [data_time[0], data_time[-1], data_time[len(data_time)//2]]
    etiquetas = [f'{val:.1e}' for val in marcadores]
    ax.set_xticks(marcadores)
    ax.set_xticklabels(etiquetas)

    plt.tight_layout()  # Elimina espacios en los bordes
    plt.savefig(f"calle {indice_i}")
    #plt.show()


for i in range(16):
    x = random.randint(0, 505)
    print(x)
    grapf2(x)