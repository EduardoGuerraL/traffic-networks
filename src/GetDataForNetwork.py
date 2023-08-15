import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from Funciones.Colores import VERDES, NARANJOS, ROJOS, MORADOS
import math
import random

# convertir los conjuntos en diccionarios
VERDES_dict = {t: 1 for t in VERDES}
NARANJOS_dict = {t: 2 for t in NARANJOS}
MORADOS_dict = {t: 4 for t in MORADOS}
ROJOS_dict = {t: 3 for t in ROJOS}

class NetworkData:
    def __init__(self, path_dir_network_data: str):
        """
        Crear el conjunto de datos de la red.

        Args:
            path_dir_network_data (str): Donde se encuentran los datos de posicion y coneccion de la red.
        """

        self.image_no_traffic = plt.imread("data/Images/screenshots/CleanScreenshot.png") #Imagen

            # INTERSECCIONES COMO NODOS
        # Atributos de armado de red.
        position_of_vertices = eval(open(str(path_dir_network_data)+"/Posiciones.dat", "r").readline())
        self.position_of_vertices = {} #Posiciones
        for i, tupla in enumerate(position_of_vertices):
            self.position_of_vertices[i] = list([tupla[0]*self.image_no_traffic.shape[1], tupla[1]*self.image_no_traffic.shape[0]])        
        self.conections = eval(open(str(path_dir_network_data)+"/Conexiones.dat", "r").readline()) #Conexiones
        self.lanes = eval(open(str(path_dir_network_data)+"/Carriles.dat", "r").readline())#Carriles por calle
        self.dataFrame = pd.DataFrame()
        self.DiGraph = nx.DiGraph(self.conections)
        self.conections_diconected = []
        [self.conections_diconected.append(x) for x in self.conections if x not in self.conections_diconected] #Conexiones_bidireccionadas
        self.Graph = nx.Graph(self.conections_diconected)
        
            # CALLES COMO NODOS
        self.dataFrameForEdges = pd.DataFrame()
        #Obtenemos la lista de conecciones como si las calles fueran nodos:
        self.dict_from_conections_dataFrame =  dict(enumerate(self.conections))
        self.Conection_between_streets = []
        for i in range(len(self.dict_from_conections_dataFrame)):
            for j in range(len(self.dict_from_conections_dataFrame)):
                if (self.dict_from_conections_dataFrame[i][1]) == self.dict_from_conections_dataFrame[j][0] and j!=i:
                    self.Conection_between_streets.append((i,j))
        self.Graph_of_conection_between_streets = nx.DiGraph(self.Conection_between_streets)

    def makeDataFrame(self, dict_to_column: dict, column_name:str, index_name:str = "Nodo"):
        """
        Crea un DataFrame de Pandas con el diccionario que se le entrega.

        Args: 
            dict_to_column(dict): Diccionario con el dato de la Red que queremos guardar.
            column_name(str): Nombre del dato que estamos guardando.
            index_name(str): Nombre por el cual se le llama al indice de 0 a N.
        
        Return:
            DataFrame de Pandas con una columna de datos.
        """

        keys_of_dict = sorted(dict_to_column.keys())
        ordered_values = [dict_to_column[key] for key in keys_of_dict]
        self.dataFrame = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        self.dataFrame.set_index(str(index_name), inplace=True)

    def makeDataFrameEdge(self, dict_to_column: dict, column_name:str, index_name:str = "Nodo"):
        """
        Crea un DataFrame de Pandas con el diccionario que se le entrega.

        Args: 
            dict_to_column(dict): Diccionario con el dato de la Red que queremos guardar.
            column_name(str): Nombre del dato que estamos guardando.
            index_name(str): Nombre por el cual se le llama al indice de 0 a N.
        
        Return:
            DataFrame de Pandas con una columna de datos.
        """

        keys_of_dict = sorted(dict_to_column.keys())
        ordered_values = [dict_to_column[key] for key in keys_of_dict]
        self.dataFrameForEdges = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        self.dataFrameForEdges.set_index(str(index_name), inplace=True)

    def addColumnToDataFrame(self, dict_to_add: dict , column_name:str):
        """
        Agrega una columna al dataFrame.

        Args:
            dataFrame: DataFrame al que agregamos los datos
            dict_to_add(dict): Datos en forma de diccionario que agregaremos.
            column_name(str): Nombre de los datos.
        Return:
            DataFrame modificado.
        """
        keys_of_dict = sorted(dict_to_add.keys())
        ordered_values = [dict_to_add[key] for key in keys_of_dict]
        df_to_add = pd.DataFrame({"Nodo": keys_of_dict, str(column_name) : ordered_values})
        df_to_add.set_index('Nodo', inplace=True)
        self.dataFrame = pd.concat([self.dataFrame, df_to_add], axis = 1)

    def addColumnToDataFrameEdge(self, dict_to_add: dict , column_name:str):
        """
        Agrega una columna al dataFrame.

        Args:
            dataFrame: DataFrame al que agregamos los datos
            dict_to_add(dict): Datos en forma de diccionario que agregaremos.
            column_name(str): Nombre de los datos.
        Return:
            DataFrame modificado.
        """
        keys_of_dict = sorted(dict_to_add.keys())
        ordered_values = [dict_to_add[key] for key in keys_of_dict]
        df_to_add = pd.DataFrame({"Nodo": keys_of_dict, str(column_name) : ordered_values})
        df_to_add.set_index('Nodo', inplace=True)
        self.dataFrameForEdges = pd.concat([self.dataFrameForEdges, df_to_add], axis = 1)

    def addBasicIndexCentrality(self):
        """
        Agrega los indices de centralidad basicos:
        "BC, CC, DC, DiBC, DiCC, DiDC"
        """
        #Indices basicos para agregar al dataFrame
        BC = nx.betweenness_centrality(self.Graph)
        CC = nx.closeness_centrality(self.Graph)
        DC = nx.degree_centrality(self.Graph)
        DiBC = nx.betweenness_centrality(self.DiGraph)
        DiCC = nx.closeness_centrality(self.DiGraph)
        DiDC = nx.degree_centrality(self.DiGraph)

        self.makeDataFrame(BC, "BC")
        self.addColumnToDataFrame(CC, "CC")
        self.addColumnToDataFrame(DC, "DC")
        self.addColumnToDataFrame(DiBC, "DiBC")
        self.addColumnToDataFrame(DiCC, "DiCC")
        self.addColumnToDataFrame(DiDC, "DiDC")

    def plotNodes(self, column_name:str, name_to_save_file: str = None, width_node:float = 2):
        """
        Crea, guarda y muestra los indices que queremos ver(que esten en el dataFrame) en la ciudad.

        Args: 
            column_name(str): Nombre de la columna del dataFrame que queremos ver.  
            name_to_save_file(str) = None:  En caso de querer guardar la imagen poner el nombre
            width_node(float) = 2: diametro de los nodos.
        Return:
            Se muestra la imagen o se guarda.
        """

        fig, ax = plt.subplots()
        ax.imshow(self.image_no_traffic)

        #Indice que graficaremos
        indice = list(self.dataFrame[str(column_name)])
        indices_ordenado = [indice[i] for i in self.Graph.nodes()]

        #grafica para direccionados
        if "Di" in column_name:
            
            nx.draw_networkx_edges(self.DiGraph, self.position_of_vertices, width= 0.3 , arrowsize=5, node_size=15)
            nodes=nx.draw_networkx_nodes(self.DiGraph, self.position_of_vertices, node_size= width_node, node_color=indices_ordenado, cmap= plt.cm.Reds)
            plt.axis('off')
                
        #grafica para no direccionados
        elif "Di" not in column_name:
            nx.draw_networkx_edges(self.Graph, self.position_of_vertices, width= 0.3, node_size=15)
            nodes=nx.draw_networkx_nodes(self.Graph, self.position_of_vertices, node_size= width_node, node_color=indices_ordenado, cmap= plt.cm.Reds)

        plt.axis('off')
        cbar = plt.colorbar(nodes, label = str(column_name),shrink=0.9, aspect=30, pad = 0.01)

        if name_to_save_file is not None:
            plt.savefig("results/"+str(name_to_save_file), bbox_inches='tight',pad_inches = 0, dpi = 500)
        else:
            plt.show()

    def ehrenfestAnalitic(self):
        
        Adjacency_matrix = np.array(nx.adjacency_matrix(self.Graph, nodelist=sorted(self.DiGraph.nodes())).todense())
        
        Matrix_B = (Adjacency_matrix.T/np.sum(Adjacency_matrix.transpose(), axis=0)) - np.identity(len(Adjacency_matrix))
        autovalores, autovectores = np.linalg.eig(Matrix_B)
        
        indice = next((i for i, valor in enumerate(autovalores) if abs(valor) < 1e-15), 0)
        Probabilidad = [round(i/sum(autovectores[:, indice]), 5) for i in autovectores[:, indice]]
        Probabilidad = {indice: valor for indice, valor in enumerate(Probabilidad)}
        
        return Probabilidad
    
    def getDesviacionStdwithN(self, N):
        Probabilidad = []
        Desviaciones_estandar = [math.sqrt(N * (p - p**2)) for p in Probabilidad]

    def eherenfestSimulation(self, N_particulas,Tiempo):
        Adjacency_matrix = np.array(nx.adjacency_matrix(self.Graph_of_conection_between_streets, nodelist=sorted(self.Graph_of_conection_between_streets.nodes())).todense())
        return Adjacency_matrix
        
        """
        #Numero de particulas que tiene cada nodo a tiempo inicial
        #NP_NODOS = np.random.multinomial(N_particulas,[1/len(Adjacency_matrix)]*len(Adjacency_matrix),size = 1)[0] #Nodos al azar
        NP_NODOS = np.zeros(len(Adjacency_matrix))
        NP_NODOS[2] = N_particulas

        for t in range(Tiempo):
            x = np.random.randint(len(NP_NODOS))
            if NP_NODOS[x] >= 1:
                indices = [i for i, dat in enumerate(Adjacency_matrix[x, :]) if dat == 1]
                
                #Elegimos uno de los indices:
                elejido = np.random.choice(indices)
                
                #cambiamos la pelotita
                NP_NODOS[x] -=1
                NP_NODOS[elejido] +=1
            else:
                continue
            pass
        
        print(NP_NODOS)
        """

    def addBasicIndexCentralityForEdges(self):
        """
        Incluimos en un dataFrame los diguientes datos para cada nodo de la red:
            -Edge Betwenness centrality (función que viene en nx)
            -Betwenness centrality**
            -Closeness centrality**
            -Degree centrality**
        **Los ultimos 3 son para nodos, pero habiendo dado como nodo a las calles.
        """
        def son_listas_de_tuplas_iguales(lista1, lista2):
            if len(lista1) != len(lista2):
                return False
            
            for tupla in lista1:
                if tupla not in lista2:
                    return False
            
            for tupla in lista2:
                if tupla not in lista1:
                    return False
            
            return True
        #Orden de conexiones que tiene el dataFrame, el cual debemos seguir
        import ast
    
    
        orden_conecciones_en_dataFrame = self.conections
        dict_from_conections_dataFrame = dict(enumerate(self.conections))

        #Obtener EdgeBetwennes de la forma convencional
        GrafoWNormalConex = nx.DiGraph(orden_conecciones_en_dataFrame)
        EdgeBetwenness_convencional = nx.edge_betweenness_centrality(GrafoWNormalConex)
        EdgeBetwenness_convencional = {clave: round(valor, 5) for clave, valor in EdgeBetwenness_convencional.items()}
        EdgeBetwenness_convencional = {index : EdgeBetwenness_convencional[clave] for index, clave in enumerate(orden_conecciones_en_dataFrame)}


            #CENTRALIDAD CON FORMA NO CONVENCIONAL
        #Obtenemos la lista de conecciones como si las calles fueran nodos:
        Conection_between_streets = []
        for i in range(len(dict_from_conections_dataFrame)):
            for j in range(len(dict_from_conections_dataFrame)):
                if (dict_from_conections_dataFrame[i][1]) == dict_from_conections_dataFrame[j][0] and j!=i:
                    Conection_between_streets.append((i,j))
        #Calculo de los indices de centralidad:
        Graph_of_conection_between_streets = nx.DiGraph(Conection_between_streets)
        
        new_streets_Betwenness = nx.betweenness_centrality(Graph_of_conection_between_streets)
        new_streets_Betwenness = {clave: round(valor, 5) for clave, valor in new_streets_Betwenness.items()}
        new_streets_Betwenness = {orden_conecciones_en_dataFrame[i]:valor for i, valor in new_streets_Betwenness.items()}
        new_streets_Betwenness = {index : new_streets_Betwenness[clave] for index, clave in enumerate(orden_conecciones_en_dataFrame)}
        
        new_streets_Closeness = nx.closeness_centrality(Graph_of_conection_between_streets)
        new_streets_Closeness = {clave: round(valor, 5) for clave, valor in new_streets_Closeness.items()}
        new_streets_Closeness = {orden_conecciones_en_dataFrame[i]:valor for i, valor in new_streets_Closeness.items()}
        new_streets_Closeness = {index : new_streets_Closeness[clave] for index, clave in enumerate(orden_conecciones_en_dataFrame)}

        new_streets_Degree = nx.degree_centrality(Graph_of_conection_between_streets)
        new_streets_Degree = {clave: round(valor, 5) for clave, valor in new_streets_Degree.items()}
        new_streets_Degree = {orden_conecciones_en_dataFrame[i]:valor for i, valor in new_streets_Degree.items()}
        new_streets_Degree = {index : new_streets_Degree[clave] for index, clave in enumerate(orden_conecciones_en_dataFrame)}
        

        self.makeDataFrameEdge(dict_from_conections_dataFrame, "conecciones")
        self.addColumnToDataFrameEdge(EdgeBetwenness_convencional, "Betweenness_nx")
        self.addColumnToDataFrameEdge(new_streets_Betwenness, "Betweenness_streets")
        self.addColumnToDataFrameEdge(new_streets_Closeness, "Closeness_streets")
        self.addColumnToDataFrameEdge(new_streets_Degree, "Degree_streets")

    def ehrenfestSimulationWithBounded(self, cantidad_particulas, iteraciones, dataFrameLessOne = None):

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

        def simular_iteraciones(matriz_adyacencia, vector_tope):

            # Obtenemos la cantidad de nodos
            num_nodos = len(matriz_adyacencia)

            if dataFrameLessOne is None:
                # Creamos un vector para almacenar la cantidad de partículas en cada nodo
                vector_particulas = np.zeros(num_nodos).astype(int)

                # Distribuimos las partículas inicialmente de manera uniforme en los nodos
                contador = cantidad_particulas
                while contador > 0:
                    nodo_inicial = random.randint(0, num_nodos - 1)
                    if vector_particulas[nodo_inicial] < vector_tope[nodo_inicial]:
                        vector_particulas[nodo_inicial] += 1
                        contador -= 1

            elif dataFrameLessOne is not None:
                vector_particulas = np.array(dataFrameLessOne.iloc[:,-1]).astype(int)

            else:
                print("No se entregó la intrucción correcta al dar un archivo de la iteración anterior")
                
            
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
        
        # Obteniendo los datos para la simulación
        new_position_of_vertices = self.position_of_vertices
        Adjacency_matrix = np.array(nx.adjacency_matrix(self.Graph_of_conection_between_streets, nodelist=sorted(self.Graph_of_conection_between_streets.nodes())).todense())

        largo_de_calles = long_of_streets(new_position_of_vertices, self.dict_from_conections_dataFrame)
        cantidad_de_autos_por_calle = [round(largo*1.876) for largo in largo_de_calles]
        N_autos_por_calle_por_pistas = [i*j for i,j in zip(cantidad_de_autos_por_calle,self.lanes)]

        vector_final = simular_iteraciones(Adjacency_matrix, N_autos_por_calle_por_pistas)

        return vector_final

    def ehrenfestSimulationWithBounded_porcentual(self):
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

        new_position_of_vertices = self.position_of_vertices
        largo_de_calles = long_of_streets(new_position_of_vertices, self.dict_from_conections_dataFrame)
        cantidad_de_autos_por_calle = [round(largo*1.876) for largo in largo_de_calles]
        N_autos_por_calle_por_pistas = [i*j for i,j in zip(cantidad_de_autos_por_calle,self.lanes)]
     
        return N_autos_por_calle_por_pistas

