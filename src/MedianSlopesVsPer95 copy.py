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
#Conjunto de archivos
N505 = [Datos_computacionales[0], Datos_observacionales[2]]
N1207 = [Datos_computacionales[1], Datos_observacionales[0]]
datos_comp_N505 = pd.read_csv(N505[0])
datos_obs_N505 = pd.read_csv(N505[1])
datos_comp_N1207 = pd.read_csv(N1207[0])
datos_obs_N1207 = pd.read_csv(N1207[1])
data_observacional = [datos_obs_N505,datos_obs_N1207]
data_computacional  = [datos_comp_N505, datos_comp_N1207]
############################################
#model          Topology data,         datos de Google,       Topology Index  max R-Square    Treshold
ModelGN1207 =  [data_computacional[1], data_observacional[1] ,'CC'           ,0.815          ,0.328]
ModelDGN1207 = [data_computacional[1], data_observacional[1] ,'DiCC'         ,0.870          ,0.368]
ModelGN505 =   [data_computacional[0], data_observacional[0] ,'CC'           ,0.874          ,0.332]
ModelDGN505 =  [data_computacional[0], data_observacional[0] ,'DiCC'         ,0.919          ,0.329]


#All Models
Modelos = [ModelGN505, ModelGN1207, ModelDGN505, ModelDGN1207]
model_number = 0

data_computational = Modelos[model_number][0][Modelos[model_number][2]]
data_observational = Modelos[model_number][1]
threshold = Modelos[model_number][4]

data_computational = [(i-min(data_computational))/(max(data_computational)-min(data_computational)) for i in data_computational]
Slopes, Per95 =  calculate_slopes_for_fit_medians_and_Per95(datos_obs= data_observational, datos_comp= data_computational)

## Graficando
"""
Opcion 1
"""

plt.style.use(["science", "notebook", "grid"])
plt.tick_params(axis='both', labelsize=18)  # Tamaño de fuente para los números de los ejes

# Dividir los puntos por encima y por debajo del threshold
datos_filtrados = [(x, y) for x, y in zip(Slopes, Per95) if y > threshold]
X_filtrado, Y_filtrado = zip(*datos_filtrados)
medians_params = scipy.stats.linregress(X_filtrado, Y_filtrado)

# Convertir a arrays de numpy para usarlos en la regresión lineal
X_filtrado = np.array(X_filtrado).reshape(-1, 1)
Y_filtrado = np.array(Y_filtrado)

# Realizar la regresión lineal con los datos filtrados
modelo = LinearRegression().fit(X_filtrado, Y_filtrado)

# Obtener la pendiente y la intersección
pendiente = modelo.coef_[0]
interseccion = modelo.intercept_

# Calcular el coeficiente de determinación (R^2)
y_pred = modelo.predict(X_filtrado)
r2 = r2_score(Y_filtrado, y_pred)
print(pendiente, medians_params[0])
print(interseccion, medians_params[1])
print(r2, medians_params[2]**2)


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
#plt.xlim(x_min - 0.1 * x_range, x_max + 0.1 * x_range)
#plt.ylim(y_min - 0.1 * y_range, y_max + 0.1 * y_range)
#plt.ylim(threshold - 0.1 * y_range , y_max + 0.1 * y_range)
plt.xlim(0, 0.32)
plt.ylim(0.2, 0.7)
#plt.legend()

# Calcular la desviación estándar
residuals = Y_filtrado - y_pred
std_dev = np.std(residuals)

# Resto del código de trazado...
# Añadir texto con R^2 y desviación estándar al gráfico
plt.text(0.2, 0.9, f'$R^2$= {r2:.3f}', 
    horizontalalignment='center', verticalalignment='center', 
    transform=plt.gca().transAxes, fontsize=16)

posicion_alpha = (0.2 + (0.7-0.2)*threshold)

plt.text(0.8, posicion_alpha, r'$\alpha$= {:.3f}'.format(threshold), 
    horizontalalignment='center', verticalalignment='center', 
    transform=plt.gca().transAxes, fontsize=16)

plt.title(f'numero {model_number}')
plt.xlabel('Slope Linear Fit')
plt.ylabel('P95(traffic intensity)')
plt.show()
