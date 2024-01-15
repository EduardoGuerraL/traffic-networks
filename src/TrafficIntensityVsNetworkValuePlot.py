"""
Grafica por cada instante de tiempo un Scatter entre:
la intensidad de trafico promedio de cada nodo 
vs 
el indice topologico que tengamos de la red.

Muestra la distrbucion de probabilidad de la intensidad
Divide en boxplots y muestra en azul su mediana.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import seaborn as sns
from functions import CrearCarpeta, obtener_nombres_con_H_M_sinFDS, reescalar_lista_de_listas, crearNintervalosOrdenados
from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales


def scatter_and_boxplot(X, Y, N):
    ## GRAFICANDO SCATTER CON BOXPLOT

    # Dividir X e Y en N intervalos
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, N)

    # Crear un subplot con dos gráficos en la misma fila
    plt.style.use(["science", "notebook", "grid"])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 11), gridspec_kw={'width_ratios': [10, 1]}, sharey=True)
    ax1.grid(True)
    # Gráfico de diagrama de caja en el primer subplot
    Medianas = []
    Posiciones_X = []
    for i in range(N):
        if intervalos_X[i]:
            ancho = (intervalos_X[i][-1] - intervalos_X[i][0])
            positions = [intervalos_X[i][-1] - (ancho / 2)]
            ax1.boxplot(intervalos_Y[i], positions=positions, widths=ancho, showfliers=False, patch_artist=True, boxprops={'facecolor': 'gray', 'alpha': 0.4}, medianprops={'color': 'blue', 'linewidth': 3})
            # Guardando datos[punto medio de x boxes, mean de Y, median de Y]
            Posiciones_X.append(positions[0])
  
    Medianas = [np.median(subconjunto) for subconjunto in intervalos_Y]

    # Configuración del primer subplot (gráfico de caja)
    ax1.scatter(X, Y, label="Scatter Plot", color='gray', alpha=0.1, s=20, edgecolor='black', marker='o')

    ax1.set_xlim(0,1)
    ax1.set_ylim(0,1)
    ax1.set_xticks([])
    #ax1.legend(loc='upper right')

    # Ajustar el tamaño de las fuentes en el gráfico
    xticks_values = [min(X), max(X)]
    formatted_xticks = ["{:.0f}".format(value) for value in xticks_values]
    
    ax1.set_xticks(xticks_values, formatted_xticks)

    
    # Gráfico de densidad en el segundo subplot (rotado en 90 grados)
    sns.kdeplot(Y, ax=ax2, color='blue', vertical=True, common_norm = True)
    plt.hist(Y, orientation="horizontal", density=True, bins=40, color="blue", alpha = 0.3)
    ax2.set_xlabel("")
    ax2.set_ylim(0,1)
    ax2.set_xlim(0,12)
    ax2.set_xticks([])
    return Medianas, Posiciones_X

def scatter4MeanObsValues(compu_data, list_of_list_of_Obs, carpetaSup,title,  xlabel = "x"):
    ## Usamos el promedio de 
    promedios = [np.mean(data) for data in list_of_list_of_Obs]
    
    ## GRAFICANDO 
    ### Agregando Cajas
    medians_box, pos_box = scatter_and_boxplot(list(compu_data), list(promedios), 20)
    
    ## REGRESION LINEAL
    #(slope, intercept, r_value, p_value, std_err)
    medians_params = scipy.stats.linregress(pos_box, medians_box)    

    ## Guardando los graficos
    NombreCarpeta = carpetaSup+"/"+str(xlabel) + "mean"
    CrearCarpeta(NombreCarpeta)

    plt.tight_layout()
    # Ajustar la distancia entre los subgráficos
    plt.subplots_adjust(wspace=0)

    plt.savefig(NombreCarpeta+"/Boxscatter_"+str(xlabel)+"_"+str(title)+".png")
    #plt.show()


    return medians_params

##########################################################################################################################
## Datos Computacionales
datos_comp = pd.read_csv(Datos_computacionales[1])

## Datos observacional
datos_obs = pd.read_csv(Datos_observacionales[0])


## Columnas de data_observacional Computacionales
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
            "mean_state_RWM_lim"]

###########################################
nombres = ["DiCC"]
############################################

for name_column in nombres:
    
    data_computational = datos_comp[name_column]
    data_computational = [(i-min(data_computational))/(max(data_computational)-min(data_computational)) for i in data_computational]
    ## Creando Carpeta
    Nombre_carpetaSuperior = "Data/"+name_column
    CrearCarpeta(Nombre_carpetaSuperior)
    
    hora_inicial, hora_final = 0, 24
    for hora_in in range(hora_inicial, hora_final):
        for minuto_in in range(0, 60, 15):

            columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
            data_observacional = datos_obs[columnas_elejidas].values.tolist()
            
            ## Reescalando los data_observacional de 0 a 1
            data_observacional = reescalar_lista_de_listas(data_observacional, 255)                
            
            fit_params_medians  = scatter4MeanObsValues(data_computational, data_observacional, carpetaSup = Nombre_carpetaSuperior, xlabel = name_column, title= str(hora_in)+"_"+str(minuto_in))
    