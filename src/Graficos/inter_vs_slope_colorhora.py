import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
import re
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import statistics

from Funciones.functions import obtener_nombres_con_H_M_sinFDS

# Función para convertir la hora en formato string a float
def convertir_hora(hora_string):
    partes = hora_string.split(":")
    horas = float(partes[0])
    minutos = float(partes[1]) / 60.0
    return horas + minutos


##########################################################################################################################

# NETWORK SIMPLE

# observacional
datos_obs = pd.read_csv("data/DataImages/In_Streets_Coord/Normal/streetsCoordsR1S4.csv")
#computacional
datos_comp = pd.read_csv("data/DataNetwork/StreetAsNode/Basic_and_advaced_data_network_aristas.csv")
lista_de_datos_comp_2 = datos_comp["Closeness_streets"].tolist()
lista_de_datos_comp = datos_comp["Betweenness_streets"].tolist()
lista_de_datos_comp_3 = datos_comp["Degree_streets"].tolist()


# RANDOM WALK
datos_sim = pd.read_csv("data/DataNetwork/StreetAsNode/Simple_states_10mA_500BT_10mS_streets.csv")
lista_valores_ultima_columna = datos_sim[datos_sim.columns[-1]].tolist()

maximo_autos_por_calle = pd.read_csv("data/DataNetwork/StreetAsNode/Simple_max_ocupation_per_streets.csv")
maximo_autos_por_calle = maximo_autos_por_calle[maximo_autos_por_calle.columns[-1]].tolist()

fraction_taco = [i/j for i,j in zip(lista_valores_ultima_columna, maximo_autos_por_calle)]


# Graficando 
#============================
#graficar los parametros en el tiempo.


datos_computacionales = fraction_taco

horas = []
MAE = []
Pendientes = []
Interseptos = []
Error_sqrt_medio = []
std_devs = []
r2_values = []
r2_values_ajust = []
hora_inicial, hora_final = 0, 24

promedio_ocupacion_total = []

for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):
        columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
        datos_new = datos_obs[columnas_elejidas].values.tolist()
        datos_new_mean = [np.mean(lista) for lista in datos_new]

        promedio_ocupacion_total.append(np.mean(datos_new_mean))

        x_values = datos_computacionales
        y_values = datos_new_mean

        # Convertir las listas en arrays de numpy para facilitar el cálculo
        x_array = np.array(x_values)
        y_array = np.array(y_values)
        
        # Crear el modelo de regresión lineal
        model = LinearRegression()
        model.fit(x_array.reshape(-1, 1), y_array)
        
        # Calcular la pendiente y la intersección
        slope = model.coef_[0]
        intercept = model.intercept_
        
        # Realizar predicciones usando el modelo
        y_pred = model.predict(x_array.reshape(-1, 1))
        
        # Calcular el error cuadrático medio
        mse = mean_squared_error(y_array, y_pred)
        
        # Calcular el error absoluto medio
        mae = mean_absolute_error(y_array, y_pred)

        # Calcular r2
        r2 = r2_score(y_array, y_pred)


        # Calcular la desviación estándar
        std_dev = statistics.stdev(y_values)

        #Introduciendo a las listas
        Pendientes.append(slope)
        Interseptos.append(intercept)
        Error_sqrt_medio.append(mse)
        MAE.append(mae)
        r2_values.append(r2)
        std_devs.append(std_dev)

        horas.append(f"{hora_in}:{minuto_in}")


# Datos_ocupados
slopes = np.array(Pendientes)
intercepts = np.array(Interseptos)
# Lista de horas convertidas a float
horas = np.array([convertir_hora(hora_string) for hora_string in horas])

# Crear un gráfico de dispersión con colores basados en la lista color_data
plt.figure(figsize=(8, 6))  # Ajustar el tamaño de la figura
scatter = plt.scatter(slopes, intercepts, c=promedio_ocupacion_total, s = np.array(std_devs) * 5 ,  cmap='turbo', marker='o', label='Datos')

#plt.plot(slopes, intercepts, c = "gray")

# Agregar barra de color
cbar = plt.colorbar(scatter)
cbar.set_label('mean total ocupation',  fontsize=20)


# Etiquetas y título
plt.xlabel(r'$m$',  fontsize=20)
plt.ylabel(r'$b$',  fontsize=20)
plt.title(r'$Random Walk$',  fontsize=20)


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)


# Gráfico de dispersión en el plano (hora, slope)
#ax.scatter(horas, slopes, zs=min(intercepts), zdir='z', )

