import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr
import numpy as np

def reescalar(data):
    
    max_valor = 255
    min_valor = 0
    
    if min_valor == 0 and max_valor == 0:
        pass
    else:
        data = [round((valor - min_valor) / (max_valor - min_valor),3) for valor in data]

    return data

def estadisticas(lista1, lista2):
    # Convertir las listas en arreglos numpy
    array1 = np.array(lista1)
    array2 = np.array(lista2)

    # Calcular el coeficiente de Pearson y su valor p
    pearson_corr, pearson_p_value = pearsonr(array1, array2)

    # Calcular el coeficiente de determinación (R cuadrado)
    r_squared = pearson_corr ** 2

    # Calcular el coeficiente de Spearman y su valor p
    spearman_corr, spearman_p_value = spearmanr(array1, array2)

    print("Coeficiente de Pearson:", pearson_corr)
    print("Valor p (Pearson):", pearson_p_value)
    print("Coeficiente de Determinación (R cuadrado):", r_squared)
    print("Coeficiente de Spearman:", spearman_corr)
    print("Valor p (Spearman):", spearman_p_value)

#ehr sim
data_pc = pd.read_csv("datos_comp_percent.csv")
data_computacional = data_pc[data_pc.columns[-1]]

#betwenness_nx
data_pc = pd.read_csv("datos_network_streets_det.csv")
data_computacional = data_pc["Betweenness_streets"]

for hora in range(6,23):
    for minutos in ["00", "30"]:
        hora_temp = str(hora).zfill(2) +"-"+minutos
        data_obs_hora = pd.read_csv("data/DataImages/In_Streets_Coord/ForHour_sinFDS/Data_"+str(hora_temp)+".scv")
        
        prom = list(data_obs_hora["Promedio"])
        maximo = list(data_obs_hora["Máximo"])
        minimo = list(data_obs_hora["Mínimo"])

        prom = reescalar(prom)
        maximo = reescalar(maximo)
        minimo = reescalar(minimo)

        estadisticas(prom, data_computacional)
        estadisticas(maximo, data_computacional)
        estadisticas(minimo, data_computacional)

        plt.scatter(prom, data_computacional, label = "Promedio", alpha= 0.3)
        plt.scatter(maximo, data_computacional, label = "Maximos", alpha= 0.3)
        plt.scatter(minimo, data_computacional, label = "Minimos", alpha= 0.3)
        plt.legend()
        plt.show()

        