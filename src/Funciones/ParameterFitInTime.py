import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
from sklearn.metrics import mean_absolute_error, r2_score
import re
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import statistics
import seaborn as sns

from functions import calcular_r_cuadrado


def scatter_with_linear_fit(x_values, y_values):
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
    
    # Calcular la desviación estándar
    std_dev = statistics.stdev(y_values)
    
    # Crear el gráfico de dispersión
    #plt.figure(figsize=(10, 6))
    #plt.scatter(x_values, y_values, label='Datos')
    #plt.plot(x_values, y_pred, color='red', label='Ajuste lineal')
    #plt.xlabel('X')
    #plt.ylabel('Y')
    #plt.title('Gráfico de Dispersión con Ajuste Lineal')
    #plt.legend()
    
    # Mostrar el gráfico
    #plt.show()
    return mse, std_dev, slope, intercept
    # Imprimir los resultados
    #print(f'Pendiente: {slope:.4f}')
    #print(f'Intersección: {intercept:.4f}')
    #print(f'Error Cuadrático Medio: {mse:.4f}')
    #print(f'Desviación Estándar: {std_dev:.4f}')

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

def scatter_with_errorbars(compu_data, list_of_list_of_Obs, show_error_bars=True, xlabel = "datos x", ylabel = "datos y", title = "title" , font_size=16 ):

    def calcular_desviacion_estandar(lista, promedio):
            diferencias = np.array(lista) - promedio
            diferencias_cuadrado = diferencias ** 2
            varianza = np.mean(diferencias_cuadrado)
            desviacion_estandar = np.sqrt(varianza)
            return desviacion_estandar
        
        
    # Calcular la media y desviación estándar de cada lista en list_of_list_of_Obs

    means = [np.mean(data) for data in list_of_list_of_Obs]
    std_devs = [np.std(data) for data in list_of_list_of_Obs]
    std_dev_down = []
    std_devs_up = []

    for lista, promedio in zip(lista_de_datos_obs, means):
        lista_up = [i for i in lista if i >= promedio]
        lista_down = [i for i in lista if i <= promedio]
        desviacion_abajo = calcular_desviacion_estandar(lista_down, promedio)
        std_dev_down.append(desviacion_abajo)
        desviacion_arriba = calcular_desviacion_estandar(lista_up, promedio)
        std_devs_up.append(desviacion_arriba)

    # Crear el gráfico de dispersión
    plt.figure(figsize=(8, 6))

    if show_error_bars:
        plt.errorbar(compu_data, means, yerr=[std_dev_down, std_devs_up], fmt='o', mec='black', mfc='white', ecolor='black', capsize=0, label='mean and std dev',elinewidth= 0.3)
    elif not show_error_bars:
        plt.scatter(compu_data, means, marker='o',c='white',edgecolors='black',label = "mean")

    # Realizar la regresión lineal
    regression_coeffs = np.polyfit(compu_data, means, 1)  # Fit a first-degree polynomial (line) to the data
    regression_line = np.polyval(regression_coeffs, compu_data)  # Generate y-values for the regression line

    plt.plot(compu_data, regression_line, color='red', label='linear fit')
    plt.ylim(0, 255)

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

    # Mostrar el gráfico
    plt.tight_layout()
    plt.savefig("scatter_"+str(xlabel)+"_"+str(title)+".png")
    #plt.show()

def calcular_r_cuadrado_y_mae(valores_obs, valores_pred):

    means = [np.mean(data) for data in valores_obs]

    if len(means) != len(valores_pred):
        raise ValueError("Las listas deben tener la misma longitud")

    # Cálculo del R cuadrado
    media_obs = sum(means) / len(means)
    ss_tot = sum((obs - media_obs) ** 2 for obs in means)
    ss_res = sum((obs - pred) ** 2 for obs, pred in zip(means, valores_pred))
    r_cuadrado = 1 - (ss_res / ss_tot)

    # Cálculo del MAE
    mae = sum(abs(obs - pred) for obs, pred in zip(means, valores_pred)) / len(means)

    return r_cuadrado, mae

def min_max_scaling(data):
    min_val = min(data)
    max_val = max(data)

    if min_val == max_val:
        # Si todos los valores son iguales, devolvemos una lista con todos los valores como 0.5
        return [0.5] * len(data)

    scaled_data = [(x - min_val) / (max_val - min_val) for x in data]
    return scaled_data

