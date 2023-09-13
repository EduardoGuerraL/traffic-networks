
using PyCall
py"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from Colores import VERDES, NARANJOS, ROJOS, MORADOS
import statistics as st
import csv
import math
from statistics import mean 

# convertir los conjuntos en sets
VERDES_set = set(VERDES)
NARANJOS_set = set(NARANJOS)
MORADOS_set = set(MORADOS)
ROJOS_set = set(ROJOS)    

import os
from PIL import Image

class DataImagesForNodes:

    def __init__(self, path_dir_screenshots:str, path_dir_network_data: str):

        self.image_no_traffic = plt.imread(path_dir_screenshots + "/2023-03-29_07-30.png") #Imagen temp/screenTest/2023-03-29_07-30.png
        self.path_dir_screenshots = str(path_dir_screenshots)
        
        self.NodesdataFrame = pd.DataFrame()
        self.images_already_processed = []

        position_of_vertices = eval(open(str(path_dir_network_data)+"/Posiciones.dat", "r").readline())
        self.position_of_vertices = {} #Posiciones
        for i, tupla in enumerate(position_of_vertices):
            self.position_of_vertices[i] = list([tupla[0]*self.image_no_traffic.shape[1], tupla[1]*self.image_no_traffic.shape[0]])
        
        self.conections = position_of_vertices = eval(open(str(path_dir_network_data)+"/Conexiones.dat", "r").readline())

        self.makeDataFrame(self.position_of_vertices, "Coordenadas")

    def addTrafficColorToDataFrame(self):
        "Es como la función principal, al usarla añade todas las columnas de datos al dataframe"
        
        files = os.listdir(self.path_dir_screenshots)

        N_files_in_dir = len(files)
        images_already_processed = set(self.images_already_processed)

        count = 0
        for archivo in files:
        
            archivo_sin_png = archivo.replace(".png", "")
            images_already_processed.add(archivo)
            namefile = os.path.join(self.path_dir_screenshots, archivo)
            
            dict_to_add_to_dataFrame = {index: self.changeColor(self.getPixelFromPath(namefile, coords[0], coords[1]), 0,  85, 170, 255)
                                        for index, coords in self.position_of_vertices.items()}

            self.addColumnToDataFrame(dict_to_add_to_dataFrame, archivo_sin_png)
            count += 1
            print(f"{count/N_files_in_dir*100:.1f}%") 

    def addTrafficColorToDataFrameFromHDF5(self, file_name_hdf5):
        
        with pd.HDFStore(file_name_hdf5, mode='r') as store:
            # Obtener la lista de claves (nombres de las imágenes)
            nombres = store.keys()
            coordenadas = self.position_of_vertices.items()
        
            for nombre in nombres:
                datos = store[nombre]
                dict_to_add_to_dataFrame = {index: datos.iloc[round(coords[1]), round(coords[0])] for index, coords in self.position_of_vertices.items()}
                nombre_sin_png = nombre.replace(".png", "")
                self.addColumnToDataFrame(dict_to_add_to_dataFrame, nombre_sin_png)
        
        return self.NodesdataFrame

    def makeDataFrame(self, dict_to_column: dict, column_name:str, index_name:str = "Nodo"):


        keys_of_dict = dict_to_column.keys()
        ordered_values = list(dict_to_column.values())
        
        self.NodesdataFrame = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        self.NodesdataFrame.set_index(str(index_name), inplace=True)
    
    def addColumnToDataFrame(self, dict_to_add: dict , column_name:str):
 
        keys_of_dict = dict_to_add.keys()
        ordered_values = list(dict_to_add.values())

        df_to_add = pd.DataFrame({"Nodo": keys_of_dict, str(column_name) : ordered_values})
        df_to_add.set_index('Nodo', inplace=True)
        self.NodesdataFrame = pd.concat([self.NodesdataFrame, df_to_add], axis = 1)

    def saveDataFrame(self, name_to_file):
        self.NodesdataFrame.to_csv("temp/" + str(name_to_file), index=True)

    def changeColor(self, pixel_from_image: tuple, Green: int, Orange: int, Red: int, Brown: int):
        b, g, r, alpha = pixel_from_image
        newPixel = 0
        if (r,g,b) in VERDES_set:
            newPixel = Green  
        elif (r,g,b) in NARANJOS_set:
            newPixel = Orange
        elif (r,g,b) in MORADOS_set:
            newPixel = Brown
        elif (r,g,b) in ROJOS_set:
            newPixel = Red
        return newPixel
    def getPixelFromPath(self, ruta_imagen, x, y):
        
        # Cargar la imagen
        imagen = Image.open(ruta_imagen)
        # Obtener el valor del píxel en las coordenadas dadas
        valor_pixel = imagen.load()[x, y]

        return valor_pixel
        
    def updateDataFromGoogleImages(self, name_file_dataFrame:str):
 
        self.NodesdataFrame = pd.read_csv(str(name_file_dataFrame))
        files = os.listdir(self.path_dir_screenshots)
        
        missing_columns = set(files) - set(self.NodesdataFrame.columns)
        siono = input(f"Quieres actualizar los {len(missing_columns)} archivos que faltan?(Yes/not)")

        if siono in ("Yes", "y", "yes", "YES", "Y"):
            count = 0
            for archivo in missing_columns:
            
                namefile = os.path.join(self.path_dir_screenshots, archivo)
                
                dict_to_add_to_dataFrame = {index: self.changeColor(self.getPixelFromPath(namefile, coords[0], coords[1]), 0,  85, 170, 255)
                                            for index, coords in self.position_of_vertices.items()}

                self.addColumnToDataFrame(dict_to_add_to_dataFrame, archivo)
                count += 1
                print(f"{count/len(missing_columns)*100:.1f}%") 

                self.saveDataFrame("datosImagenesTotalNodos.dat")

    def getAllDataInOneFile(self, name_of_file):
        
        def changeColor(pixel_from_image: tuple, Green: int, Orange: int, Red: int, Brown: int):
            b, g, r, alpha = pixel_from_image
            newPixel = 0
            if (r,g,b) in VERDES_set:
                newPixel = Green  
            elif (r,g,b) in NARANJOS_set:
                newPixel = Orange
            elif (r,g,b) in MORADOS_set:
                newPixel = Brown
            elif (r,g,b) in ROJOS_set:
                newPixel = Red
            
            return newPixel

        def obtener_matrices_rojo(directorio):
            matrices_rojo = {}
            
            # Recorrer todas las imágenes en el directorio
            n = 0
            for filename in os.listdir(directorio):
                if filename.endswith(".png"):
                    path = os.path.join(directorio, filename)
                    
                    # Leer la imagen y obtener la matriz de píxeles rojos
                    imagen = Image.open(path)
                    matriz_rojo = obtener_matriz_rojo(imagen)
                    
                    # Agregar la matriz al diccionario
                    matrices_rojo[filename] = matriz_rojo
                print(n)
                n += 1
                
            return matrices_rojo

        def obtener_matriz_rojo(imagen):
            matriz_pixeles = imagen.load()
            ancho, alto = imagen.size
            matriz_rojo = []
            
            for y in range(alto):
                fila_rojo = []
                for x in range(ancho):
                    pixel = matriz_pixeles[x, y]
                    
                    rojo = changeColor(pixel, 63, 127, 191, 255)
                    fila_rojo.append(rojo)
                
                matriz_rojo.append(fila_rojo)
            
            return matriz_rojo

        def guardar_diccionario_txt(diccionario, archivo):
            with open(archivo, 'w') as file:
                for key, value in diccionario.items():
                    file.write(f"{key}: {value}\n")

        def guardar_diccionario_csv(diccionario, archivo):
            with open(archivo, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Imagen', 'Matriz Rojo'])
                for key, value in diccionario.items():
                    writer.writerow([key, value])
        
        # Directorio de las imágenes
        directorio_imagenes = self.path_dir_screenshots

        # Obtener las matrices de píxeles rojos
        matrices_rojo = obtener_matrices_rojo(directorio_imagenes)

        # Guardar el diccionario en un archivo de texto (.txt)
        archivo_txt = str(name_of_file)+".txt"
        guardar_diccionario_txt(matrices_rojo, archivo_txt)

        # Guardar el diccionario en un archivo CSV (.csv)
        archivo_csv = str(name_of_file)+".csv"
        guardar_diccionario_csv(matrices_rojo, archivo_csv)

    def getAllDataInOneFile2(self, name_of_file):
        
        def changeColor(pixel_from_image: tuple, Green: int, Orange: int, Red: int, Brown: int):
            b, g, r, alpha = pixel_from_image
            newPixel = 0
            if (r,g,b) in VERDES_set:
                newPixel = Green  
            elif (r,g,b) in NARANJOS_set:
                newPixel = Orange
            elif (r,g,b) in MORADOS_set:
                newPixel = Brown
            elif (r,g,b) in ROJOS_set:
                newPixel = Red
            
            return newPixel

        def obtener_matrices_rojo(directorio, archivo_hdf5):
            with pd.HDFStore(archivo_hdf5, mode='w') as store:
                # Recorrer todas las imágenes en el directorio
                for filename in os.listdir(directorio):
                    if filename.endswith(".png"):
                        path = os.path.join(directorio, filename)
                        
                        # Leer la imagen y obtener la matriz de píxeles rojos
                        imagen = Image.open(path)
                        matriz_rojo = obtener_matriz_rojo(imagen)
                        
                        # Guardar la matriz en el archivo HDF5
                        store.put(filename, pd.DataFrame(matriz_rojo))
            
        def obtener_matriz_rojo(imagen):
            matriz_pixeles = np.array(imagen)
            matriz_rojo = matriz_pixeles[:, :, 0]  # Canal rojo
            
            # Tamaño de la matriz
            filas, columnas = matriz_rojo.shape

            # Definir los valores de los colores
            Green = 63
            Orange = 127
            Red = 191
            Brown = 255

            # Iterar sobre los píxeles y aplicar la función changeColor
            for i in range(filas):
                for j in range(columnas):
                    pixel = matriz_pixeles[i, j]
                    matriz_rojo[i, j] = changeColor(pixel, Green, Orange, Red, Brown)

            return matriz_rojo
                
        # Directorio de las imágenes
        directorio_imagenes = self.path_dir_screenshots

                # Archivo HDF5 para guardar los datos
        archivo_hdf5 = str(name_of_file)+".h5"

        # Obtener y guardar las matrices de píxeles rojos
        obtener_matrices_rojo(directorio_imagenes, archivo_hdf5)

    def getSumOfColorsInFileFromHDF5(self, name_of_file_to_save, file_name_hdf5):
        # Crear un DataFrame vacío para almacenar los resultados
        df_frecuencias = pd.DataFrame(columns=['nombre', '63', '127', '191', '255'])
        
        with pd.HDFStore(file_name_hdf5, mode='r') as store:
            # Obtener la lista de claves (nombres de las imágenes)
            nombres = store.keys()
            coordenadas = self.position_of_vertices.items()
            

            for nombre in nombres:
                datos = store[nombre]
                # Contar la frecuencia de los valores
                frecuencias = datos.stack().value_counts()
            
                nombre_sin_png = nombre.replace(".png", "")

                # Crear una fila con los resultados
                fila_resultado = pd.Series([nombre_sin_png, frecuencias.get(63, 0), frecuencias.get(127, 0), frecuencias.get(191, 0), frecuencias.get(255, 0)],
                                           index=['nombre', '63', '127', '191', '255'])
                # Agregar la fila al DataFrame de frecuencias
                df_frecuencias = df_frecuencias._append(fila_resultado, ignore_index=True)

        # Guardar el DataFrame en un archivo CSV
        print(df_frecuencias)
        df_frecuencias.to_csv(str(name_of_file_to_save) + '.csv', index=False)

class DataImagesForEdges:

    def __init__(self, path_dir_screenshots:str, path_dir_network_data: str):

        self.image_no_traffic = plt.imread(path_dir_screenshots + "/2023-03-29_07-30.png") #Imagen temp/screenTest/2023-03-29_07-30.png
        self.path_dir_screenshots = str(path_dir_screenshots)

        position_of_vertices = eval(open(str(path_dir_network_data)+"/Posiciones.dat", "r").readline())
        self.position_of_vertices = {} #Posiciones
  
        for i, tupla in enumerate(position_of_vertices):
            self.position_of_vertices[i] = list([tupla[0]*self.image_no_traffic.shape[1], tupla[1]*self.image_no_traffic.shape[0]])
        
        self.conections = eval(open(str(path_dir_network_data)+"/Conexiones.dat", "r").readline())

        self.lanes = eval(open(str(path_dir_network_data)+"/Carriles.dat", "r").readline())
  

    def dataEdgesAllImagesToDataFrame(self, path_all_data_matrix_images, steps, type_data_steps = "mean_and_max", Radio = 0):
        
        def coordenadas_intermedias(coord1, coord2, steps):
            intermedios = []
            coord1[0] = round(coord1[0])
            coord1[1] = round(coord1[1])
            coord2[0] = round(coord2[0])
            coord2[1] = round(coord2[1])

            step_x = (coord2[0] - coord1[0]) / (steps + 1)
            step_y = (coord2[1] - coord1[1]) / (steps + 1)

            for i in range(0, steps + 1):
                intermedio_x = int(coord1[0] + i * step_x)
                intermedio_y = int(coord1[1] + i * step_y)
                intermedios.append((intermedio_x, intermedio_y))
            
            intermedios.append((int(coord2[0]), int(coord2[1])))                               
            return intermedios
        
        def obtener_datos(matriz, posiciones):
            datos = []
            for posicion in posiciones:
                fila, columna = posicion
                for i in range(-Radio, Radio+1):
                    for j in range(-Radio, Radio+1):
                        dato = matriz[fila+i][columna+j]
                        if dato != 0:
                            datos.append(dato)
                if not datos:
                    datos.append(0)
            return datos
        
        def get_largo_camino(coord1, coord2):
            x1, y1 = coord1
            x2, y2 =  coord2
            distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return distancia
        
        Datos = pd.DataFrame()
        
        with pd.HDFStore(path_all_data_matrix_images, mode='r') as store:
            nombres = store.keys()
            conexiones = self.conections
            posiciones = self.position_of_vertices
            carriles = self.lanes
            Datos["conection"] = conexiones
            Datos["lanes"] = carriles
            coordenadas_entre_conexiones = []
            distacias_entre_nodos = []

            for conexion in conexiones:
                coordenadas_entre_conexiones.append((posiciones[conexion[0]], posiciones[conexion[1]]))
                distacias_entre_nodos.append(get_largo_camino(posiciones[conexion[0]], posiciones[conexion[1]]))
            
            Datos["Largo"] = distacias_entre_nodos
            columns_data_mean = {}
            columns_data_max = {}

            for index, fecha in enumerate(nombres):
                print(index)
                colors_steps = []

                for conexion in coordenadas_entre_conexiones:
                    inter_steps_in_conexions = coordenadas_intermedias(conexion[0], conexion[1], steps)
                    color_in_steps = np.array(obtener_datos(store[fecha], inter_steps_in_conexions), dtype=np.uint8)
                    colors_steps.append(color_in_steps)
                
                if type_data_steps == "mean_and_max":
                    columns_data_mean[fecha] = [mean(lista) for lista in colors_steps]
                    columns_data_max[fecha] = [max(lista) for lista in colors_steps]

                elif type_data_steps == "all":
                    columns_data_mean[fecha] = colors_steps

            if type_data_steps == "mean_and_max":
                Datos_mean = pd.concat([Datos, pd.DataFrame(columns_data_mean)], axis=1)
                Datos_max = pd.concat([Datos, pd.DataFrame(columns_data_max)], axis=1)
                return Datos_mean, Datos_max
            
            elif type_data_steps == "all":
                Datos = pd.concat([Datos, pd.DataFrame(columns_data_mean)], axis=1)
                return Datos
        
    def makeDataFrame(self, dict_to_column: dict, column_name:str, index_name:str = "Nodo"):

        dict_to_column = {indice:tupla for indice, tupla in enumerate(dict_to_column)}
        keys_of_dict = dict_to_column.keys()
        ordered_values = list(dict_to_column.values())
        
        self.PromEdgedataFrame = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        self.IntEdgedataFrame = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        self.MaxEdgedataFrame = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        self.PromEdgedataFrame.set_index(str(index_name), inplace=True)
        self.IntEdgedataFrame.set_index(str(index_name), inplace=True)
        self.MaxEdgedataFrame.set_index(str(index_name), inplace=True)

    def promedio_integral_and_max_en_imagen(self, ruta_imagen, steps):

        def promedio_integral_and_max_pixeles_en_arista(self, coord1, coord2, ruta_imagen, steps):
            
            def coordenadas_intermedias(x1, y1, x2, y2, steps):
                intermedios = []
                step_x = (x2 - x1) / (steps + 1)
                step_y = (y2 - y1) / (steps + 1)

                for i in range(1, steps + 1):
                    intermedio_x = int(x1 + i * step_x)
                    intermedio_y = int(y1 + i * step_y)
                    intermedios.append((intermedio_x, intermedio_y))
                
                return intermedios
            
            def getPixelFromPath(ruta_imagen, x, y):
                # Cargar la imagen
                imagen = Image.open(ruta_imagen)
                # Obtener el valor del píxel en las coordenadas dadas
                valor_pixel = imagen.load()[x, y]

                return valor_pixel

            def changeColor(pixel_from_image: tuple, Green: int, Orange: int, Red: int, Brown: int):
                b, g, r, alpha = pixel_from_image
                newPixel = 0
                
                if (r,g,b) in VERDES_set:
                    newPixel = Green  
                
                elif (r,g,b) in NARANJOS_set:
                    newPixel = Orange
                
                elif (r,g,b) in MORADOS_set:
                    newPixel = Brown
                
                elif (r,g,b) in ROJOS_set:
                    newPixel = Red
                
                return newPixel
            
            total_coordenadas = coordenadas_intermedias(coord1[0], coord1[1], coord2[0], coord2[1], steps)
            pixel_one_line = []
            
            for coordenada in total_coordenadas:
                x, y = coordenada[0], coordenada[1]
                pixel_one_line.append(changeColor(getPixelFromPath(ruta_imagen, x, y),0,  85, 170, 255))
            
            promedio = st.mean(pixel_one_line)
            maximo = max(pixel_one_line)
            integral = sum(pixel_one_line)
            
            return promedio,integral, maximo

        Posiciones = self.position_of_vertices
        Conexiones = self.conections
        conexiones_in_coordendas = []
        
        for conexion in Conexiones:
            conexiones_in_coordendas.append((Posiciones[conexion[0]], Posiciones[conexion[1]]))
        
        promedios = dict()
        integrales = dict()
        maximos = dict()
        
        for index, conexion in enumerate(conexiones_in_coordendas):
            coord1 = conexion[0]
            coord2 = conexion[1]
            prom, integral, maximo = self.promedio_integral_and_max_pixeles_en_arista(coord1, coord2, ruta_imagen, steps)
            promedios[index] = prom
            integrales[index] = integral
            maximos[index] = maximo

        return promedios, integrales, maximos

    def addTrafficColorToDataFrame(self):
        "Es como la función principal, al usarla añade todas las columnas de datos al dataframe"
            
        def addColumnToDataFrame(self, dict_to_add: dict , column_name:str):
   
            keys_of_dict = dict_to_add.keys()
            ordered_values = list(dict_to_add.values())
            df_to_add = pd.DataFrame({"Nodo": keys_of_dict, str(column_name) : ordered_values})
            df_to_add.set_index('Nodo', inplace=True)
            self.PromEdgedataFrame = pd.concat([self.PromEdgedataFrame, df_to_add], axis = 1)

        files = os.listdir(self.path_dir_screenshots)
        N_files_in_dir = len(files)
        count = 0

        for archivo in files:
            namefile = os.path.join(self.path_dir_screenshots, archivo)
            prom, integral, max = self.promedio_integral_and_max_en_imagen(namefile, 10)
            self.addColumnToDataFrame(prom, archivo)
            count += 1
            self.saveDataFrame()
            print(f"{count/N_files_in_dir*100:.1f}%") 

def obtenerDataFrameDetalladoNodos():
    PuntaArenasNodes = DataImagesForNodes("data/Images/screenshots","data/DataMakeNetwork/PuntaArenasDetallado")
    datos_de_imagenes = "data/DataImages/DataMatrixImages.h5"

    dataFrame = PuntaArenasNodes.addTrafficColorToDataFrameFromHDF5(datos_de_imagenes)

    dataFrame.to_csv("intersectionCoord_detallado.csv")    

def obtenerDataFrameDetalladoEdges():
    
    PuntaArenasEdges = DataImagesForEdges("data/Images/screenshots","data/DataMakeNetwork/PuntaArenasDetallado")
    datos_de_imagenes = "data/DataImages/DataMatrixImages.h5"

    Datos_mean, Datos_max = PuntaArenasEdges.dataEdgesAllImagesToDataFrame(datos_de_imagenes, steps=1, Radio=1)
    Datos_mean.to_csv("DataStreetDetR1S1_mean.csv")
    Datos_max.to_csv("DataStreetDetR1S1_max.csv")


def main():
    obtenerDataFrameDetalladoEdges()


if __name__ == '__main__':
    main()                  

"""
