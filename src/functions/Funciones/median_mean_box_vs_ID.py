import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from functions.basics import obtener_nombres_con_H_M_sinFDS
import os
import scipy
import seaborn as sns
import math

def dividir_x_y(X, Y, N):
    # Calcula el rango de valores de X
    rango_x = max(X) - min(X)
    
    # Calcula el tamaño del intervalo
    tam_intervalo = rango_x / N

    # Inicializa listas vacías para almacenar los intervalos de X e Y
    intervalos_X = [[] for _ in range(N)]
    intervalos_Y = [[] for _ in range(N)]

    # Divide los valores de X e Y en los intervalos correspondientes
    for x, y in zip(X, Y):
        indice_intervalo = min(int((x - min(X)) / tam_intervalo), N - 1)
        intervalos_X[indice_intervalo].append(x)
        intervalos_Y[indice_intervalo].append(y)

    return intervalos_X, intervalos_Y

def ordenar_listas(X, Y):
    # Emparejar los valores de X e Y
    pares = list(zip(X, Y))

    # Ordenar los pares basados en los valores de X
    pares_ordenados = sorted(pares, key=lambda x: x[0])

    # Separar los valores ordenados nuevamente en X e Y
    X_ordenado, Y_ordenado = zip(*pares_ordenados)

    return list(X_ordenado), list(Y_ordenado)

def scatter_and_boxplot(X, Y, N):
    ## GRAFICANDO SCATTER CON BOXPLOT
    # Ordenar X de menor a mayor y reordenar Y en consecuencia
    X, Y = ordenar_listas(X, Y)

    # Dividir X e Y en N intervalos
    intervalos_X, intervalos_Y = dividir_x_y(X, Y, N)
    
    # Gráfico de diagrama de caja en el primer subplot
    Medianas = []
    Promedios = []
    Posiciones_X = []

    # Crear un subplot con dos gráficos en la misma fila
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 11), gridspec_kw={'width_ratios': [10, 1]})

    for i in range(N):
        if intervalos_X[i]:
            ancho = (intervalos_X[i][-1] - intervalos_X[i][0])
            positions = [intervalos_X[i][-1] - (ancho / 2)]
            
            promedio = np.mean(intervalos_Y[i])
            
            # Guardando datos[punto medio de x boxes, mean de Y, median de Y]
            Posiciones_X.append(positions[0])
            Promedios.append(promedio)
    
    # Gráfico de densidad en el segundo subplot (rotado en 90 grados)
    sns.kdeplot(Y, ax=ax2, color='green', vertical=True, common_norm = True)
    plt.hist(Y, orientation="horizontal", density=True, bins=20)
    ax2.set_xlabel("Densidad")
    ax2.set_ylim(0,1)
    ax2.set_xlim(0,12)
    ax2.set_yticks([])
 
    # Ajustar la distancia entre los subgráficos
    plt.subplots_adjust(wspace=0)

    Medianas = [np.median(subconjunto) for subconjunto in intervalos_Y]

    Medianas = [math.log10(i) for i in Medianas]
    Promedios = [math.log10(i) for i in Promedios]
    ax1.plot(Posiciones_X,Medianas)
    ax1.plot(Posiciones_X, Promedios)
    plt.show()

    return Medianas, Promedios, Posiciones_X

def CrearCarpeta(nombre_carpeta):
    # Ruta completa donde deseas crear la carpeta
    ruta_completa = os.path.join(os.getcwd(), nombre_carpeta)

    # Verifica si la carpeta no existe antes de crearla
    if not os.path.exists(ruta_completa):
        os.makedirs(ruta_completa)
        print(f"Se ha creado la carpeta '{nombre_carpeta}' en '{ruta_completa}'")
    else:
        pass

def reescalar_lista_de_listas(lista_de_listas, maximo):

    lista_reescalada = []

    for lista in lista_de_listas:
        lista_reescalada.append([valor / maximo for valor in lista])

    return lista_reescalada

def scatter4MeanObsValues(compu_data, list_of_list_of_Obs, carpetaSup, xlabel = "x"):

    # Calcular la media y desviación estándar de cada lista en list_of_list_of_Obs

    promedios = [np.mean(data) for data in list_of_list_of_Obs]

    # Obteniendo su skweness y kurtosis
    kurtosis = scipy.stats.kurtosis(promedios)
    skewness = scipy.stats.skew(promedios)
    
    ## GRAFICANDO 
    ### Agregando Cajas
    medians_box, means_box, pos_box = scatter_and_boxplot(list(compu_data), list(promedios), 20)

    
    ## REGRESION LINEAL
    #(slope, intercept, r_value, p_value, std_err)
    medians_params = scipy.stats.linregress(pos_box, medians_box)
    means_params = scipy.stats.linregress(pos_box, means_box)
    
    return medians_params, means_params, kurtosis, skewness

##########################################################################################################################
## Datos Computacionales

#"data/DataNetwork/StreetAsNode/all_data_SimpleNet_new.csv"
#"data/DataNetwork/StreetAsNode/all_data_ComplexNet_new.csv"
datos_comp = pd.read_csv("data/DataNetwork/StreetAsNode/all_data_ComplexNet_new.csv")

## Datos observacional

#"data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv"
#"data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_max.csv"
#"data/DataImages/In_Streets_Coord/Normal/streetsCoordsR1S4.csv"
#"data/DataImages/In_Streets_Coord/Normal/MaxStreetscoordsR0S6.csv"
#"data/DataImages/In_Streets_Coord/Normal/MeanStreetscoordsR0S6.csv"
datos_obs = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")

## Columnas de data_observacional Computacionales
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
nombres = ["BC",
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
#thresholds = [0, 60, 80, 100,130, 150, 200]

###########################################
nombres = ["CC"]
thresholds = [0]
############################################

Slopes = []
Kurtosis = []
Skewness = []
for threshold in thresholds:
    for name_column in nombres:
        
        data_computational = datos_comp[name_column]
        #data_computational = [(i-min(data_computational))/(max(data_computational)-min(data_computational)) for i in data_computational]
        
        ## Creando Carpeta
        Nombre_carpetaSuperior = "DataThresholdBox"+str(threshold)+"/"+name_column
        CrearCarpeta(Nombre_carpetaSuperior)
        
        hora_inicial, hora_final = 0, 24
        for hora_in in range(hora_inicial, hora_final):
            for minuto_in in range(0, 60, 15):

                columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
                data_observacional = datos_obs[columnas_elejidas].values.tolist()
                
                ## Reescalando los data_observacional de 0 a 1
                #data_observacional = reescalar_lista_de_listas(data_observacional, 255)                
                
                fit_params_medians,fit_params_means, kurtosis, skewness  = scatter4MeanObsValues(data_computational, data_observacional, carpetaSup = Nombre_carpetaSuperior, xlabel = name_column)
                
                Slopes.append(fit_params_medians[0])
                Kurtosis.append(kurtosis)
                Skewness.append(skewness)

