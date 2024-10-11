import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from functions.Funciones.Colores import VERDES, NARANJOS, ROJOS, MORADOS
import statistics as st
import csv
import math
from statistics import mean 
from functions.basics import reescalar_lista_de_listas, obtener_nombres_con_H_M_sinFDS, plot_distribution

# convertir los conjuntos en sets
VERDES_set = set(VERDES)
NARANJOS_set = set(NARANJOS)
MORADOS_set = set(MORADOS)
ROJOS_set = set(ROJOS)    

import os
from PIL import Image


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
    
    def dataEdgesAllImagesToDataFrame(self, path_all_data_matrix_images, steps, type_data_steps = "mean", Radio = 0):
        
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

            for num, conexion in enumerate(conexiones):
                coordenadas_entre_conexiones.append((posiciones[conexion[0]], posiciones[conexion[1]]))
                distacias_entre_nodos.append(get_largo_camino(posiciones[conexion[0]], posiciones[conexion[1]]))
            
            Datos["Largo"] = distacias_entre_nodos
            columns_data_mean = {}
            for index, fecha in enumerate(nombres):
                print(index)
                colors_steps = []

                for num, conexion in enumerate(coordenadas_entre_conexiones):
                    inter_steps_in_conexions = coordenadas_intermedias(conexion[0], conexion[1], steps)
                    color_in_steps = np.array(obtener_datos(store[fecha], inter_steps_in_conexions), dtype=np.uint8)
                    colors_steps.append(color_in_steps)
                
                if type_data_steps == "mean":
                    columns_data_mean[fecha] = [mean(lista) for lista in colors_steps]

                elif type_data_steps == "all":
                    columns_data_mean[fecha] = colors_steps

            if type_data_steps == "mean":
                Datos_mean = pd.concat([Datos, pd.DataFrame(columns_data_mean)], axis=1)
                #Datos_max = pd.concat([Datos, pd.DataFrame(columns_data_max)], axis=1)
                return Datos_mean#, Datos_max
            
            elif type_data_steps == "all":
                Datos = pd.concat([Datos, pd.DataFrame(columns_data_mean)], axis=1)
                return Datos
        
        '''
        """
        Crea un DataFrame de Pandas con el diccionario que se le entrega.

        Args: 
            dict_to_column(dict): Diccionario con el dato de la Red que queremos guardar.
            column_name(str): Nombre del dato que estamos guardando.
            index_name(str): Nombre por el cual se le llama al indice de 0 a N.
        
        Return:
            DataFrame de Pandas con una columna de datos.
        """
        dict_to_column = {indice:tupla for indice, tupla in enumerate(dict_to_column)}
        keys_of_dict = dict_to_column.keys()
        ordered_values = list(dict_to_column.values())
        
        self.PromEdgedataFrame = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        self.IntEdgedataFrame = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        self.MaxEdgedataFrame = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        self.PromEdgedataFrame.set_index(str(index_name), inplace=True)
        self.IntEdgedataFrame.set_index(str(index_name), inplace=True)
        self.MaxEdgedataFrame.set_index(str(index_name), inplace=True)
        '''

#Para obtener los datos en las coordenadas de los ejes que entregamos
def obtenerDataFrameDetalladoEdges():
    
    PuntaArenasEdges = DataImages("data/Images/screenshots","data/DataMakeNetwork/PuntaArenas")
    datos_de_imagenes = "data/DataImages/DataMatrixImages.h5"

    DatosR = []
    for R in range(10):
        Datos_mean = PuntaArenasEdges.dataEdgesAllImagesToDataFrame(datos_de_imagenes, steps=1, Radio=R)
  
        columnas_elejidas = obtener_nombres_con_H_M_sinFDS(Datos_mean.columns, hora_exacta=(7, 0))
        data_observacional = Datos_mean[columnas_elejidas].values.tolist()
        
        ## Reescalando los data_observacional de 0 a 1
        data_observacional = reescalar_lista_de_listas(data_observacional, 255)
        data = [np.mean(data) for data in data_observacional]
        DatosR.append(data)
    
    return DatosR
                
def plot_scatter(data):
    """
    Grafica un scatter plot para cada lista en data en un mismo gráfico.

    Args:
        data (list of lists): Lista de listas, donde cada sublista contiene los valores a graficar.
    """
    for sublist in data:
        x = list(range(1, len(sublist) + 1))
        print(x)
        plt.scatter(x, sublist)

    plt.xlabel('Índice')
    plt.ylabel('Valor')
    plt.title('Scatter Plot de Listas')
    plt.legend([f'Lista {i+1}' for i in range(len(data))])
    plt.show()

def main():
    datos = obtenerDataFrameDetalladoEdges()
    plot_scatter(datos)

if __name__ == '__main__':
    main()