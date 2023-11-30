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

def plot_scatter(data_x, data_y, title):
    # Configurar el estilo de Seaborn
    sns.set(style="whitegrid")

    # Crear el diagrama de dispersión
    plt.figure(figsize=(8, 6))  # Ajustar el tamaño de la figura (opcional)
    sns.scatterplot(x=data_x, y=data_y, color='red', s=100, alpha=0.7)

    # Personalizar el título y los ejes
    plt.title(title, fontsize=18)
    plt.xlabel('Data CI', fontsize=18)
    plt.ylabel('Promedio observacional de una calle ', fontsize=18)

    # Ajustar las fuentes para que sean más grandes y legibles en un paper
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    # Mostrar el gráfico
    plt.tight_layout()  # Ajustar el diseño para evitar recortes
    plt.show()

fracciones = get_porcentaje()

#Datos Observacionales
def total():
    totaldatos_mean = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")
    promedios_total = []
    for indice_i in totaldatos_mean.index:
        data_street = totaldatos_mean.iloc[indice_i][4:]
        promedio = round(np.mean(data_street), 1)
        promedios_total.append(promedio)


    plot_scatter(fracciones, promedios_total)

def total_sinFDS():
    totaldatos_mean = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1_sinFDS.csv")
    promedios_total = []
    for indice_i in totaldatos_mean.index:
        data_street = totaldatos_mean.iloc[indice_i][5:]
        promedio = round(np.mean(data_street), 1)
        promedios_total.append(promedio)

    plot_scatter(fracciones, promedios_total, "total sin FDS")

def total_por_hora(hora):
    totaldatos_mean = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/ForHour_sinFDS_meanS2_r1/Data_"+str(hora)+"-00.scv")
    promedios_total = []
    for indice_i in totaldatos_mean.index:
        data_street = totaldatos_mean.iloc[indice_i][1:]
        promedio = round(max(data_street), 1)
        promedios_total.append(promedio)

    plot_scatter(fracciones, promedios_total, "Hora= "+str(hora))

#Indices de centralidad
#ejes:
def total_ci():
    totaldatos_mean = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")
    promedios_total = []
    
    data = pd.read_csv("data/DataNetwork/StreetAsNode/Basic_and_advaced_data_network_aristas_detallado.csv")

    dataBC = data["Betweenness_streets"]
    dataCC = data["Closeness_streets"]
    dataDC = data["Degree_streets"]
    
    for indice_i in totaldatos_mean.index:
        data_street = totaldatos_mean.iloc[indice_i][4:]
        promedio = round(np.mean(data_street), 1)
        promedios_total.append(promedio)


    plot_scatter(dataBC, promedios_total, "Betweenness_streets")
    plot_scatter(dataCC, promedios_total, "Closeness_streets")
    plot_scatter(dataDC, promedios_total, "Degree_streets")

def total_por_hora_ci(hora):
    totaldatos_mean = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/ForHour_sinFDS_meanS2_r1/Data_"+str(hora)+"-00.scv")
    promedios_total = []

    data = pd.read_csv("data/DataNetwork/StreetAsNode/Basic_and_advaced_data_network_aristas_detallado.csv")
    dataBC = data["Betweenness_streets"]
    dataCC = data["Closeness_streets"]
    dataDC = data["Degree_streets"]
    

    for indice_i in totaldatos_mean.index:
        data_street = totaldatos_mean.iloc[indice_i][1:]
        promedio = round(max(data_street), 1)
        promedios_total.append(promedio)

    plot_scatter(dataBC, promedios_total, "Hora= "+str(hora))
    plot_scatter(dataCC, promedios_total, "Hora= "+str(hora))
    plot_scatter(dataDC, promedios_total, "Hora= "+str(hora))

def total_sinFDS_ci():
    totaldatos_mean = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1_sinFDS.csv")
    promedios_total = []

    data = pd.read_csv("data/DataNetwork/StreetAsNode/Basic_and_advaced_data_network_aristas_detallado.csv")
    dataBC = data["Betweenness_streets"]
    dataCC = data["Closeness_streets"]
    dataDC = data["Degree_streets"]
    

    for indice_i in totaldatos_mean.index:
        data_street = totaldatos_mean.iloc[indice_i][5:]
        promedio = round(np.mean(data_street), 1)
        promedios_total.append(promedio)
    
    plot_scatter(dataBC, promedios_total, "Betweenness_streets")
    plot_scatter(dataCC, promedios_total, "Closeness_streets")
    plot_scatter(dataDC, promedios_total, "Degree_streets")


#RED SIMPLE 
#nodos
def total_simple():
    
    totaldatos_mean = pd.read_csv("data/DataImages/In_Intersection_Coord/Normal/intersectionCoord_basic.csv")
    promedios_total = []
    for indice_i in totaldatos_mean.index:
        data_street = totaldatos_mean.iloc[indice_i][4:]
        promedio = round(max(data_street), 1)
        promedios_total.append(promedio)

    
    data = pd.read_csv("data/DataNetwork/InterAsNode/Basic_and_advaced_data_network_nodes.csv")
    dataBC = data["BC"]
    dataCC = data["CC"]
    dataDC = data["DC"]
    
    data = pd.read_csv("data/DataNetwork/InterAsNode/Basic_and_advaced_data_network_nodes.csv")
    dataBC = data["DiBC"]
    dataCC = data["DiCC"]
    dataDC = data["DiDC"]

    plot_scatter(dataBC, promedios_total, "Betweenness_streets directed")
    plot_scatter(dataCC, promedios_total, "Closeness_streets directed")
    plot_scatter(dataDC, promedios_total, "Degree_streets directed")

#edges
def total_simple_ejes():
    
    totaldatos_mean = pd.read_csv("data/DataImages/In_Streets_Coord/Normal/streetsCoordsR1S6.csv")
    promedios_total = []
    for indice_i in totaldatos_mean.index:
        data_street = totaldatos_mean.iloc[indice_i][4:]
        promedio = round(np.mean(data_street), 1)
        promedios_total.append(promedio)

    
    data = pd.read_csv("data/DataNetwork/StreetAsNode/Basic_and_advaced_data_network_aristas.csv")
    dataBC = data["Betweenness_streets"]
    dataCC = data["Closeness_streets"]
    dataDC = data["Degree_streets"]


    plot_scatter(dataBC, promedios_total, "Betweenness streets directed")
    plot_scatter(dataCC, promedios_total, "Closeness streets directed")
    plot_scatter(dataDC, promedios_total, "Degree streets directed")



total_simple_ejes()
#for i in ["07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22"]:
 #   total_por_hora_ci(i)

#total_sinFDS_ci()