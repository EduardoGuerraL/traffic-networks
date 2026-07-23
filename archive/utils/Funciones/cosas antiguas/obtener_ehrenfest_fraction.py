import pandas as pd
import numpy as np

def get_porcentaje():
    ehrenfest = pd.read_csv("data/DataNetwork/StreetAsNode/estado_ejes_500M_10msteps.csv")
    maximo_autos = pd.read_csv("data/N_max_autos_por_calle.csv")
    maximo_autos = maximo_autos.iloc[:,1]
    
    promedios = []
    for indice_i in ehrenfest.index:
        data_street = ehrenfest.iloc[indice_i][1:]
        promedio = round(np.mean(data_street), 1)
        promedios.append(promedio)

    fracciones = [round(i/j, 1) for i, j in zip(promedios, maximo_autos)]

    return fracciones

import seaborn as sns
import matplotlib.pyplot as plt

def plot_distribution(data):
    # Configurar el estilo de Seaborn
    sns.set(style="whitegrid")

    # Crear el histograma con distribución de densidad suavizada-
    plt.figure(figsize=(8, 6))  # Ajustar el tamaño de la figura (opcional)
    sns.histplot(data, kde=True, color='skyblue', bins=20)

    # Personalizar el título y los ejes
    plt.title("Distribución BC", fontsize=18)
    plt.xlabel('Fraccion de llenado', fontsize=18)
    plt.ylabel('Frecuencia', fontsize=18)

    # Ajustar las fuentes para que sean más grandes y legibles en un paper
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    # Mostrar el gráfico
    plt.tight_layout()  # Ajustar el diseño para evitar recortes
    plt.show()

def plot_distribution_multiple(data_list, labels, title):
    # Configurar el estilo de Seaborn
    sns.set(style="whitegrid")

    # Crear el histograma con distribución de densidad suavizada
    plt.figure(figsize=(8, 6))  # Ajustar el tamaño de la figura (opcional)
    for data, label in zip(data_list, labels):
        sns.histplot(data, kde=True, label=label, alpha=0.7)

    # Personalizar el título y los ejes
    plt.title(title, fontsize=18)
    plt.xlabel('Valores', fontsize=18)
    plt.ylabel('Frecuencia', fontsize=18)

    # Ajustar las fuentes para que sean más grandes y legibles en un paper
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    # Mostrar la leyenda con las etiquetas de cada histograma
    plt.legend(fontsize=18)

    # Ajustar el diseño para evitar recortes y mostrar el gráfico
    plt.tight_layout()
    plt.show()

def reescalar(data):               
    max_valor = max(data)
    min_valor = min(data)
        
    if min_valor == 0 and max_valor == 0:
        pass
    else:
        data = [round((valor - min_valor) / (max_valor - min_valor),3) for valor in data]
    return data

data = pd.read_csv("data/DataNetwork/InterAsNode/Basic_and_advaced_data_network_nodes.csv")

data_detallado = pd.read_csv("data/DataNetwork/InterAsNode/Basic_and_advaced_data_network_nodes_detallado.csv")


#dataBC = data["BC"]
#dataCC = data["CC"]
#dataDC = data["DC"]

#dataBC = reescalar(data["DiBC"])
#dataCC = reescalar(data["DiCC"])
#dataDC = reescalar(data["DiDC"])
#plot_distribution_multiple((dataBC, dataCC, dataDC), ("DiBC", "DiCC", "DiDC"), "distribution CI nodes directed")


#dataBC = reescalar(data_detallado["BC"])
#dataCC = reescalar(data_detallado["CC"])
#dataDC = reescalar(data_detallado["DC"])
#plot_distribution_multiple((dataBC, dataCC, dataDC), ("BC", "CC", "DC"), "distribution CI nodes")

#ejes 
#data = pd.read_csv("data/DataNetwork/StreetAsNode/Basic_and_advaced_data_network_aristas.csv")

#dataBC = reescalar(data["Betweenness_streets"])
#dataCC = reescalar(data["Closeness_streets"])
#dataDC = reescalar(data["Degree_streets"])
#plot_distribution_multiple((dataBC, dataCC, dataDC), ("BC", "CC", "DC"), "distribution CI street as node")


data = pd.read_csv("data/DataNetwork/StreetAsNode/Basic_and_advaced_data_network_aristas_detallado.csv")

dataBC = reescalar(data["Betweenness_streets"])
dataCC = reescalar(data["Closeness_streets"])
dataDC = reescalar(data["Degree_streets"])

plot_distribution_multiple((dataBC, dataCC, dataDC), ("BC", "CC", "DC"), "distribution CI street as node")
