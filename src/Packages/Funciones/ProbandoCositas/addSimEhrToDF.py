import random
import numpy as np
import matplotlib.pyplot as plt
import math
import networkx as nx

def agregar_columna(lista, dataframe, nombre_columna):
    dataframe[nombre_columna] = lista
    return dataframe

def sacando_vector():
    def simular_iteraciones(matriz_adyacencia, vector_tope, cantidad_particulas, iteraciones):
        # Obtenemos la cantidad de nodos
        num_nodos = len(matriz_adyacencia)

        # Creamos un vector para almacenar la cantidad de partículas en cada nodo
        vector_particulas = np.zeros(num_nodos)

        # Distribuimos las partículas inicialmente de manera uniforme en los nodos
        contador = cantidad_particulas
        while contador > 0:
            nodo_inicial = random.randint(0, num_nodos - 1)
            if vector_particulas[nodo_inicial] < vector_tope[nodo_inicial]:
                vector_particulas[nodo_inicial] += 1
                contador -= 1
    
        # Realizamos las iteraciones
        for _ in range(iteraciones):
            # Elegimos una partícula al azar
            nodo_origen = random.randint(0, num_nodos - 1)
            particulas_origen = vector_particulas[nodo_origen]

            # Si hay partículas en el nodo de origen
            if particulas_origen > 0:
                # Elegimos un nodo destino aleatoriamente
                nodos_destino = np.where(matriz_adyacencia[nodo_origen]==1)[0]
                if len(nodos_destino) > 0:
                    nodo_destino = random.choice(nodos_destino)
                    #si el destino no está lleno
                    if vector_tope[nodo_destino] > vector_particulas[nodo_destino]:
                        # Movemos una partícula del nodo origen al nodo destino
                        vector_particulas[nodo_origen] -= 1
                        vector_particulas[nodo_destino] += 1

        return vector_particulas

    def long_of_streets(posicion_nodos, conection_btw_nodos):
        def calcular_distancia(coord1, coord2):
            x1, y1 = coord1
            x2, y2 = coord2
            distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return distancia

        lenghts = {}
        for index, conection in conection_btw_nodos.items():
            lenghts[index] = calcular_distancia(posicion_nodos[conection[0]], posicion_nodos[conection[1]])
        
        return list(lenghts.values())

    path_dir_network_data = "data/fromMakeNet/PuntaArenas2.pickle"
    image_no_traffic ="data/screenshots/2023-03-29_07-45.png"
    image_no_traffic = plt.imread(image_no_traffic)

    position_of_vertices = eval(open(str(path_dir_network_data)+"/Posiciones.dat", "r").readline())
    new_position_of_vertices = {} #Posiciones

    for i, tupla in enumerate(position_of_vertices):
        new_position_of_vertices[i] = list([tupla[0]*image_no_traffic.shape[1], tupla[1]*image_no_traffic.shape[0]])

    conections = eval(open(str(path_dir_network_data)+"/Conexiones.dat", "r").readline()) #Conexiones
    dict_from_conections_dataFrame =  dict(enumerate(conections))
    #Obtenemos la lista de conecciones como si las calles fueran nodos:
    Conection_between_streets = []
    for i in range(len(dict_from_conections_dataFrame)):
        for j in range(len(dict_from_conections_dataFrame)):
            if (dict_from_conections_dataFrame[i][1]) == dict_from_conections_dataFrame[j][0] and j!=i:
                Conection_between_streets.append((i,j))

    Graph_of_conection_between_streets = nx.DiGraph(Conection_between_streets)
    Adjacency_matrix = np.array(nx.adjacency_matrix(Graph_of_conection_between_streets, nodelist=sorted(Graph_of_conection_between_streets.nodes())).todense())



    topes = long_of_streets(new_position_of_vertices, dict_from_conections_dataFrame)
    topes = [round(tope/5) for tope in topes]
    vector_final = simular_iteraciones(Adjacency_matrix, topes, 10000, 1000000)

    return vector_final

hola = sacando_vector()
print(hola)
