import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import seaborn as sns
from functions.basics import *

def scatter_and_boxplot(X, Y, N):
   
    # Dividir X e Y en N intervalos
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, N)


    # Crear un gráfico de diagrama de caja para cada intervalo con transparencia
    for i in range(N):
        if intervalos_X[i]:
            ancho = (intervalos_X[i][-1] - intervalos_X[i][0])
            positions = [intervalos_X[i][-1]-(ancho/2)]
            plt.boxplot(intervalos_Y[i], positions=positions, widths=ancho, showfliers=False, patch_artist=True, boxprops={'facecolor': 'blue', 'alpha': 0.5}, medianprops={'color': 'yellow'})
            
            plt.scatter(positions, np.mean(intervalos_Y[i]), color = "r", s = 50)


    # Configurar el estilo de los puntos de dispersión como pequeños anillos grises con opacidad
    plt.scatter(X, Y, label="Scatter Plot", color='gray', alpha=0.1, s=20, edgecolor='black', marker='o')
    # Agregar líneas verticales punteadas en max(intervalo_X)
    for intervalo_X in intervalos_X:
        if intervalo_X:
            plt.axvline(max(intervalo_X), linestyle='--', color='gray', alpha=0.5)

    # Configurar etiquetas y leyenda
    plt.xlim(min(X), max(X))
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(loc='upper right')

    # Mostrar el gráfico
    #plt.show()

def scatter_and_boxplot_with_density_Y(X, Y, N):

    # Dividir X e Y en N intervalos
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, N)

    # Crear un subplot con dos gráficos en la misma fila
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), gridspec_kw={'width_ratios': [10, 1]})

    # Gráfico de diagrama de caja en el primer subplot
    for i in range(N):
        if intervalos_X[i]:
            ancho = (intervalos_X[i][-1] - intervalos_X[i][0])
            positions = [intervalos_X[i][-1] - (ancho / 2)]
            ax1.boxplot(intervalos_Y[i], positions=positions, widths=ancho, showfliers=False, patch_artist=True, boxprops={'facecolor': 'blue', 'alpha': 0.5}, medianprops={'color': 'yellow'})
            ax1.scatter(positions, np.mean(intervalos_Y[i]), color="r", s=50)

    # Configuración del primer subplot (gráfico de caja)
    ax1.scatter(X, Y, label="Scatter Plot", color='gray', alpha=0.1, s=20, edgecolor='black', marker='o')
    for intervalo_X in intervalos_X:
        if intervalo_X:
            ax1.axvline(max(intervalo_X), linestyle='--', color='gray', alpha=0.5)
    
    ax1.set_xlim(min(X), max(X))
    ax1.set_ylim(0,260)
    ax1.set_xlabel("CC")
    ax1.set_ylabel("Red Pixel Intensity")
    #ax1.legend(loc='upper right')

    # Ajustar el tamaño de las fuentes en el gráfico
    xticks_values = [min(X), max(X)]
    formatted_xticks = ["{:.2f}".format(value) for value in xticks_values]
    
    ax1.set_xticks(xticks_values, formatted_xticks, fontsize = 10)
    
    # Gráfico de densidad en el segundo subplot (rotado en 90 grados)
    sns.kdeplot(Y, ax=ax2, color='green', vertical=True)
    ax2.set_xlabel("Densidad")
    ax2.set_ylim(0,260)
    ax2.set_xlim(0, 0.05)
    ax2.set_yticks([])

    # Ajustar el tamaño de las fuentes en el gráfico
    xticks_values = [0, 0.05]
    formatted_xticks = ["{:.2f}".format(value) for value in xticks_values]
    
    ax2.set_xticks(xticks_values, formatted_xticks, fontsize = 10)




    # Ajustar la distancia entre los subgráficos
    plt.subplots_adjust(wspace=0)

def scatter_with_errorbars_MeanStdDev(compu_data, list_of_list_of_Obs, carpetaSup, show_error_bars=True, xlabel = "datos x", ylabel = "datos y", title = "title" , font_size=16):

    def calcular_desviacion_estandar(lista, promedio):
            diferencias = np.array(lista) - promedio
            diferencias_cuadrado = diferencias ** 2
            varianza = np.mean(diferencias_cuadrado)
            desviacion_estandar = np.sqrt(varianza)
            return desviacion_estandar
    
    # Calcular la media y desviación estándar de cada lista en list_of_list_of_Obs

    proms = [np.mean(data) for data in list_of_list_of_Obs]
    std_dev_down = []
    std_devs_up = []

    for lista, promedio in zip(list_of_list_of_Obs, proms):
        lista_up = [i for i in lista if i >= promedio]
        lista_down = [i for i in lista if i <= promedio]
        desviacion_abajo = calcular_desviacion_estandar(lista_down, promedio)
        std_dev_down.append(desviacion_abajo)
        desviacion_arriba = calcular_desviacion_estandar(lista_up, promedio)
        std_devs_up.append(desviacion_arriba)

    ## GRAFICANDO 
    ### Agregando Cajas
    scatter_and_boxplot_with_density_Y(list(compu_data), list(proms), 20)

    ## Guardando los graficos
    NombreCarpeta = carpetaSup+"/"+str(xlabel) + "max"
    CrearCarpeta(NombreCarpeta)

    plt.tight_layout()
    #plt.savefig(NombreCarpeta+"/Boxscatter_"+str(xlabel)+"_"+str(title)+"max.png")

    plt.show()