# Gráfico de dispersión en el plano (hora, intercept)
#ax.scatter(horas, intercepts, zs=max(slopes), zdir='y', label='Intercept')

plt.tight_layout()
# Mostrar el gráfico
plt.show()



# NETWORK COMPLEJA

# CALLES 

# Observacional(Google)
datos_obs = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")

#computacional
datos_comp = pd.read_csv("data/DataNetwork/StreetAsNode/Basic_and_advaced_data_network_aristas_detallado.csv")
lista_de_datos_comp_2 = datos_comp["Closeness_streets"].tolist()
lista_de_datos_comp = datos_comp["Betweenness_streets"].tolist()
lista_de_datos_comp_3 = datos_comp["Degree_streets"].tolist()

"ehrenfest sim"
datos_sim = pd.read_csv("data/DataNetwork/StreetAsNode/estado_ejes_500M_10msteps.csv")
lista_valores_ultima_columna = datos_sim[datos_sim.columns[-1]].tolist()

maximo_autos_por_calle = pd.read_csv("data/DataNetwork/StreetAsNode/N_max_autos_por_calle.csv")
maximo_autos_por_calle = maximo_autos_por_calle[maximo_autos_por_calle.columns[-1]].tolist()

fraction_taco = [i/j for i,j in zip(lista_valores_ultima_columna, maximo_autos_por_calle)]

# Graficando 
#============================
#graficar los parametros en el tiempo.


datos_computacionales = lista_de_datos_comp

horas = []
MAE = []
Pendientes = []
Interseptos = []
Error_sqrt_medio = []
std_devs = []
r2_values = []
r2_values_ajust = []
hora_inicial, hora_final = 0, 24

promedio_ocupacion_total = []

for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):
        columnas_elejidas = obtener_nombres_con_H_M(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
        datos_new = datos_obs[columnas_elejidas].values.tolist()
        datos_new_mean = [np.mean(lista) for lista in datos_new]

        promedio_ocupacion_total.append(np.mean(datos_new_mean))

        x_values = datos_computacionales
        y_values = datos_new_mean

        # Convertir las listas en arrays de numpy para facilitar el cálculo
        x_array = np.array(x_values)
        y_array = np.array(y_values)
        
        # Crear el modelo de regresión lineal
        model = LinearRegression()
        model.fit(x_array.reshape(-1, 1), y_array)
        
        # Calcular la pendiente y la intersección
        slope = model.coef_[0]
        intercept = model.intercept_
        
        # Realizar predicciones usando el modelo
        y_pred = model.predict(x_array.reshape(-1, 1))
        
        # Calcular el error cuadrático medio
        mse = mean_squared_error(y_array, y_pred)
        
        # Calcular el error absoluto medio
        mae = mean_absolute_error(y_array, y_pred)

        # Calcular r2
        r2 = r2_score(y_array, y_pred)


        # Calcular la desviación estándar
        std_dev = statistics.stdev(y_values)

        #Introduciendo a las listas
        Pendientes.append(slope)
        Interseptos.append(intercept)
        Error_sqrt_medio.append(mse)
        MAE.append(mae)
        r2_values.append(r2)
        std_devs.append(std_dev)

        horas.append(f"{hora_in}:{minuto_in}")


# Datos_ocupados
slopes = np.array(Pendientes)
intercepts = np.array(Interseptos)
# Lista de horas convertidas a float
horas = np.array([convertir_hora(hora_string) for hora_string in horas])

# Crear un gráfico de dispersión con colores basados en la lista color_data
plt.figure(figsize=(8, 6))  # Ajustar el tamaño de la figura
scatter = plt.scatter(slopes, intercepts, c=promedio_ocupacion_total, s = np.array(std_devs) * 5 ,  cmap='turbo', marker='o', label='Datos')

#plt.plot(slopes, intercepts, c = "gray")

# Agregar barra de color
cbar = plt.colorbar(scatter)
cbar.set_label('mean total ocupation',  fontsize=20)


# Etiquetas y título
plt.xlabel(r'$m$',  fontsize=20)
plt.ylabel(r'$b$',  fontsize=20)
plt.title(r'$C_B$',  fontsize=20)


plt.xticks(fontsize=15)
plt.yticks(fontsize=15)


# Gráfico de dispersión en el plano (hora, slope)
#ax.scatter(horas, slopes, zs=min(intercepts), zdir='z', )

# Gráfico de dispersión en el plano (hora, intercept)
#ax.scatter(horas, intercepts, zs=max(slopes), zdir='y', label='Intercept')

plt.tight_layout()
# Mostrar el gráfico
plt.show()

