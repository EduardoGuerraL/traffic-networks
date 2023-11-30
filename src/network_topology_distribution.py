import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_distribution(data, name):

     # Crear una figura y ejes
    fig, ax = plt.subplots()

    # Ajustar el tamaño de las fuentes de los ejes X e Y
    ax.tick_params(axis='x', labelsize=18)  # Tamaño de fuente para el eje X
    ax.tick_params(axis='y', labelsize=18)  # Tamaño de fuente para el eje Y
    
    # Ajustar la cantidad de ticks en los ejes X e Y
    #ax.set_xticks([0.007, 0.01, 0.013, 0.016])
    #ax.set_yticks([0.1, 0.3, 0.5])

    # Ajustar el tamaño de las fuentes en las etiquetas y títulos
    
    ax.set_xlabel(rf'${name}$', fontsize=18)
    ax.set_ylabel(rf'$P[{name}]$', fontsize=18, rotation = 0)
    
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
    plt.savefig(f"distribution {name}")
    #plt.show()


#Simple 

data = pd.read_csv("data/DataNetwork/StreetAsNode/all_data_SimpleNet_new.csv")

print(data.info())

BC = data["BC"]
CC = data["CC"]
DC = data["DC"]
DiBC = data["DiBC"]
DiCC = data["DiCC"]
DiDC = data["DiDC"]
Max_ocupation = data["MaxOcupation"]
mean_rw = data["mean_state_RW"]
mean_rwm = data["mean_state_RWM"]
mean_rw_uplim = data["mean_state_RW_lim"]
mean_rwm_uplim = data["mean_state_RW_lim"]

"""
plot_distribution(BC, "C_B")
plot_distribution(CC, "C_C")
plot_distribution(DC, "C_D")
plot_distribution(DiBC, "C_{DB}")
plot_distribution(DiCC, "C_{DC}")
plot_distribution(DiDC, "C_{DD}")
plot_distribution(mean_rw, r"\langle N \rangle_{rw}")
plot_distribution(mean_rwm, r"\langle N \rangle_{rwm}")
plot_distribution(mean_rw_uplim, r"\langle N \rangle_{rw(lim)}")
plot_distribution(mean_rwm_uplim, r"\langle N \rangle_{rwm(lim)}")

plot_distribution(Max_ocupation, "N_{max}")
"""

#Complejo

data = pd.read_csv("data/DataNetwork/StreetAsNode/all_data_ComplexNet_new.csv")
print(data.info())

BC = data["BC"]
CC = data["CC"]
DC = data["DC"]
DiBC = data["DiBC"]
DiCC = data["DiCC"]
DiDC = data["DiDC"]
Max_ocupation = data["MaxOcupation"]
mean_rw = data["mean_state_RW"]
mean_rwm = data["mean_state_RWM"]
mean_rw_uplim = data["mean_state_RW_lim"]
mean_rwm_uplim = data["mean_state_RWM_lim"]

plot_distribution(BC, "C_B")
plot_distribution(CC, "C_C")
plot_distribution(DC, "C_D")
plot_distribution(DiBC, "C_{DB}")
plot_distribution(DiCC, "C_{DC}")
plot_distribution(DiDC, "C_{DD}")
plot_distribution(mean_rw, r"\langle N \rangle_{rw}")
plot_distribution(mean_rwm, r"\langle N \rangle_{rwm}")
plot_distribution(mean_rw_uplim, r"\langle N \rangle_{rw(lim)}")
plot_distribution(mean_rwm_uplim, r"\langle N \rangle_{rwm(lim)}")

plot_distribution(Max_ocupation, "N_{max}")