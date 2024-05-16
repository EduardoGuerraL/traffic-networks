import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scienceplots
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
from functions.basics import reescalar_lista_de_listas, crearNintervalosOrdenados, obtener_nombres_con_H_M_sinFDS
from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales
import math

def calculate_median_positions(X: list, Y: list, box_count: int):
    # Dividir X e Y en box_count intervalos
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, box_count)
    
    # Gráfico de diagrama de caja en el primer subplot
    y_median_box = []
    x_median_box = []
    for i in range(box_count):
        if intervalos_X[i]:
            ancho = (intervalos_X[i][-1] - intervalos_X[i][0])
            positions = [intervalos_X[i][-1] - (ancho / 2)]
                    
            # Guardando datos[punto medio de x boxes, mean de Y, median de Y]
            x_median_box.append(positions[0])
    
    y_median_box = [np.median(subconjunto) for subconjunto in intervalos_Y]
    return y_median_box, x_median_box

def calculate_slopes_for_fit_medians_and_Per95(datos_obs, datos_comp, n_boxes):
    Slopes = []
    Per95 = []

    hora_inicial, hora_final = 0, 24
    for hora_in in range(hora_inicial, hora_final):
        for minuto_in in range(0, 60, 15):

            columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
            data_observacional = datos_obs[columnas_elejidas].values.tolist()
            
            ## Reescalando los data_observacional de 0 a 1
            data_observacional = reescalar_lista_de_listas(data_observacional, 255)  
         

            # Obtener el promedio de cada nodo sobre los dias en el instante de tiempo
            promedios = [np.mean(data) for data in data_observacional]
            # Percentil 90
            percentil_95 = np.percentile(promedios, 95)
            y_medians, x_medians = calculate_median_positions(datos_comp, promedios, n_boxes)
            ## REGRESION LINEAL
            #(slope, intercept, r_value, p_value, std_err)
            medians_params = scipy.stats.linregress(x_medians, y_medians)
            Slopes.append(medians_params[0])
            Per95.append(percentil_95)
    
    return Slopes, Per95

def find_values_matrix(data):
    X = list(data[0])
    Y = list(data[1])
    Z = list(data[2])
    
    # Encontrar el valor máximo de X y su correspondiente Y
    X_max = max(X)
    indice_X_max = X.index(X_max)
    Y_X_max = Y[indice_X_max]
    Z_X_max = Z[indice_X_max]

    # Encontrar el valor máximo de Y y su correspondiente X
    Y_max = max(Y)
    indice_Y_max = Y.index(Y_max)
    X_Y_max = X[indice_Y_max]
    Z_Y_max = Z[indice_Y_max]

    return X_Y_max,Y_max, Z_Y_max

##########################################################################################################################
#Conjunto de archivos
N1207 = [Datos_computacionales[1], Datos_observacionales[0]]
N505 = [Datos_computacionales[0], Datos_observacionales[2]]
datos_comp_N505 = pd.read_csv(N505[0])
datos_obs_N505 = pd.read_csv(N505[1])
datos_comp_N1207 = pd.read_csv(N1207[0])
datos_obs_N1207 = pd.read_csv(N1207[1])
data_observacional = [datos_obs_N505,datos_obs_N1207]
data_computacional  = [datos_comp_N505, datos_comp_N1207]

############################################
#model          Topology data,         datos de Google,       Topology Index  max R-Square  Treshold
ModelGN505 =   [data_computacional[0], data_observacional[0] ,'CC'           ,0.82          ,0.33]
ModelGN1207 =  [data_computacional[1], data_observacional[1] ,'CC'           ,0.87          ,0.33]
ModelDGN505 =  [data_computacional[0], data_observacional[0] ,'DiCC'         ,0.87          ,0.37]
ModelDGN1207 = [data_computacional[1], data_observacional[1] ,'DiCC'         ,0.92          ,0.33]


#All Models
Modelos = [ModelGN505, ModelGN1207, ModelDGN505, ModelDGN1207]
model_number = 2

data_computational = Modelos[model_number][0][Modelos[model_number][2]]
data_observational = Modelos[model_number][1]
threshold = Modelos[model_number][4]

# Definir los nombres de las columnas
nombres = ["DiBC","BC","DiCC", "CC", "DiDC", "DC"]
nombres = ['CC', 'DiCC']
# Diccionarios para almacenar los datos de cada nombre
lista_datos_por_nombre = []
for datos_obs, datos_comp in zip(data_observacional, data_computacional):
    # Bucle para recorrer cada nombre
    
    #Donde guardaremos todos los datos de la forma: [[slopes],[r2],[alpha]]
    for name_column in nombres:
                
        data_computational = datos_comp[name_column]
        data_computational = [(i-min(data_computational))/(max(data_computational)-min(data_computational)) for i in data_computational]
        
        if name_column in ["DiDC", "DC"]:
            n = 3
        if name_column in ["DiBC", "BC"]:
            n = 15
        if name_column in ["DiCC", "CC"]:
            n = 20

        Slopes, Per95 =  calculate_slopes_for_fit_medians_and_Per95(datos_obs= datos_obs, datos_comp= data_computational, n_boxes= n)

        # Definir los umbrales
        umbrales = np.linspace(min(Per95), max(Per95)- 0.2*max(Per95), 200)  # Cambia el número 50 para tener más o menos umbrales
        #Donde guardaremos los datos
        Todos_los_datos = []
        r2_list = []
        slopes_list = []
        Trh = []
        for threshold in umbrales:
            threshold = math.trunc(threshold * 1000) / 1000

            # Dividir los puntos por encima y por debajo del threshold
            datos_filtrados = [(x, y) for x, y in zip(Slopes, Per95) if y >= threshold]
            X_filtrado, Y_filtrado = zip(*datos_filtrados)
        
            
            ## REGRESION LINEAL
            #(slope, intercept, r_value, p_value, std_err)
            medians_params = scipy.stats.linregress(X_filtrado, Y_filtrado)
            
            r2_list.append(math.trunc((medians_params[2]**2) * 1000) / 1000)
            slopes_list.append(math.trunc((medians_params[0]) * 1000) / 1000)
            Trh.append(threshold)

        Todos_los_datos.append(slopes_list)
        Todos_los_datos.append(r2_list)
        Todos_los_datos.append(Trh)
        print(name_column, find_values_matrix(Todos_los_datos))
    
    #for i in range(len(Todos_los_datos[0])-1):
     #   print(Todos_los_datos[0][i],Todos_los_datos[1][i],Todos_los_datos[2][i])