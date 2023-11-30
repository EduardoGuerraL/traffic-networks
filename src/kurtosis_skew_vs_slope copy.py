import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Packages.Funciones.functions import obtener_nombres_con_H_M_sinFDS
import os
import scipy
import scienceplots
import seaborn as sns
from sklearn.linear_model import LinearRegression
from statistics import mode
from sklearn.metrics import r2_score
from scipy import stats
from scipy.stats import scoreatpercentile

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
    for i in range(N):
        if intervalos_X[i]:
            ancho = (intervalos_X[i][-1] - intervalos_X[i][0])
            positions = [intervalos_X[i][-1] - (ancho / 2)]
            
            promedio = np.mean(intervalos_Y[i])
            
            # Guardando datos[punto medio de x boxes, mean de Y, median de Y]
            Posiciones_X.append(positions[0])
            Promedios.append(promedio)
    
    Medianas = [np.median(subconjunto) for subconjunto in intervalos_Y]
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
    
    #viendo distribucion
    # Mediana
    mediana = np.median(promedios)

    # Percentil 90
    percentil_90 = np.percentile(promedios, 95)

    # Máximo
    maximo = np.max(promedios)

    # Tercer cuartil (percentil 75)
    cuartil_3 = np.percentile(promedios, 5)

    prom = np.mean(promedios)

    moda = mode(promedios)
    print(moda)

    # Ordenar los datos
    datos_ordenados = np.sort(promedios)

    # Calcular los percentiles necesarios
    Q1 = scoreatpercentile(datos_ordenados, 25)
    Q3 = scoreatpercentile(datos_ordenados, 75)
    D1 = scoreatpercentile(datos_ordenados, 10)
    D9 = scoreatpercentile(datos_ordenados, 90)

    # Calcular el rango intercuartílico (IQR)
    IQR = Q3 - Q1

    # Calcular el coeficiente de asimetría de Bowley-Yule
    coef_bowley_yule = ((D9 - D1) * 12) / (IQR * 10)

    ## GRAFICANDO 
    ### Agregando Cajas
    medians_box, means_box, pos_box = scatter_and_boxplot(list(compu_data), list(promedios), 20)
    
    ## REGRESION LINEAL
    #(slope, intercept, r_value, p_value, std_err)
    medians_params = scipy.stats.linregress(pos_box, medians_box)
    means_params = scipy.stats.linregress(pos_box, means_box)
    
    return medians_params, means_params, kurtosis, skewness, mediana, percentil_90, maximo, cuartil_3, prom, moda, coef_bowley_yule

##########################################################################################################################
## Datos Computacionales

#"data/DataNetwork/StreetAsNode/all_data_SimpleNet_new.csv"
#"data/DataNetwork/StreetAsNode/all_data_ComplexNet_new.csv"
datos_comp = pd.read_csv("data/DataNetwork/StreetAsNode/all_data_SimpleNet_new.csv")
## Datos observacional

#"data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv"
#"data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_max.csv"
#"data/DataImages/In_Streets_Coord/Normal/streetsCoordsR1S4.csv"
#"data/DataImages/In_Streets_Coord/Normal/MaxStreetscoordsR0S6.csv"
#"data/DataImages/In_Streets_Coord/Normal/MeanStreetscoordsR0S6.csv"
datos_obs = pd.read_csv("data/DataImages/In_Streets_Coord/Normal/streetsCoordsR1S4.csv")

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
SuperAlgo = []
for name_column in nombres:
    
    data_computational = datos_comp[name_column]
    data_computational = [(i-min(data_computational))/(max(data_computational)-min(data_computational)) for i in data_computational]
    
    ## Creando Carpeta
    Nombre_carpetaSuperior = "DataBox/"+name_column
    CrearCarpeta(Nombre_carpetaSuperior)
    
    hora_inicial, hora_final = 0, 24
    for hora_in in range(hora_inicial, hora_final):
        for minuto_in in range(0, 60, 15):

            columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
            data_observacional = datos_obs[columnas_elejidas].values.tolist()
            
            ## Reescalando los data_observacional de 0 a 1
            data_observacional = reescalar_lista_de_listas(data_observacional, 255)                
            
            fit_params_medians,fit_params_means, kurtosis, skewness, mediana, percentil_90, maximo, cuartil_3, prom, moda, coef  = scatter4MeanObsValues(data_computational, data_observacional, carpetaSup = Nombre_carpetaSuperior, xlabel = name_column)
            
            Slopes.append(fit_params_medians[0])
            Kurtosis.append(kurtosis)
            Skewness.append(skewness)
            algo  = percentil_90
            SuperAlgo.append(algo)

    plt.style.use(["science", "notebook", "grid"])


    # threshold M
    threshold = 0.35
    plt.tick_params(axis='both', labelsize=18)  # Tamaño de fuente para los números de los ejes

    # Dividir los puntos por encima y por debajo del threshold
    datos_filtrados = [(x, y) for x, y in zip(Slopes, SuperAlgo) if y > threshold]
    X_filtrado, Y_filtrado = zip(*datos_filtrados)

    # Convertir a arrays de numpy para usarlos en la regresión lineal
    X_filtrado = np.array(X_filtrado).reshape(-1, 1)
    Y_filtrado = np.array(Y_filtrado)

    # Realizar la regresión lineal con los datos filtrados
    modelo = LinearRegression().fit(X_filtrado, Y_filtrado)

    # Obtener la pendiente y la intersección
    pendiente = modelo.coef_[0]
    interseccion = modelo.intercept_

    # Dibujar el fondo dividido por el threshold
    plt.axhspan(-1, threshold, facecolor='skyblue', alpha=0.6)  # Área por debajo del threshold
    plt.axhspan(threshold, 2, facecolor='firebrick', alpha=0.8)   # Área por encima del threshold
    # Crear el plot con colores diferentes para por encima y por debajo del threshold
    plt.scatter(Slopes, SuperAlgo, edgecolors='black', facecolors='white', label='Datos filtrados')

    X_plot = np.linspace(min(X_filtrado), max(X_filtrado), 100)
    plt.plot(X_plot, modelo.predict(X_plot), color='k', label='Regresión lineal', linestyle = "--")
    #plt.axhline(threshold, linestyle='--', color='gray')

    # Límites de los ejes X e Y con un pequeño margen alrededor de los datos
    x_min, x_max = min(Slopes), max(Slopes)
    y_min, y_max = min(SuperAlgo), max(SuperAlgo)

    x_range = x_max - x_min
    y_range = y_max - y_min

    # Agregar un pequeño margen alrededor de los datos
    plt.xlim(x_min - 0.1 * x_range, x_max + 0.1 * x_range)
    plt.ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)

    # Calcular el coeficiente de determinación (R^2)
    y_pred = modelo.predict(X_filtrado)
    r2 = r2_score(Y_filtrado, y_pred)

    # Calcular la desviación estándar
    residuals = Y_filtrado - y_pred
    std_dev = np.std(residuals)

    # Resto del código de trazado...
    # Añadir texto con R^2 y desviación estándar al gráfico
    plt.text(0.2, 0.9, f'$R^2$= {r2:.3f}\n$\sigma$= {std_dev:.2e}', 
        horizontalalignment='center', verticalalignment='center', 
        transform=plt.gca().transAxes, fontsize=16)

    plt.text(0.8, threshold, r'$\alpha$= {:.3f}'.format(threshold), 
        horizontalalignment='center', verticalalignment='center', 
        transform=plt.gca().transAxes, fontsize=16)
    
    plt.show()