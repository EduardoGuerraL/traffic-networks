import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from functions.basics import *
import os
import scipy

def CrearCarpeta(nombre_carpeta):
    # Ruta completa donde deseas crear la carpeta
    ruta_completa = os.path.join(os.getcwd(), nombre_carpeta)

    # Verifica si la carpeta no existe antes de crearla
    if not os.path.exists(ruta_completa):
        os.makedirs(ruta_completa)
        print(f"Se ha creado la carpeta '{nombre_carpeta}' en '{ruta_completa}'")
    else:
        pass

def scatter_with_errorbars_MeanStdDev(compu_data, list_of_list_of_Obs, carpetaSup, show_error_bars=True, xlabel = "datos x", ylabel = "datos y", title = "title" , font_size=16):

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

    ## Parametros de la regresión
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(compu_data, means)

    ## GRAFICANDO 

    # Realizar la regresión lineal
    regression_coeffs = np.polyfit(compu_data, means, 1)  # Fit a first-degree polynomial (line) to the data
    regression_line = np.polyval(regression_coeffs, compu_data)  # Generate y-values for the regression line
    
    # Crear el gráfico de dispersión
    plt.figure(figsize=(8, 6))

    if show_error_bars:
        plt.errorbar(compu_data, means, yerr=[std_dev_down, std_devs_up], fmt='o', mec='black', mfc='white', ecolor='black', capsize=0,elinewidth= 0.3)
    elif not show_error_bars:
        plt.scatter(compu_data, means, marker='o',c='white',edgecolors='black',label = "mean")

    plt.plot(compu_data, regression_line, color='red', label='linear fit')
    plt.ylim(0, 260)

    # Personalizar el gráfico
    plt.xlabel(str(xlabel), fontsize=font_size)
    plt.ylabel(str(ylabel), fontsize=font_size)
    plt.title(str(title), fontsize=font_size)
    plt.legend(fontsize=font_size)
    plt.grid(False)

    # Ajustar el tamaño de las fuentes en el gráfico
    xticks_values = [min(compu_data), max(compu_data)]
    formatted_xticks = ["{:.2f}".format(value) for value in xticks_values]

    plt.xticks(xticks_values,formatted_xticks,fontsize=font_size-5)
    
    plt.yticks(fontsize=font_size-5)

    # Cambiar el estilo de las líneas principales
    plt.rc('axes', linewidth=2)
    plt.tick_params(axis='both', which='major', length=0, width=0)

    ## Guardando los graficos
    NombreCarpeta = carpetaSup+"/"+str(xlabel) + "MeanStD"
    CrearCarpeta(NombreCarpeta)

    plt.tight_layout()
    plt.savefig(NombreCarpeta+"/scatter_"+str(xlabel)+"_"+str(title)+"mean.png")
    #plt.show()

    return slope, intercept, r_value, p_value, std_err

def scatter_with_errorbars_Median90Percent(compu_data, list_of_list_of_Obs, carpetaSup, show_error_bars=True, xlabel = "datos x", ylabel = "datos y", title = "title" , font_size=16 ):

    medianas = [np.median(lista) for lista in list_of_list_of_Obs]
    iqr_lower = [np.percentile(lista, 5) for lista in list_of_list_of_Obs]
    iqr_lower = [abs(media - iqr) for media, iqr in zip(medianas, iqr_lower)]
    iqr_upper = [np.percentile(lista, 95) for lista in list_of_list_of_Obs]
    iqr_upper = [abs(media - iqr) for media, iqr in zip(medianas, iqr_upper)]

    # Realizar la regresión lineal
    regression_coeffs = np.polyfit(compu_data, medianas, 1)  # Fit a first-degree polynomial (line) to the data
    regression_line = np.polyval(regression_coeffs, compu_data)  # Generate y-values for the regression line

    ## Parametros de la regresión
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(compu_data, medianas)

    # Crear el gráfico de dispersión
    plt.figure(figsize=(8, 6))

    if show_error_bars:
        plt.errorbar(compu_data, medianas, yerr=[iqr_lower, iqr_upper], fmt='o', mec='black', mfc='white', ecolor='black', capsize=0,elinewidth= 0.3)
    elif not show_error_bars:
        plt.scatter(compu_data, medianas, marker='o',c='white',edgecolors='black',label = "mean")

    plt.plot(compu_data, regression_line, color='red', label='linear fit')
    plt.ylim(0, 260)

    # Personalizar el gráfico
    plt.xlabel(str(xlabel), fontsize=font_size)
    plt.ylabel(str(ylabel), fontsize=font_size)
    plt.title(str(title), fontsize=font_size)
    plt.legend(fontsize=font_size)
    plt.grid(False)

    # Ajustar el tamaño de las fuentes en el gráfico
    xticks_values = [min(compu_data), max(compu_data)]
    formatted_xticks = ["{:.2f}".format(value) for value in xticks_values]

    plt.xticks(xticks_values,formatted_xticks,fontsize=font_size-5)
    
    plt.yticks(fontsize=font_size-5)

    # Cambiar el estilo de las líneas principales
    plt.rc('axes', linewidth=2)
    plt.tick_params(axis='both', which='major', length=0, width=0)

    # Graficar la regresión lineal
    NombreCarpeta = carpetaSup+"/"+str(xlabel) + "MedianPer90"
    CrearCarpeta(NombreCarpeta)

    # Mostrar el gráfico
    plt.tight_layout()
    plt.savefig(NombreCarpeta+"/scatter_"+str(xlabel)+"_"+str(title)+"median.png")
    #plt.show()

    return slope, intercept, r_value, p_value, std_err

