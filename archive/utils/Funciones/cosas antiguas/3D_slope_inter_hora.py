import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
import re
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import statistics


def obtener_nombres_con_H_M(lista_nombres,  hora_exacta=None, rango_horas=None):
    nombres_coincidentes = []
    patron = r"/\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(?:\.png)?"

    for nombre in lista_nombres:
        match = re.search(patron, nombre)
        if match:
            hora_minutos_str = match.group(0).split(".")[0].split("_")[1]
            hora = int(hora_minutos_str.split("-")[0])
            minutos = int(hora_minutos_str.split("-")[1])
            if hora_exacta is not None:
                if hora == hora_exacta[0] and minutos == hora_exacta[1]:
                    nombres_coincidentes.append(nombre)
            elif rango_horas is not None:
                hora_inicial = rango_horas[0]
                hora_final = rango_horas[1]

                for hora_in in range(hora_inicial, hora_final):
                    for minuto_in in range(0, 60, 15):
                        if hora == hora_in and minutos == minuto_in:
                            nombres_coincidentes.append(nombre)
            else:
                nombres_coincidentes.append(nombre)


    return nombres_coincidentes

# Función para convertir la hora en formato string a float
def convertir_hora(hora_string):
    partes = hora_string.split(":")
    horas = float(partes[0])
    minutos = float(partes[1]) / 60.0
    return horas + minutos

# Función para rotar manualmente
def rotate_graph(elev, azim):
    ax.view_init(elev=elev, azim=azim)
    plt.draw()

##########################################################################################################################

#NETWORK COMPLEJA

#CALLES 

#observacional
datos_obs = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")
lista_de_datos_obs = datos_obs.values.tolist()
lista_de_datos_obs = [lista[4:-1] for lista in lista_de_datos_obs]

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

for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):
        columnas_elejidas = obtener_nombres_con_H_M(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
        datos_new = datos_obs[columnas_elejidas].values.tolist()
        datos_new_mean = [np.mean(lista) for lista in datos_new]

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


# Crear una figura 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Gráfico de dispersión en el plano (hora, slope)
#ax.scatter(horas, slopes, zs=min(intercepts), zdir='z', )

# Gráfico de dispersión en el plano (hora, intercept)
#ax.scatter(horas, intercepts, zs=max(slopes), zdir='y', label='Intercept')

# Conectar los puntos con líneas
ax.plot(horas, slopes, zs=min(intercepts) - 10, zdir='z', c = "grey")
ax.plot(horas, intercepts, zs=max(slopes) + 10, zdir='y', c =  "grey")

ax.plot3D(horas, slopes, intercepts, c = "red")
ax.scatter3D(horas, slopes, intercepts, c = "red", alpha = 0.5)

# Etiquetas de los ejes y título
ax.set_xlabel('Hour')
ax.set_ylabel('m')
ax.set_zlabel('b')
ax.set_title(r'Ocupation fraction in random walk ')


# Ajustar límites y ángulo de visualización
ax.set_xlim(min(horas), max(horas))
ax.set_ylim(min(slopes), max(slopes) + 10)
ax.set_zlim(min(intercepts) - 10, max(intercepts))
ax.view_init(elev=20, azim=-40)  # Ángulos de elevación y azimut

plt.tight_layout()
# Mostrar el gráfico
plt.show()



"""
#almacenar los resultados
horas = []
MAE = []
Pendientes = []
Interseptos = []
Error_sqrt_medio = []
std_devs = []
r2_values = []
r2_values_ajust = []
hora_inicial, hora_final = 0, 24

for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):
        columnas_elejidas = obtener_nombres_con_H_M(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
        datos_new = datos_obs[columnas_elejidas].values.tolist()
        datos_new_mean = [np.mean(lista) for lista in datos_new]

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


# Crear una figura 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Gráfico de dispersión en el plano (hora, slope)
#ax.scatter(horas, slopes, zs=min(intercepts), zdir='z', )

# Gráfico de dispersión en el plano (hora, intercept)
#ax.scatter(horas, intercepts, zs=max(slopes), zdir='y', label='Intercept')

# Conectar los puntos con líneas
ax.plot(horas, slopes, zs=min(intercepts) - 10, zdir='z', c = "grey")
ax.plot(horas, intercepts, zs=max(slopes) + 30, zdir='y', c =  "grey")

ax.plot3D(horas, slopes, intercepts, c = "red")
ax.scatter3D(horas, slopes, intercepts, c = "red", alpha = 0.5)

# Etiquetas de los ejes y título
ax.set_xlabel('Hour')
ax.set_ylabel('m')
ax.set_zlabel('b')
ax.set_title(r'$C_B$')


# Ajustar límites y ángulo de visualización
ax.set_xlim(min(horas), max(horas))
ax.set_ylim(min(slopes), max(slopes) + 30)
ax.set_zlim(min(intercepts) - 10, max(intercepts))
ax.view_init(elev=20, azim=-40)  # Ángulos de elevación y azimut

plt.tight_layout()
# Mostrar el gráfico
plt.show()

"""