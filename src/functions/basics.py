import os
import csv
import numpy as np
from PIL import Image
import imageio
import re
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def CrearCarpeta(nombre_carpeta):
    # Ruta completa donde deseas crear la carpeta
    ruta_completa = os.path.join(os.getcwd(), nombre_carpeta)

    # Verifica si la carpeta no existe antes de crearla
    if not os.path.exists(ruta_completa):
        os.makedirs(ruta_completa)
        print(f"Se ha creado la carpeta '{nombre_carpeta}' en '{ruta_completa}'")
    else:
        pass

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

def crearNintervalosOrdenados(X, Y, N):
    def ordenar_listas(X, Y):
        # Emparejar los valores de X e Y
        pares = list(zip(X, Y))

        # Ordenar los pares basados en los valores de X
        pares_ordenados = sorted(pares, key=lambda x: x[0])

        # Separar los valores ordenados nuevamente en X e Y
        X_ordenado, Y_ordenado = zip(*pares_ordenados)

        return list(X_ordenado), list(Y_ordenado)
    
    X, Y = ordenar_listas(X,Y)

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

def apply_threshold(lista_de_listas, N):
    # Recorremos todas las listas en la lista de listas
    for lista in lista_de_listas:
        # Utilizamos una comprensión de lista para filtrar los números mayores o iguales a N
        lista[:] = [x for x in lista if x >= N]

        # Si la lista quedó vacía después de eliminar los elementos menores a N, agregamos un 0
        if not lista:
            lista.append(0)

    return lista_de_listas

def plot_distribution(data, name):

     # Crear una figura y ejes
    fig, ax = plt.subplots()

    # Ajustar el tamaño de las fuentes de los ejes X e Y
    ax.tick_params(axis='x', labelsize=18)  # Tamaño de fuente para el eje X
    ax.tick_params(axis='y', labelsize=18)  # Tamaño de fuente para el eje Y
    
    # Ajustar la cantidad de ticks en los ejes X e Y
    #ax.set_xticks([0.007, 0.01, 0.013, 0.016])
    #ax.set_yticks([0.1, 0.3, 0.5])

    # Ajustar el tamaño de las fuentes en las etiquetas y títulos
    
    ax.set_xlabel(rf'${name}$', fontsize=18)
    ax.set_ylabel(rf'$P[{name}]$', fontsize=18, rotation = 0)
    
    # Ajustar las coordenadas de las etiquetas de los ejes X e Y
    ax.xaxis.set_label_coords(1.04, 0.04)  
    ax.yaxis.set_label_coords(0, 1.01)

    # Eliminar el contorno superior y derecho del gráfico
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Graficar el histograma con las alturas de las barras ajustadas
    sns.histplot(data, bins=20, kde=True, color='red', ax=ax, stat="probability")

    # Agregar líneas de cuadrícula en el eje Y
    #ax.yaxis.grid(True)
    plt.tight_layout()
    # Mostrar el gráfico
    #plt.savefig(f"distribution {name}")
    plt.show()


def reescalar_lista_de_listas(lista_de_listas, maximo):

    lista_reescalada = []

    for lista in lista_de_listas:
        lista_reescalada.append([valor / maximo for valor in lista])

    return lista_reescalada