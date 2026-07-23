import pandas as pd
import numpy as np
import math
from statistics import mean 
import os 
import 
class DataImages:

    def __init__(self, path_dir_screenshots:str, path_dir_network_data: str):
            """
            Para crear un PromEdgedataFrame que tenga los datos de las imagenes obtenidas de Google.

            Args:
                path_dir_screenshots:str = directorio donde se encuentran las imagenes de Google
                path_dir_network_data: str = directorio donde se encuentran los datos de coordenadas de la red.
            """

            self.image_no_traffic = plt.imread(path_dir_screenshots + "/2023-03-29_07-30.png") #Imagen temp/screenTest/2023-03-29_07-30.png
            self.path_dir_screenshots = str(path_dir_screenshots)

            position_of_vertices = eval(open(str(path_dir_network_data)+"/Posiciones.dat", "r").readline())
            self.position_of_vertices = {} #Posiciones
    
            for i, tupla in enumerate(position_of_vertices):
                self.position_of_vertices[i] = list([tupla[0]*self.image_no_traffic.shape[1], tupla[1]*self.image_no_traffic.shape[0]])
            
            self.conections = eval(open(str(path_dir_network_data)+"/Conexiones.dat", "r").readline())

            self.lanes = eval(open(str(path_dir_network_data)+"/Carriles.dat", "r").readline())

    def dataEdgesAllImagesToDataFrame(self, path_all_data_matrix_images, steps=0, type_data_steps = "mean_and_max", Radio = 0):
            
        def coordenadas_intermedias(coord1, coord2, steps):
            coordenadas_intermedias = []
            coord1[0] = round(coord1[0])
            coord1[1] = round(coord1[1])
            coord2[0] = round(coord2[0])
            coord2[1] = round(coord2[1])

            step_x = (coord2[0] - coord1[0]) / (steps + 1)
            step_y = (coord2[1] - coord1[1]) / (steps + 1)

            for i in range(0, steps + 1):
                intermedio_x = int(coord1[0] + i * step_x)
                intermedio_y = int(coord1[1] + i * step_y)
                coordenadas_intermedias.append((intermedio_x, intermedio_y))
            
            coordenadas_intermedias.append((int(coord2[0]), int(coord2[1])))                               
            return coordenadas_intermedias

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

        # Recorrer todos los archivos en el directorio
        for filename in os.listdir(path_all_data_matrix_images):
            if filename.endswith(".txt"):
                path = os.path.join(path_all_data_matrix_images, filename)
                
                # Leer el archivo de texto y convertirlo en una matriz
                matriz = np.loadtxt(path)
                print()
        
        
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