def Super_funcion():

    columnas_elejidas = obtener_nombres_con_H_M(datos_obs.columns, rango_horas=(7, 22))
    datos_new = datos_obs[columnas_elejidas].values.tolist()
    scatter_with_errorbars(lista_de_datos_comp, datos_new, ylabel= "Red Pixel Intensity", xlabel="BC", title="range hour = 7-22", show_error_bars=False)

    columnas_elejidas = obtener_nombres_con_H_M(datos_obs.columns)
    datos_new = datos_obs[columnas_elejidas].values.tolist()
    scatter_with_errorbars(lista_de_datos_comp, datos_new, ylabel= "Red Pixel Intensity", xlabel="BC", title="total data",show_error_bars=False)


    #almacenar los resultados
    horas = []
    mae_values = []
    r2_values = []
    hora_inicial, hora_final = 0, 24

    for hora_in in range(hora_inicial, hora_final):
        for minuto_in in range(0, 60, 15):
            columnas_elejidas = obtener_nombres_con_H_M(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
            datos_new = datos_obs[columnas_elejidas].values.tolist()
            scatter_with_errorbars(lista_de_datos_comp, datos_new, ylabel= "Red Pixel Intensity", xlabel="BC", title="hour = "+str(hora_in)+":"+str(minuto_in), show_error_bars=True)

            # Calcular el promedio de cada sublista en lista_de_datos_comp
            datos_new = [np.mean(datos) for datos in datos_new]

            datos_new = min_max_scaling(datos_new)
            lista_de_datos_comp = min_max_scaling(lista_de_datos_comp)
            # Calcular el MAE y el R2
            mae = mean_absolute_error(lista_de_datos_comp, datos_new)
            r2 = r2_score(lista_de_datos_comp, datos_new)

            # Agregar los resultados a las listas
            horas.append(f"{hora_in}")
            mae_values.append(mae)
            r2_values.append(r2)


    # Graficar los resultados en dos ejes y con diferentes colores
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Horas')
    ax1.set_ylabel('MAE', color=color)
    ax1.plot(horas, mae_values, label='MAE', color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid()

    ax2 = ax1.twinx()  # Crear un segundo eje y

    color = 'tab:blue'
    ax2.set_ylabel('R2', color=color)
    ax2.plot(horas, r2_values, label='R2', color=color, marker='x')
    ax2.tick_params(axis='y', labelcolor=color)

    # Ajustar los ticks del eje x (horas) para que aparezcan solo cada 4 valores
    x_ticks_step = 4
    plt.xticks(range(0, len(horas), x_ticks_step), horas[::x_ticks_step], rotation=45)

    plt.title('MAE y R2 por Hora')
    plt.tight_layout()
    plt.show()

    plt.title('MAE y R2 por Hora')
    plt.tight_layout()
    plt.show()



##########################################################################################################################

#NETWORK COMPLEJA

#CALLES 

#observacional
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

datos_computacionales = lista_de_datos_comp_3

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
        r2 = calcular_r_cuadrado(x_values, y_values)
        print(r2)

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


fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(9, 5))
axes = axes.flat
columnas_numeric = [MAE, r2_values, Pendientes, Interseptos, Error_sqrt_medio, std_devs]
columnas_label = ["mae", "r square", "slope", "intersept", "mse", "std_dev"]

for i, colum in enumerate(columnas_numeric):
    print(colum)
    axes[i].plot(horas, colum)
    axes[i].set_title(f"hour vs {columnas_label[i]}", fontsize = 7, fontweight = "bold")
    #axes[i].yaxis.set_major_formatter(ticker.EngFormatter())
    #axes[i].xaxis.set_major_formatter(ticker.EngFormatter())
    #axes[i].ticklabel_format(style='sci', scilimits=(-4,4), axis='both')
    #axes[i].tick_params(labelsize = 6)
    #axes[i].set_xlabel("")
    #axes[i].set_ylabel("")

    # Establecer los ticks en el eje x
    x_ticks = range(0, len(horas), 4)  # Números del 0 al 23 cada 4 números
    axes[i].set_xticks(x_ticks, range(0,24))

fig.tight_layout()
plt.subplots_adjust(top=0.9)
fig.suptitle('Parameters of scatter Observational data per hour vs degree centrality', fontsize = 10, fontweight = "bold")
plt.show()
