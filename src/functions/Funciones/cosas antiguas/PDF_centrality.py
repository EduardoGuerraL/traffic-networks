import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_distribution(data):

     # Crear una figura y ejes
    fig, ax = plt.subplots()

    # Ajustar el tamaño de las fuentes de los ejes X e Y
    ax.tick_params(axis='x', labelsize=18)  # Tamaño de fuente para el eje X
    ax.tick_params(axis='y', labelsize=18)  # Tamaño de fuente para el eje Y
    
    # Ajustar la cantidad de ticks en los ejes X e Y
    ax.set_xticks([0.007, 0.01, 0.013, 0.016])
    ax.set_yticks([0.1, 0.3, 0.5])

    # Ajustar el tamaño de las fuentes en las etiquetas y títulos
    ax.set_xlabel(r'$C_D$', fontsize=18)
    ax.set_ylabel(r'$P[C_D]$', fontsize=18, rotation = 0)
    
    # Ajustar las coordenadas de las etiquetas de los ejes X e Y
    ax.xaxis.set_label_coords(1.04, 0.04)  
    ax.yaxis.set_label_coords(0, 1.01)

    # Eliminar el contorno superior y derecho del gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Graficar el histograma con las alturas de las barras ajustadas
    sns.histplot(data, bins=20, kde=True, color='red', ax=ax, stat="probability")

    # Agregar líneas de cuadrícula en el eje Y
    #ax.yaxis.grid(True)
    plt.tight_layout()
    # Mostrar el gráfico
    plt.show()


data = pd.read_csv("data/DataNetwork/InterAsNode/Basic_and_advaced_data_network_nodes.csv")

dataBC = data["DiBC"]
dataCC = data["DiCC"]
dataDC = data["DiDC"]

plot_distribution(dataDC)
