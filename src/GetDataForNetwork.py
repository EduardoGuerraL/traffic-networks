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

        self.img_without_traffic = plt.imread("data/Images/screenshots/CleanScreenshot.png") #Imagen Google

        # Se le entregan los datos que construimos en NetworkCreator.py
        pos_vertices = eval(open(str(path_dir_network_data)+"/Posiciones.dat", "r").readline())
        self.position_of_vertices = {}
        # Redimensionando al tamaño de la imagen(antes estaba en fracciones de imagen)
        for i, tupla in enumerate(pos_vertices):
            self.position_of_vertices[i] = list([tupla[0]*self.img_without_traffic.shape[1], tupla[1]*self.img_without_traffic.shape[0]])        
        
        self.Edges = eval(open(str(path_dir_network_data)+"/Conexiones.dat", "r").readline()) #Conexiones
        
        # Creando redes en networkx
        
        # Interceccion de calles como nodos 
        self.DiGraphNodes = nx.DiGraph(self.Edges)
        self.GraphNodes = nx.Graph(self.Edges)
        
        # Calles como nodos.
        self.lanes = eval(open(str(path_dir_network_data)+"/Carriles.dat", "r").readline())#Carriles por calle

        #Obtenemos la lista de conecciones como si las calles fueran nodos:
        dict_Edges =  dict(enumerate(self.Edges))
        self.StreetsNodes = []
        for i in range(len(dict_Edges)):
            for j in range(len(dict_Edges)):
                if (dict_Edges[i][1]) == dict_Edges[j][0] and j!=i:
                    self.StreetsNodes.append((i,j))
        
        self.DiGraphEdges = nx.DiGraph(self.StreetsNodes)
        self.GraphEdges = nx.Graph(self.StreetsNodes)
    
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
        dataFrame = pd.DataFrame({str(index_name): keys_of_dict, str(column_name) : ordered_values})
        dataFrame.set_index(str(index_name), inplace=True)
        
        return dataFrame
    
    def addColumnToDataFrame(self, df, dict_to_add: dict , column_name:str, index_name:str = "Nodo"):
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
        df_to_add = pd.DataFrame({index_name: keys_of_dict, str(column_name) : ordered_values})
        df_to_add.set_index(index_name, inplace=True)
        dataFrame = pd.concat([df, df_to_add], axis = 1)

        return dataFrame
    
    #VER LUEGO
    def getBasicIndexCentrality(self):
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

    def getBasicIndexCentralityForEdges(self):
        """
        Suponiendo los nodos como las calles:
        Incluimos en un dataFrame los siguientes datos para cada nodo de la red:
            -Betwenness centrality
            -Closeness centrality
            -Degree centrality
        """

        #Orden de conexiones que tiene el dataFrame, el cual debemos seguir
        import ast
    
        dict_Edges = dict(enumerate(self.Edges))

        EdgeBetwenness = nx.betweenness_centrality(self.DiGraphEdges)
        EdgeBetwenness = {clave: valor for clave, valor in EdgeBetwenness.items()}
        EdgeBetwenness = {self.Edges[i]:valor for i, valor in EdgeBetwenness.items()}
        EdgeBetwenness = {index : EdgeBetwenness[clave] for index, clave in enumerate(self.Edges)}
        
        EdgesCloseness = nx.closeness_centrality(self.DiGraphEdges)
        EdgesCloseness = {clave: valor for clave, valor in EdgesCloseness.items()}
        EdgesCloseness = {self.Edges[i]:valor for i, valor in EdgesCloseness.items()}
        EdgesCloseness = {index : EdgesCloseness[clave] for index, clave in enumerate(self.Edges)}

        EdgesDegree = nx.degree_centrality(self.DiGraphEdges)
        EdgesDegree = {clave: valor for clave, valor in EdgesDegree.items()}
        EdgesDegree = {self.Edges[i]:valor for i, valor in EdgesDegree.items()}
        EdgesDegree = {index : EdgesDegree[clave] for index, clave in enumerate(self.Edges)}

        df = self.makeDataFrame(dict_Edges, "Conections")
        df = self.addColumnToDataFrame(df, EdgeBetwenness, "DiBC")
        df = self.addColumnToDataFrame(df, EdgesCloseness, "DiCC")
        df = self.addColumnToDataFrame(df, EdgesDegree, "DiDC")

        EdgeBetwenness = nx.betweenness_centrality(self.GraphEdges)
        EdgeBetwenness = {clave: valor for clave, valor in EdgeBetwenness.items()}
        EdgeBetwenness = {self.Edges[i]:valor for i, valor in EdgeBetwenness.items()}
        EdgeBetwenness = {index : EdgeBetwenness[clave] for index, clave in enumerate(self.Edges)}
        
        EdgesCloseness = nx.closeness_centrality(self.GraphEdges)
        EdgesCloseness = {clave: valor for clave, valor in EdgesCloseness.items()}
        EdgesCloseness = {self.Edges[i]:valor for i, valor in EdgesCloseness.items()}
        EdgesCloseness = {index : EdgesCloseness[clave] for index, clave in enumerate(self.Edges)}

        EdgesDegree = nx.degree_centrality(self.GraphEdges)
        EdgesDegree = {clave: valor for clave, valor in EdgesDegree.items()}
        EdgesDegree = {self.Edges[i]:valor for i, valor in EdgesDegree.items()}
        EdgesDegree = {index : EdgesDegree[clave] for index, clave in enumerate(self.Edges)}

        df = self.addColumnToDataFrame(df, EdgeBetwenness, "BC")
        df = self.addColumnToDataFrame(df, EdgesCloseness, "CC")
        df = self.addColumnToDataFrame(df, EdgesDegree, "DC")

        return df

    # Para mostrar los indices:
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
        ax.imshow(self.img_without_traffic)

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
        Adjacency_matrix = np.array(nx.adjacency_matrix(self.DiGraphEdges, nodelist=sorted(self.DiGraphEdges.nodes())).todense())
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
        Adjacency_matrix = np.array(nx.adjacency_matrix(self.DiGraphEdges, nodelist=sorted(self.DiGraphEdges.nodes())).todense())

        largo_de_calles = long_of_streets(new_position_of_vertices, dict_Edges)
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
        largo_de_calles = long_of_streets(new_position_of_vertices, dict_Edges)
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
    
    path_network_info = "data/DataMakeNetwork/PuntaArenasDetallado"
    PuntaArenasDetallado = NetworkData(path_network_info)
    df = PuntaArenasDetallado.getBasicIndexCentralityForEdges()
    print(df)
    df.to_csv("Detallado_IndicesCentralidad.csv")
    path_network_info = "data/DataMakeNetwork/PuntaArenas"
    PuntaArenas = NetworkData(path_network_info)
    df = PuntaArenas.getBasicIndexCentralityForEdges()
    print(df)
    df.to_csv("Simple_IndicesCentralidad.csv")
