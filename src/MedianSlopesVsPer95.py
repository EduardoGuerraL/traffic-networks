import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scienceplots
import seaborn as sns
from sklearn.linear_model import LinearRegression
from statistics import mode
from sklearn.metrics import r2_score
from scipy import stats
from scipy.stats import scoreatpercentile
from functions.basics import CrearCarpeta, reescalar_lista_de_listas, obtener_nombres_con_H_M_sinFDS, crearNintervalosOrdenados
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

def calculate_slopes_for_fit_medians_and_Per95(datos_obs, datos_comp):
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
            
            y_medians, x_medians = calculate_median_positions(datos_comp, promedios, 20)
            
            ## REGRESION LINEAL
            #(slope, intercept, r_value, p_value, std_err)
            medians_params = scipy.stats.linregress(x_medians, y_medians)
            
            Slopes.append(medians_params[0])
            Per95.append(percentil_95)
    
    return Slopes, Per95


##########################################################################################################################
## Datos Computacionales

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
            "mean_state_RWM_lim"
        ]

###########################################
nombres = ["CC"]
############################################

data_computational = datos_comp["CC"]
data_computational = [(i-min(data_computational))/(max(data_computational)-min(data_computational)) for i in data_computational]
    
Slopes, Per95 =  calculate_slopes_for_fit_medians_and_Per95(datos_obs= datos_obs, datos_comp= data_computational)

## Graficando

#borrar opciones luego de que elijamos
"""
Opcion 1
"""

# threshold M
threshold = 0.35

plt.style.use(["science", "notebook", "grid"])
plt.tick_params(axis='both', labelsize=18)  # Tamaño de fuente para los números de los ejes

# Dividir los puntos por encima y por debajo del threshold
datos_filtrados = [(x, y) for x, y in zip(Slopes, Per95) if y > threshold]
X_filtrado, Y_filtrado = zip(*datos_filtrados)

# Convertir a arrays de numpy para usarlos en la regresión lineal
X_filtrado = np.array(X_filtrado).reshape(-1, 1)
Y_filtrado = np.array(Y_filtrado)

# Realizar la regresión lineal con los datos filtrados
modelo = LinearRegression().fit(X_filtrado, Y_filtrado)

# Obtener la pendiente y la intersección
pendiente = modelo.coef_[0]
interseccion = modelo.intercept_

"""
# Dibujar el fondo dividido por el threshold
plt.axhspan(-1, threshold, facecolor='skyblue', alpha=0.6)  # Área por debajo del threshold
plt.axhspan(threshold, 2, facecolor='firebrick', alpha=0.8)   # Área por encima del threshold
"""
# Crear el plot con colores diferentes para por encima y por debajo del threshold
plt.scatter(Slopes, Per95, edgecolors='black', facecolors='white')

X_plot = np.linspace(min(X_filtrado), max(X_filtrado), 100)
plt.plot(X_plot, modelo.predict(X_plot), color='k', label=f'Fit\n (y = {pendiente:.2f} x + {interseccion:.2f})', linestyle = "--")
plt.axhline(threshold, linestyle='--', color='gray')

# Límites de los ejes X e Y con un pequeño margen alrededor de los datos
x_min, x_max = min(Slopes), max(Slopes)
y_min, y_max = min(Per95), max(Per95)

x_range = x_max - x_min
y_range = y_max - y_min

# Agregar un pequeño margen alrededor de los datos
plt.xlim(x_min - 0.1 * x_range, x_max + 0.1 * x_range)
plt.ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)
plt.ylim(threshold - 0.1 * y_range , y_max + 0.1 * y_range)
plt.legend()

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

plt.text(0.8, 0.2, r'$\alpha$= {:.3f}'.format(threshold), 
    horizontalalignment='center', verticalalignment='center', 
    transform=plt.gca().transAxes, fontsize=16)

plt.show()

"""
opcion 2
"""

# threshold M
threshold = 0.35
plt.tick_params(axis='both', labelsize=18)  # Tamaño de fuente para los números de los ejes

# Dividir los puntos por encima y por debajo del threshold
datos_filtrados = [(x, y) for x, y in zip(Slopes, Per95) if y > threshold]
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
plt.scatter(Slopes, Per95, edgecolors='black', facecolors='white', label='Datos filtrados')

X_plot = np.linspace(min(X_filtrado), max(X_filtrado), 100)
plt.plot(X_plot, modelo.predict(X_plot), color='k', label='Regresión lineal', linestyle = "--")
#plt.axhline(threshold, linestyle='--', color='gray')

# Límites de los ejes X e Y con un pequeño margen alrededor de los datos
x_min, x_max = min(Slopes), max(Slopes)
y_min, y_max = min(Per95), max(Per95)

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
