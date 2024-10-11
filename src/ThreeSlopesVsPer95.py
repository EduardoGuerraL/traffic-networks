'''

'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scienceplots
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from functions.basics import reescalar_lista_de_listas, obtener_nombres_con_H_M_sinFDS, crearNintervalosOrdenados
from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales

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

def calculate_slopes_for_fit_medians_and_Per95(datos_obs, datos_comp, box_count):
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
            #percentil_95 = max(promedios)
            y_medians, x_medians = calculate_median_positions(datos_comp, promedios, box_count)
            ## REGRESION LINEAL
            #(slope, intercept, r_value, p_value, std_err)
            medians_params = scipy.stats.linregress(x_medians, y_medians)
            
            Slopes.append(medians_params[0])
            Per95.append(percentil_95)
    
    return Slopes, Per95


##########################################################################################################################
#Conjunto de archivos
N505 = [Datos_computacionales[0], Datos_observacionales[2]]
N1207 = [Datos_computacionales[1], Datos_observacionales[0]]
datos_comp_N505 = pd.read_csv(N505[0])
datos_obs_N505 = pd.read_csv(N505[1])
datos_comp_N1207 = pd.read_csv(N1207[0])
datos_obs_N1207 = pd.read_csv(N1207[1])
data_observacional = [datos_obs_N505,datos_obs_N1207]
data_computacional  = [datos_comp_N505, datos_comp_N1207]

datos_comp = data_computacional[1]
datos_obs = data_observacional[1]

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
            "mean_state_RWM_lim"
        ]

###########################################
############################################

## Graficando

#borrar opciones luego de que elijamos
"""
Opcion 1
"""
plt.rcParams.update({
    "text.usetex": True,
})
plt.style.use(["science", "notebook", "grid"])
#threshold = [0.25,0.329,0.319] #DGN505
#threshold = [0.423,0.368,0.305] #DGN1207
#threshold = [0.25,0.332,0.319] #GN505
threshold = [0.38,0.328,0.305] #GN1027


markers = ['o','s','^' ]
box_count = [15,20,3]
colores = ['green', 'blue', 'red']
plt.tick_params(axis='both', labelsize=18)  # Tamaño de fuente para los números de los ejes
plt.xlim(-0.1, 0.32)
plt.ylim(0.2, 0.7)

for indice, index in  enumerate([0,1,2]):
    data_computational = datos_comp[nombres[index]]
    data_computational = [(i-min(data_computational))/(max(data_computational)-min(data_computational)) for i in data_computational]
    Slopes, Per95 =  calculate_slopes_for_fit_medians_and_Per95(datos_obs= datos_obs, datos_comp= data_computational, box_count=box_count[indice])
    print(min(Slopes))
    # Dividir los puntos por encima y por debajo del threshold
    datos_filtrados = [(x, y) for x, y in zip(Slopes, Per95) if y > threshold[index-3]]
    X_filtrado, Y_filtrado = zip(*datos_filtrados)

    # Convertir a arrays de numpy para usarlos en la regresión lineal
    X_filtrado = np.array(X_filtrado).reshape(-1, 1)
    Y_filtrado = np.array(Y_filtrado)

    # Realizar la regresión lineal con los datos filtrados
    modelo = LinearRegression().fit(X_filtrado, Y_filtrado)

    # Obtener la pendiente y la intersección
    pendiente = modelo.coef_[0]
    interseccion = modelo.intercept_
    print(pendiente)
    # Crear el plot con colores diferentes para por encima y por debajo del threshold
    Scater = plt.scatter(Slopes, Per95, edgecolors=colores[indice], facecolors='white', marker=markers[indice], label = nombres[index])
    X_plot = np.linspace(min(X_filtrado), max(X_filtrado), 100)
    plt.plot(X_plot, modelo.predict(X_plot), color='k', linestyle = "--", label='_nolegend_')

    plt.axhline(threshold[indice], linestyle='--', color=colores[indice], label='_nolegend_')

plt.xlabel('Slope Linear Fit')
plt.ylabel(r'$P_{95}$(Traffic Intensity)')
#plt.legend(['BC', 'CC', 'DC'],bbox_to_anchor=(1.05, 1), loc='upper center')

#Agregando texto
'''
plt.text(0.1, (0.25+0.2)*0.5, f'$ \\alpha = 0.25$', 
    horizontalalignment='center', verticalalignment='center', 
    transform=plt.gca().transAxes, fontsize=16)
plt.text(0.1, (0.33+0.2)*0.5, f'$ \\alpha = 0.33$', 
    horizontalalignment='center', verticalalignment='center', 
    transform=plt.gca().transAxes, fontsize=16)
plt.text(0.1, (0.32+0.2)*0.5, f'$ \\alpha = 0.32$', 
    horizontalalignment='center', verticalalignment='center', 
    transform=plt.gca().transAxes, fontsize=16)
'''


''', label='_nolegend_'
# Calcular el coeficiente de determinación (R^2)
y_pred = modelo.predict(X_filtrado)
r2 = r2_score(Y_filtrado, y_pred)

# Calcular la desviación estándar
residuals = Y_filtrado - y_pred
std_dev = np.std(residuals)

# Resto del código de trazado...
# Añadir texto con R^2 y desviación estándar al gráfico
'''
plt.show()
