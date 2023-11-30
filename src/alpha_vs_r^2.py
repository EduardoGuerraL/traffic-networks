import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import scipy
import scienceplots
import seaborn as sns
from sklearn.linear_model import LinearRegression
from statistics import mode
from sklearn.metrics import r2_score
from scipy import stats
from scipy.stats import scoreatpercentile
from functions.basics import *

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
datos_comp1 = pd.read_csv("data/DataNetwork/StreetAsNode/all_data_SimpleNet_new.csv")
datos_comp2 = pd.read_csv("data/DataNetwork/StreetAsNode/all_data_ComplexNet_new.csv")
## Datos observacional

#"data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv"
#"data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_max.csv"
#"data/DataImages/In_Streets_Coord/Normal/streetsCoordsR1S4.csv"
#"data/DataImages/In_Streets_Coord/Normal/MaxStreetscoordsR0S6.csv"
#"data/DataImages/In_Streets_Coord/Normal/MeanStreetscoordsR0S6.csv"
datos_obs1 = pd.read_csv("data/DataImages/In_Streets_Coord/Normal/streetsCoordsR1S4.csv")
datos_obs2 = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")

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

# Definir los umbrales
umbrales = np.linspace(0, 0.5, 50)  # Cambia el número 50 para tener más o menos umbrales

# Definir los nombres de las columnas
nombres = ["CC", "DiCC"]

# Listas de datos adicionales
datos_adicionales = [
    (datos_comp1, datos_obs1),
    (datos_comp2, datos_obs2)
]

# Diccionarios para almacenar los datos de cada nombre
R2 = []
for datos_comp, datos_obs in datos_adicionales:
    datos_por_nombre = {nombre: {"Slopes": [], "SuperAlgo": []} for nombre in nombres}
    # Bucle para recorrer cada nombre
    for name_column in nombres:
        Slopes = []
        SuperAlgo = []
        
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
                algo  = percentil_90
                SuperAlgo.append(algo)

        for threshold in umbrales:
            # Dividir los puntos por encima y por debajo del threshold
            datos_filtrados = [(x, y) for x, y in zip(Slopes, SuperAlgo) if y > threshold]
            X_filtrado, Y_filtrado = zip(*datos_filtrados)

            # Convertir a arrays de numpy para usarlos en la regresión lineal
            X_filtrado = np.array(X_filtrado).reshape(-1, 1)
            Y_filtrado = np.array(Y_filtrado)

            # Guardar los datos filtrados en la lista correspondiente al nombre actual
            datos_por_nombre[name_column]["Slopes"].append(X_filtrado)
            datos_por_nombre[name_column]["SuperAlgo"].append(Y_filtrado)
    R2.append(datos_por_nombre)

# Crear el gráfico combinado para ambos nombres
plt.figure(figsize=(8, 6))
plt.style.use(["science", "notebook", "grid"])


# Lista para almacenar los valores de R^2
r2_valores = []

for i in range(2):
    datos_por_nombre = R2[i]
    for nombre, datos in datos_por_nombre.items():
        r2_valores_nombre = []

        for i in range(len(umbrales)):
            # Realizar la regresión lineal con los datos filtrados
            modelo = LinearRegression().fit(
                np.array(datos["Slopes"][i]).reshape(-1, 1),
                np.array(datos["SuperAlgo"][i])
            )

            # Calcular el coeficiente de determinación (R^2)
            y_pred = modelo.predict(np.array(datos["Slopes"][i]).reshape(-1, 1))
            r2 = r2_score(np.array(datos["SuperAlgo"][i]), y_pred)
            r2_valores_nombre.append(r2)

        # Guardar los valores de R^2 para cada nombre
        r2_valores.append(r2_valores_nombre)

# Graficar los valores de R^2 en función de los umbrales para cada nombre
nombres = ["CC 505","DiCC 505", "CC 1207", "DiCC 1207"]
for i in range(4):
    plt.plot(umbrales, r2_valores[i], marker='o', label = nombres[i])

plt.xlabel(r'$\alpha$', fontsize = 30)
plt.ylabel('$R^2$', fontsize = 30)
plt.legend()
plt.grid(True)
plt.show()