def ehrenfest_sim(primero = True, iteraciones = 100, autos = 10000):
    
    datos = "data/DataMakeNetwork/PuntaArenasDetallado"
    PuntaArenasDetallado = NetworkData(datos)
    if primero is True:
        # Primera iteración
        dataframe = pd.DataFrame()
        simulation = PuntaArenasDetallado.ehrenfestSimulationWithBounded(autos, iteraciones)
        dataframe[str(iteraciones)] = simulation
        dataframe.index.name = "Calle"
        dataframe.to_csv("data/DataNetwork/Ehr_sim_10mAutos_det_pist.scv", index=True)
    
    elif primero is False:
        dataframe = pd.read_csv("data/DataNetwork/Ehr_sim_10mAutos_det_pist.scv")    
        columna_anterior = int(dataframe.columns[-1])
        simulation = PuntaArenasDetallado.ehrenfestSimulationWithBounded(autos, iteraciones, dataframe)
        dataframe[str(columna_anterior + iteraciones)] = simulation
        dataframe.to_csv("data/DataNetwork/Ehr_sim_10mAutos_det_pist.scv", index=False)

def graph(indice_i):
    df = pd.read_csv("estado_ejes_500M_10msteps.csv")
    # Seleccionar la columna del índice específico
    datos_indice = df.iloc[indice_i][1:]

    ## Graficar el avance en el tiempo del índice i
    plt.plot(datos_indice.index, datos_indice.values)
    plt.xlabel('tiempo')
    plt.ylabel('particulas')
    plt.title(f'Avance en el tiempo de la calle {indice_i}')
    # Configurar los marcadores y etiquetas del eje x
    intervalo = 1000  # Mostrar un marcador y etiqueta cada 1 elemento
    marcadores = plt.gca().get_xticks()[::intervalo]
    etiquetas = datos_indice.index[::intervalo]
    plt.xticks(marcadores, etiquetas, rotation=45)
    plt.show()