def apply_threshold(lista_de_listas, N):
    # Recorremos todas las listas en la lista de listas
    for lista in lista_de_listas:
        # Utilizamos una comprensión de lista para filtrar los números mayores o iguales a N
        lista[:] = [x for x in lista if x >= N]

        # Si la lista quedó vacía después de eliminar los elementos menores a N, agregamos un 0
        if not lista:
            lista.append(0)

    return lista_de_listas

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

## Columnas de datos Computacionales
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
thresholds = [0, 60, 80, 100,130, 150, 200]

###########################################
nombres = ["CC"]
############################################

for name_column in nombres:
    data_computational = datos_comp[name_column]
    """
    ## Parametros que deseo guardar.
    horas = []
    promedio_ocupacion_total = []

    r2_values_mean = []
    r2_values_median = []
    r2_values_max = []

    Pendientes_mean = []
    Pendientes_median = []
    Pendientes_max = []

    Interseptos_mean = []
    Interseptos_median = []
    Interseptos_max = []

    pvalue_mean = []
    pvalue_median = []
    pvalue_max = []

    stddev_mean = []
    stddev_median = []
    stddev_max = []
    """

    hora_inicial, hora_final = 0, 24
    ## Creando Carpeta
    Nombre_carpetaSuperior = "Box/"+name_column
    CrearCarpeta(Nombre_carpetaSuperior)
    for hora_in in range(hora_inicial, hora_final):
        for minuto_in in range(0, 60, 15):
            columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
            datos_new = datos_obs[columnas_elejidas].values.tolist()
            
            ## Eliminando los datos que están debajo del threshold
            datos_comp_sin_cero = []
            datos_obs_sin_cero = []
            for i, lista in enumerate(datos_new):
                if len(datos_new[i]) == 1 and datos_new[i] == [0]:
                    continue
                else:
                    datos_comp_sin_cero.append(data_computational[i])
                    datos_obs_sin_cero.append(datos_new[i])
            
            fit_mean = scatter_with_errorbars_MeanStdDev(datos_comp_sin_cero, datos_obs_sin_cero, ylabel= "Red Pixel Intensity", xlabel=name_column, title="hour = "+str(hora_in)+":"+str(minuto_in), show_error_bars=True, carpetaSup = Nombre_carpetaSuperior)
    """

            ## Guardando los datos que necesito
            horas.append(f"{hora_in}:{minuto_in}")
            
            # El promedio lo usamos con todos los datos(sin threshold)
            datos_mean = [np.mean(lista) for lista in datos]
            promedio_ocupacion_total.append(np.mean(datos_mean))
            
            # slopes
            Pendientes_mean.append(fit_mean[0])
            Pendientes_median.append(fit_Median[0])
            Pendientes_max.append(fit_Max[0])

            # interceptos
            Interseptos_mean.append(fit_mean[1])
            Interseptos_median.append(fit_Median[1])
            Interseptos_max.append(fit_Max[1])

            # rsquare
            r2_values_mean.append(fit_mean[2])
            r2_values_median.append(fit_Median[2])
            r2_values_max.append(fit_Max[2])

            # pvalue
            pvalue_mean.append(fit_mean[3])
            pvalue_median.append(fit_Median[3])
            pvalue_max.append(fit_Max[3])

            # std
            stddev_mean.append(fit_mean[4])
            stddev_median.append(fit_Median[4])
            stddev_max.append(fit_Max[4])

    df = pd.DataFrame()
    df["horas"] = horas
    df["mean_total_ocupation"] = promedio_ocupacion_total

    df["Pendientes_mean"] = Pendientes_mean
    df["Pendientes_median"] = Pendientes_median
    df["Pendientes_max"] = Pendientes_max

    df["Intercepto_mean"] = Interseptos_mean
    df["Intercepto_median"] = Interseptos_median
    df["Intercepto_max"] = Interseptos_max

    df["R2_mean"]=r2_values_mean
    df["R2_median"]=r2_values_median
    df["R2_max"]=r2_values_max

    df["P_mean"]=pvalue_mean
    df["P_median"]=pvalue_median
    df["P_max"]=pvalue_max

    df["stdDev_mean"]=stddev_mean
    df["stdDev_median"]=stddev_median
    df["stdDev_max"]=stddev_max

    df.to_csv(Nombre_carpetaSuperior+"/datos_"+str(name_column)+"_treshold_"+str(threshold)+"complex.dat")
    print("listo")
    """