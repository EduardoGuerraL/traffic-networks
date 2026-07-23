import csv
from PIL import Image
import imageio
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Funciones básicas

def csv_to_txt(archivo_entrada, archivo_salida):
    """
    Convierte un archivo de una columna en un txt:

        columna ----> (a, b, c, d, ...)

    """
    # Leer valores de la segunda columna del archivo CSV
    valores_segunda_columna = []
    with open(archivo_entrada, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Saltar el encabezado si existe
        for row in reader:
            valor = int(row[1])
            valores_segunda_columna.append(valor)

    # Convertir los valores en una cadena separada por comas
    cadena_valores = ','.join(str(valor) for valor in valores_segunda_columna)

    # Escribir la cadena de valores en el archivo de salida
    with open(archivo_salida, 'w') as txtfile:
        txtfile.write(cadena_valores)

def txt_to_csv(archivo_entrada, archivo_salida, steps):
    """
    Convierte la salida de Random Walk a un csv compatible con las
    demás funciones.
    """
    def read_data_from_file(file_path):
        data = []
        with open(file_path, 'r') as file:
            for line in file:
                # Parse the numbers from each line and store them in a tuple
                numbers = tuple(map(int, line.strip('()\n').split(',')))
                data.append(numbers)
        return data

    def transpose_data(data):
        # Transpose the data to change rows into columns
        transposed_data = list(zip(*data))
        return transposed_data

    def write_data_to_file(file_path, transposed_data, steps_column):
        with open(file_path, 'w') as file:
            # Write the column names as the first row
            column_names = ["nodo"] + [f"{i * steps_column}" for i in range(1, len(transposed_data[0]))]
            file.write(",".join(column_names) + "\n")
            
            # Write the transposed data to the file in the desired format
            for idx, row in enumerate(transposed_data):
                file.write(f"{idx}, {', '.join(str(num) for num in row)}\n")
    
    data = read_data_from_file(archivo_entrada)

    # Transpose the data
    transposed_data = transpose_data(data)

    # Write the transposed data to the output file
    write_data_to_file(archivo_salida, transposed_data, steps)

def imgs_to_gif(input_folder, output_gif_path, frame_duration):


    def extract_time(filename):
        # Extraer la hora del nombre de archivo en formato "scatter_CC_hour = 18:0.png"
        time_str = filename.split('=')[-1].split('.png')[0].strip()
        hour, minute = map(int, time_str.split(':'))
        return hour, minute

    def create_gif(image_folder, output_gif, duration=0.5):
        # Lista todos los archivos en la carpeta de imágenes y ordenalos cronológicamente
        image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')], key=extract_time)

        images = []
        for filename in image_files:
            file_path = os.path.join(image_folder, filename)
            img = Image.open(file_path)
            images.append(img)

        # Guarda las imágenes como GIF
        imageio.mimsave(output_gif, images, duration=duration)

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

def obtener_nombres_con_H_M_sinFDS(lista_nombres,  hora_exacta=None, rango_horas=None):
    nombres_coincidentes = []
    patron = r"/\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(?:\.png)?"

    for nombre in lista_nombres:
        match = re.search(patron, nombre)
        if match:
            fecha_str = match.group(0).split(".")[0].split("/")[1]
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d_%H-%M")

            hora_minutos_str = match.group(0).split(".")[0].split("_")[1]
            hora = int(hora_minutos_str.split("-")[0])
            minutos = int(hora_minutos_str.split("-")[1])

            if fecha.weekday() < 5:
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

def calcular_r_cuadrado(lista1, lista2):

    matriz_X = np.array(lista1).reshape(-1, 1)
    matriz_Y = np.array(lista2).reshape(-1, 1)
    model = LinearRegression()
    model.fit(matriz_X, matriz_Y)
    y_pred = model.predict(matriz_X).flatten().tolist()
    
    Media_Y = np.mean(lista2)

    #Calculo de SS_{tot}:
    SS_tot = sum([(Y - Media_Y)**2 for Y in lista2])

    #Calculo de SS_{res}
    SS_res = sum([(Y - Y_pred)**2 for Y, Y_pred in zip(lista2, y_pred)] )

    R_cuadrado = 1 - (SS_res/SS_tot)

    return R_cuadrado

# Funciones de Visualización de la red.

def graph_ocupation_randomWalk_to_node(file_states_for_RW, file_max_ocupation, index_node):
    
    indice_i = index_node
    
    df = pd.read_csv(file_states_for_RW)
    df_max = pd.read_csv(file_max_ocupation)

    # Seleccionar la columna del índice específico
    data_street = df.iloc[indice_i][1:]
    max_car_in_street = df_max.iloc[indice_i][1]

    plt.rc('font', size=18)
    # Dibuja la recta roja horizontal
    plt.axhline(y=max_car_in_street, color='red', linestyle='-')
    # Etiqueta la recta con 'Max'
    plt.text(0.5, max_car_in_street + 0.1, 'Max', color='red', fontsize=18)

    data_time = [int(val) for val in data_street.index]
    ## Graficar el avance en el tiempo del índice i
    plt.plot(data_time, data_street.values)
    plt.xlabel('')
    plt.ylabel('ocupation')
    plt.title(f'Node {indice_i}')

    # Mostrar solo el primer, último y valor medio del intervalo
    marcadores = [data_time[0], data_time[-1], data_time[len(data_time)//2]]
    etiquetas = [f'{val:.1e}' for val in marcadores]

    plt.xticks(marcadores, etiquetas)

    #dibujar linea promedio de datos
    promedio = round(np.mean(data_street), 1)
    plt.axhline(y=promedio, color='red', linestyle='-')
    # Etiqueta la recta con 'Min'
    plt.text(0.5, promedio + 0.1, 'Mean', color='red', fontsize=18)

    plt.tight_layout()  # Elimina espacios en los bordes
    plt.show()