def ehrenfest_sim_percent():
    datos = "data/DataMakeNetwork/PuntaArenas"
    PuntaArenasDetallado = NetworkData(datos)
    porcentaje = PuntaArenasDetallado.ehrenfestSimulationWithBounded_porcentual()
    df = pd.DataFrame(porcentaje)
    df.to_csv("Max_ocupation_per_streets_simple.csv")

def network_dense():
    puntaarenas = NetworkData("data/DataMakeNetwork/PuntaArenas")
    puntaarenas.addBasicIndexCentralityForEdges()
    return puntaarenas.dataFrameForEdges

def getdfNodosNetworkBasics():
    puntaarenas = NetworkData("data/DataMakeNetwork/PuntaArenas")
    puntaarenas.addBasicIndexCentrality()
    return puntaarenas.dataFrame

def getdfNodosNetworkBasics_detallado():
    puntaarenas = NetworkData("data/DataMakeNetwork/PuntaArenasDetallado")
    puntaarenas.addBasicIndexCentrality()
    return puntaarenas.dataFrame

def getdfStreetsNetworkBasics():
    puntaarenas = NetworkData("data/DataMakeNetwork/PuntaArenas")
    puntaarenas.addBasicIndexCentralityForEdges()
    return puntaarenas.dataFrameForEdges

def getdfStreetsNetworkBasics_detallado():
    puntaarenas = NetworkData("data/DataMakeNetwork/PuntaArenasDetallado")
    puntaarenas.addBasicIndexCentralityForEdges()
    return puntaarenas.dataFrameForEdges

if __name__ == "__main__":
    
    ehrenfest_sim_percent()
    
    #ehrenfest_sim(primero=True, iteraciones=200)
    #for _ in range(2000):
     #  ehrenfest_sim(primero=False, iteraciones=1000)
    
    #for i in range(1,1200, 63):
     #   graph(i)
    
    #datos = "data/DataMakeNetwork/PuntaArenas"
    #puntaArenas = NetworkData(datos)

    #datos = puntaArenas.eherenfestSimulation(10,10)
    #np.savetxt("matriz_A_ejes.txt", datos)
    
    #puntaArenas.ehrenfestAnalitic()
    #data  = getdfStreetsNetworkBasics_detallado()
    #print(data)
    #data.to_csv("Basic_and_advaced_data_network_aristas_detallado.csv")