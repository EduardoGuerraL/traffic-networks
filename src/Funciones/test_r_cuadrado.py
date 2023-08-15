from functions import calcular_r_cuadrado, obtener_nombres_con_H_M
import pandas as pd
import numpy as np

#observacional
datos_obs = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")

#computacional

datos_comp = pd.read_csv("data/DataNetwork/StreetAsNode/Basic_and_advaced_data_network_aristas_detallado.csv")
lista_de_datos_comp_2 = datos_comp["Closeness_streets"].tolist()
lista_de_datos_comp = datos_comp["Betweenness_streets"].tolist()
lista_de_datos_comp_3 = datos_comp["Degree_streets"].tolist()

datos_computacionales = lista_de_datos_comp

#almacenar los resultados
horas = []
MAE = []
Pendientes = []
Interseptos = []
Error_sqrt_medio = []
std_devs = []
r2_values = []
r2_values_ajust = []
hora_inicial, hora_final = 0, 24

for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):
        columnas_elejidas = obtener_nombres_con_H_M(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
        datos_new = datos_obs[columnas_elejidas].values.tolist()
        datos_new_mean = [np.mean(lista) for lista in datos_new]

        r = calcular_r_cuadrado(datos_computacionales, datos_new_mean)
        
        print(r)