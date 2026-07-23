import pandas as pd
import matplotlib.pyplot as plt
import scipy
from functions.basics import *

def scatter_with_errorbars_MeanStdDev(compu_data, list_of_list_of_Obs, carpetaSup, xlabel = "datos x"):

    def calcular_desviacion_estandar(lista, promedio):
            diferencias = np.array(lista) - promedio
            diferencias_cuadrado = diferencias ** 2
            varianza = np.mean(diferencias_cuadrado)
            desviacion_estandar = np.sqrt(varianza)
            return desviacion_estandar
    
    # Calcular la media y desviación estándar de cada lista en list_of_list_of_Obs

    means = [np.mean(data) for data in list_of_list_of_Obs]
    std_dev_down = []
    std_devs_up = []

    for lista, promedio in zip(list_of_list_of_Obs, means):
        lista_up = [i for i in lista if i >= promedio]
        lista_down = [i for i in lista if i <= promedio]
        desviacion_abajo = calcular_desviacion_estandar(lista_down, promedio)
        std_dev_down.append(desviacion_abajo)
        desviacion_arriba = calcular_desviacion_estandar(lista_up, promedio)
        std_devs_up.append(desviacion_arriba)

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(compu_data, means)
    
    ## Guardando los graficos
    NombreCarpeta = carpetaSup+"/"+str(xlabel) + "MeanStD"
    CrearCarpeta(NombreCarpeta)
    
    return slope, intercept, r_value, p_value, std_err

def scatter_with_errorbars_Median90Percent(compu_data, list_of_list_of_Obs,carpetaSup, xlabel = "datos x"):

    medianas = [np.median(lista) for lista in list_of_list_of_Obs]
    iqr_lower = [np.percentile(lista, 5) for lista in list_of_list_of_Obs]
    iqr_lower = [abs(media - iqr) for media, iqr in zip(medianas, iqr_lower)]
    iqr_upper = [np.percentile(lista, 95) for lista in list_of_list_of_Obs]
    iqr_upper = [abs(media - iqr) for media, iqr in zip(medianas, iqr_upper)]

    ## Parametros de la regresión
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(compu_data, medianas)
 
    # Graficar la regresión lineal
    NombreCarpeta = carpetaSup+"/"+str(xlabel) + "MedianPer90"
    CrearCarpeta(NombreCarpeta)

    return slope, intercept, r_value, p_value, std_err

def scatter_with_errorbars_Max(compu_data, list_of_list_of_Obs,carpetaSup, xlabel = "datos x"):

    ## Obtener maximos de cada calle observacional
    maximos = [np.max(lista) for lista in list_of_list_of_Obs]

    ## Parametros de la regresión
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(compu_data, maximos)
    
    # Graficar la regresión lineal
    NombreCarpeta =carpetaSup+"/"+ str(xlabel) + "Max"
    CrearCarpeta(NombreCarpeta)

    return slope, intercept, r_value, p_value, std_err

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
thresholds = [10, 30, 50, 70, 90, 110, 120, 140, 160, 170]
for threshold in thresholds:
    for name_column in nombres:
        
        data_computational = datos_comp[name_column]

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

        hora_inicial, hora_final = 0, 24
        ## Creando Carpeta
        Nombre_carpetaSuperior = "Threshold"+str(threshold)+"/"+name_column
        CrearCarpeta(Nombre_carpetaSuperior)
        
        for hora_in in range(hora_inicial, hora_final):
            for minuto_in in range(0, 60, 15):
                columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
                datos = datos_obs[columnas_elejidas].values.tolist()
                datos_new = apply_threshold(datos, threshold)
                
                ## Eliminando los datos que están debajo del threshold
                datos_comp_sin_cero = []
                datos_obs_sin_cero = []
                for i, list in enumerate(datos_new):
                    if len(datos_new[i]) == 1 and datos_new[i] == [0]:
                        continue
                    else:
                        datos_comp_sin_cero.append(data_computational[i])
                        datos_obs_sin_cero.append(datos_new[i])
                
                fit_mean = scatter_with_errorbars_MeanStdDev(datos_comp_sin_cero, datos_obs_sin_cero, xlabel=name_column, carpetaSup = Nombre_carpetaSuperior)
                fit_Median = scatter_with_errorbars_Median90Percent(datos_comp_sin_cero, datos_obs_sin_cero, xlabel=name_column, carpetaSup = Nombre_carpetaSuperior)
                fit_Max = scatter_with_errorbars_Max(datos_comp_sin_cero, datos_obs_sin_cero, xlabel=name_column, carpetaSup = Nombre_carpetaSuperior)

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

        print(df)
        df.to_csv(Nombre_carpetaSuperior+"/datos_"+str(name_column)+"_treshold_"+str(threshold)+"complex.dat")
        print("listo")