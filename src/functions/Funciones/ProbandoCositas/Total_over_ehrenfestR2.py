from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, r2_score

import re

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


# Escala de horas:


# Crear un diccionario para almacenar los valores del canal rojo de los pixeles por día de la semana
red_values = {'06:00': [], '08:00': [], '10:00': [], '12:00': [], '14:00': [], '16:00': [], '18:00': [], '20:00': [], '22:00': []}

# Crear una lista con las imágenes y sus respectivos días de la semana
images = [('data/Images/ImgMean/Hour/6.png', '06:00'), 
            ('data/Images/ImgMean/Hour/8.png', '08:00'),
            ('data/Images/ImgMean/Hour/10.png', '10:00'),
            ('data/Images/ImgMean/Hour/12.png', '12:00'),
            ('data/Images/ImgMean/Hour/14.png', '14:00'),
            ('data/Images/ImgMean/Hour/16.png', '16:00'),
            ('data/Images/ImgMean/Hour/18.png', '18:00'),
            ('data/Images/ImgMean/Hour/20.png', '20:00'),
            ('data/Images/ImgMean/Hour/22.png', '22:00')]

# Iterar a través de cada pixel de la imagen
for image_path, day in images:
    image = Image.open(image_path)
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # Obtener el valor del canal rojo del pixel
            r, _, _ = image.getpixel((i, j))
            # Agregar el valor del canal rojo a la lista correspondiente al día de la semana
            if r!=0:
                red_values[day].append(r)



#CALLES 

#observacional
datos_obs = pd.read_csv("data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv")
lista_de_datos_obs = datos_obs.values.tolist()
lista_de_datos_obs = [lista[4:-1] for lista in lista_de_datos_obs]

"ehrenfest sim"
datos_sim = pd.read_csv("data/DataNetwork/StreetAsNode/estado_ejes_500M_10msteps.csv")
lista_valores_ultima_columna = datos_sim[datos_sim.columns[-1]].tolist()
print(lista_valores_ultima_columna)

maximo_autos_por_calle = pd.read_csv("data/DataNetwork/StreetAsNode/N_max_autos_por_calle.csv")
maximo_autos_por_calle = maximo_autos_por_calle[maximo_autos_por_calle.columns[-1]].tolist()
print(maximo_autos_por_calle)

fraction_taco = [i/j for i,j in zip(lista_valores_ultima_columna, maximo_autos_por_calle)]
print(fraction_taco)


x_label = "fill fraction"
datos_computacionales = fraction_taco

#almacenar los resultados
horas = []
mae_values = []
r2_values = []
hora_inicial, hora_final = 0, 24

for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):
        columnas_elejidas = obtener_nombres_con_H_M(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
        datos_new = datos_obs[columnas_elejidas].values.tolist()
        # Calcular el promedio de cada sublista en lista_de_datos_comp
        datos_new = [np.mean(datos) for datos in datos_new]

        datos_new = min_max_scaling(datos_new)
        datos_computacionales = min_max_scaling(datos_computacionales)
        # Calcular el MAE y el R2
        mae = mean_absolute_error(datos_computacionales, datos_new)
        r2 = r2_score(datos_computacionales, datos_new)

        # Agregar los resultados a las listas
        horas.append(f"{hora_in}:{minuto_in}")
        mae_values.append(mae)
        r2_values.append(r2)


# Crear una figura y un primer eje y
fig, ax1 = plt.subplots()

# Graficar la línea de R2 en el primer eje y
color = 'tab:blue'
ax1.plot(horas, r2_values, label='R2', color=color, marker='x')
ax1.set_xlabel('Hora del día')
ax1.set_ylabel('R2', color=color)
ax1.tick_params(axis='y', labelcolor=color)

# Crear un segundo eje y
ax2 = ax1.twinx()

#print(red_values)
data = list(red_values.values())
ax2.boxplot(data)

# Graficar los datos computacionales (fraction_taco) en el segundo eje y
color = 'tab:red'
ax2.set_ylabel('Fraction Taco', color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Mostrar una leyenda combinando ambas líneas de los ejes y
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2)

# Ajustar el espaciado para evitar recorte de etiquetas
plt.tight_layout()

# Mostrar el gráfico
plt.show()