def scatter_with_errorbars_Max(compu_data, list_of_list_of_Obs,carpetaSup, show_error_bars=True, xlabel = "datos x", ylabel = "datos y", title = "title" , font_size=16 ):

    ## Obtener maximos de cada calle observacional
    maximos = [np.max(lista) for lista in list_of_list_of_Obs]

    ## Realizar la regresión lineal
    regression_coeffs = np.polyfit(compu_data, maximos, 1)  # Fit a first-degree polynomial (line) to the data
    regression_line = np.polyval(regression_coeffs, compu_data)  # Generate y-values for the regression line
    ## Parametros de la regresión
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(compu_data, maximos)
    
    ## Graficando
    yerr = np.zeros(len(list_of_list_of_Obs))
    # Crear el gráfico de dispersión
    plt.figure(figsize=(8, 6))

    if show_error_bars:
        plt.errorbar(compu_data, maximos, yerr=[yerr, yerr], fmt='o', mec='black', mfc='white', ecolor='black', capsize=0,elinewidth= 0.3)
 
    plt.plot(compu_data, regression_line, color='red', label='linear fit')
    plt.ylim(0, 260)

    # Personalizar el gráfico
    plt.xlabel(str(xlabel), fontsize=font_size)
    plt.ylabel(str(ylabel), fontsize=font_size)
    plt.title(str(title), fontsize=font_size)
    plt.legend(fontsize=font_size)
    plt.grid(False)

    # Ajustar el tamaño de las fuentes en el gráfico
    xticks_values = [min(compu_data), max(compu_data)]
    formatted_xticks = ["{:.2f}".format(value) for value in xticks_values]

    plt.xticks(xticks_values,formatted_xticks,fontsize=font_size-5)
    
    plt.yticks(fontsize=font_size-5)

    # Cambiar el estilo de las líneas principales
    plt.rc('axes', linewidth=2)
    plt.tick_params(axis='both', which='major', length=0, width=0)
   
    #Graficar la regresión lineal
    NombreCarpeta =carpetaSup+"/"+ str(xlabel) + "Max"
    CrearCarpeta(NombreCarpeta)
    
    # Mostrar el gráfico
    plt.tight_layout()
    plt.savefig(NombreCarpeta+"/scatter_"+str(xlabel)+"_"+str(title)+"max.png")
    #plt.show()


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
thresholds = [0, 60, 80, 100,130, 150, 200]

###########################################
nombres = ["CC"]
thresholds = [0]
############################################

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
                
                fit_mean = scatter_with_errorbars_MeanStdDev(datos_comp_sin_cero, datos_obs_sin_cero, ylabel= "Red Pixel Intensity", xlabel=name_column, title="hour = "+str(hora_in)+":"+str(minuto_in), show_error_bars=True, carpetaSup = Nombre_carpetaSuperior)
                fit_Median = scatter_with_errorbars_Median90Percent(datos_comp_sin_cero, datos_obs_sin_cero, ylabel= "Red Pixel Intensity", xlabel=name_column, title="hour = "+str(hora_in)+":"+str(minuto_in), show_error_bars=True, carpetaSup = Nombre_carpetaSuperior)
                fit_Max = scatter_with_errorbars_Max(datos_comp_sin_cero, datos_obs_sin_cero, ylabel= "Red Pixel Intensity", xlabel=name_column, title="hour = "+str(hora_in)+":"+str(minuto_in), show_error_bars=True, carpetaSup = Nombre_carpetaSuperior)

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