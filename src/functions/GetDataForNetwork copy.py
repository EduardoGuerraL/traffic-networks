import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import random

class NetworkData:
    def __init__(self, path_dir_network_data: str, path_img_without_traffic: str):
        """
        To extract information obout the network that you make in NetworkCreator.

        Args:
            path_dir_network_data (str): Path where you save nodes, conections and lanes of network.
            path_img_without_traffic (str): this is to plot above imgage. And to get dimenstions.
        """

        self.img_without_traffic = plt.imread(path_img_without_traffic) #Imagen Google

        ## Open the data from network Creator.
        # node_positions --> fraction_pos_intersections (fraction of img)
        # node_conections --> intersection_2_intersection
        # lanes --> street_lanes
        fraction_pos_intersections = eval(open(str(path_dir_network_data)+"/node_positions.dat", "r").readline())
        self.Edges = eval(open(str(path_dir_network_data)+"/node_conections.dat", "r").readline()) #Conexiones
        self.lanes = eval(open(str(path_dir_network_data)+"/lanes_of_link.dat", "r").readline())#Carriles por calle
        
        
        # Rezise position of intersections to img coordinates
        self.pos_intersections = {}
        for i, tupla in enumerate(fraction_pos_intersections):
            self.pos_intersections[i] = list([tupla[0]*self.img_without_traffic.shape[1], tupla[1]*self.img_without_traffic.shape[0]])        

        # Pass intersections to links and streets to nodes.
        dict_Edges =  dict(enumerate(self.Edges))
        self.StreetsNodes = []
        for i in range(len(dict_Edges)):
            for j in range(len(dict_Edges)):
                if (dict_Edges[i][1]) == dict_Edges[j][0] and j!=i:
                    self.StreetsNodes.append((i,j))

        ## Use Networkx to make network
        
        # Intersections To Nodes
        self.DiGraphNodes = nx.DiGraph(self.Edges)
        self.GraphNodes = nx.Graph(self.Edges)
        
        # Streets to Nodes
        self.DiGraphEdges = nx.DiGraph(self.StreetsNodes)
        self.GraphEdges = nx.Graph(self.StreetsNodes)
    
    #funciones de creación de datos basicos
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

    def getBasicIndexCentrality(self):
        """
        Agrega los indices de centralidad basicos:
        "BC, CC, DC, DiBC, DiCC, DiDC"
        """
        #Indices basicos para agregar al dataFrame
        BC = nx.betweenness_centrality(self.GraphNodes)
        CC = nx.closeness_centrality(self.GraphNodes)
        DC = nx.degree_centrality(self.GraphNodes)
        DiBC = nx.betweenness_centrality(self.DiGraphNodes)
        DiCC = nx.closeness_centrality(self.DiGraphNodes)
        DiDC = nx.degree_centrality(self.DiGraphNodes)

        df = self.makeDataFrame(BC, "BC")
        df = self.addColumnToDataFrame(df, CC, "CC")
        df = self.addColumnToDataFrame(df, DC, "DC")
        df = self.addColumnToDataFrame(df, DiBC, "DiBC")
        df = self.addColumnToDataFrame(df, DiCC, "DiCC")
        df = self.addColumnToDataFrame(df, DiDC, "DiDC")

        return df

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


    #Funciones de entrega de caracteristicas
    def getAdjacencyMatrix(self):
        Adjacency_matrix_edges = np.array(nx.adjacency_matrix(self.DiGraphEdges, nodelist=sorted(self.DiGraphEdges.nodes())).todense())
        Adjacency_matrix_nodes = np.array(nx.adjacency_matrix(self.DiGraphNodes, nodelist=sorted(self.DiGraphNodes.nodes())).todense())

        return Adjacency_matrix_nodes, Adjacency_matrix_edges

    def getMaxParticlesPerUrns(self, factor_escala = 1.876):
        """
        Para obtener factor escala necesitamos:
            M_R : Medida real de una calle
            M_V : Medida virtual de una calle
            M_A : Medida de un auto.
            \alpha : factor escala.

            \alpha = M_R/(M_V*M_A)
        
        Así obtenemos la cantidad de autos en la calle i como:

            N(i) = \alpha * M_v(i)
        
        Por hacer: que calcule el factor de escala dado M_A.
        """

        def long_of_streets(posicion_nodos, conection_btw_nodos):
            def calcular_distancia(coord1, coord2):
                x1, y1 = coord1
                x2, y2 = coord2
                distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                return distancia

            lenghts = {}
            print()
            for index, conection in enumerate(conection_btw_nodos):
                lenghts[conection] = calcular_distancia(posicion_nodos[list(conection)[0]], posicion_nodos[list(conection)[1]])
            
            return lenghts
        

        largo_de_calles = long_of_streets(self.pos_intersections, self.Edges)
        
        cantidad_de_autos_por_calle = {indice : round( largo * factor_escala ) for indice, largo in largo_de_calles.items()}

        return cantidad_de_autos_por_calle
    

    # Funciones de Visualización:
    def plotNodes(self, dataframe, column_name:str, directed:bool = True ,name_to_save_file: str = None, width_node:float = 2):
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
        indice = list(dataframe[str(column_name)])
        indices_ordenado = [indice[i] for i in self.DiGraphNodes.nodes()]

        #grafica para direccionados
        if directed is True:
            
            nx.draw_networkx_edges(self.DiGraphNodes, self.pos_intersections, width= 0.3 , arrowsize=5, node_size=15)
            nodes=nx.draw_networkx_nodes(self.DiGraphNodes, self.pos_intersections, node_size= width_node, node_color=indices_ordenado, cmap= plt.cm.Reds)
            plt.axis('off')
                
        #grafica para no direccionados
        elif directed is not True:
            nx.draw_networkx_edges(self.GraphNodes, self.pos_intersections, width= 0.3, node_size=15)
            nodes=nx.draw_networkx_nodes(self.GraphNodes, self.pos_intersections, node_size= width_node, node_color=indices_ordenado, cmap= plt.cm.Reds)

        plt.axis('off')
        cbar = plt.colorbar(nodes, label = str(column_name),shrink=0.9, aspect=30, pad = 0.01)

        if name_to_save_file is not None:
            plt.savefig("results/"+str(name_to_save_file), bbox_inches='tight',pad_inches = 0, dpi = 500)
        else:
            plt.show()
    
    def plotEdges(self, dataframe, column_name:str, directed:bool = True ,name_to_save_file: str = None, ):
        """
        Crea, guarda y muestra los indices que queremos ver(que esten en el dataFrame) en la ciudad.

        Args: 
            column_name(str): Nombre de la columna del dataFrame que queremos ver.  
            name_to_save_file(str) = None:  En caso de querer guardar la imagen poner el nombre
        Return:
            Se muestra la imagen o se guarda.
        """

        fig, ax = plt.subplots()
        ax.imshow(self.img_without_traffic)

        #Indice que graficaremos
        indice = list(dataframe[str(column_name)])
        indices_ordenado = [indice[i] for i in self.DiGraphEdges.nodes()]

        #grafica para direccionados
        if directed is True:
            
            #nx.draw_networkx_edges(self.DiGraphNodes, self.pos_intersections, width= 0.3 , arrowsize=5, node_size=15)
            plt.axis('off')
            edges = nx.draw_networkx_edges(self.DiGraphNodes,
                                            self.pos_intersections,
                                            arrowstyle="-|>",
                                            arrowsize=10,
                                            edge_color=indices_ordenado,
                                            edge_cmap= plt.cm.Reds,
                                            width=5)    

        plt.axis('off')
        #cbar = plt.colorbar(edges, label = str(column_name),shrink=0.9, aspect=30, pad = 0.01)

        if name_to_save_file is not None:
            plt.savefig("results/"+str(name_to_save_file), bbox_inches='tight',pad_inches = 0, dpi = 500)
        else:
            plt.show()

    #Funciones de otras aplicaciones en la red:
    def randomwalkAnalitic_nodes(self):
        Adjacency_matrix = self.getAdjacencyMatrix()[0]
        
        Matrix_B = (Adjacency_matrix.T/np.sum(Adjacency_matrix.transpose(), axis=0)) - np.identity(len(Adjacency_matrix))
        autovalores, autovectores = np.linalg.eig(Matrix_B)
        
        indice = next((i for i, valor in enumerate(autovalores) if abs(valor) < 1e-15), 0)
        Probabilidad = [i/sum(autovectores[:, indice]) for i in autovectores[:, indice]]
        Probabilidad = {indice: np.real(valor) for indice, valor in enumerate(Probabilidad)}
        
        return Probabilidad    
 
    def randomwalkAnalitic_edges(self):
        Adjacency_matrix = np.array(nx.adjacency_matrix(self.DiGraphEdges, nodelist=sorted(self.DiGraphEdges.nodes())).todense())
        
        Matrix_B = (Adjacency_matrix.T/np.sum(Adjacency_matrix.transpose(), axis=0)) - np.identity(len(Adjacency_matrix))
        autovalores, autovectores = np.linalg.eig(Matrix_B)
        
        indice = next((i for i, valor in enumerate(autovalores) if abs(valor) < 1e-15), 0)
        Probabilidad = [i/sum(autovectores[:, indice]) for i in autovectores[:, indice]]
        Probabilidad = {indice: np.real(valor) for indice, valor in enumerate(Probabilidad)}
        
        return Probabilidad
    
    def eherenfestSimulation(self, Adjacency_matrix ,N_particulas,Tiempo):
        
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




if __name__ == "__main__":
    
    path_img_no_traffic = "data/raw/Images/screenshots/CleanScreenshot.png"
    path_network_info = "data/processed/from_networkCreator/PuntaArenas"
    path_network_info = "data/processed/from_networkCreator/PuntaArenasDetallado"


    """
    PuntaArenasDetallado = NetworkData(path_network_info)
    df = PuntaArenasDetallado.getBasicIndexCentralityForEdges()
    print(df)
    df.to_csv("Detallado_IndicesCentralidad.csv")
    path_network_info = "data/DataMakeNetwork/PuntaArenas"
    PuntaArenas = NetworkData(path_network_info)
    df = PuntaArenas.getBasicIndexCentralityForEdges()
    print(df)
    df.to_csv("Simple_IndicesCentralidad.csv")
    """
    path_medina = "data/DataMakeNetwork/Medina"
    Medina = NetworkData(path_medina)

    # Nodos
    """
    RW = Medina.randomwalkAnalitic_nodes()
    df = Medina.getBasicIndexCentrality()
    df["RW"] = RW
    print(df)
    Medina.plotNodes(df, "RW", True, width_node=50)
    """

    # Probando con ejes

    RW = Medina.randomwalkAnalitic_edges()
    df = Medina.getBasicIndexCentralityForEdges()
    df["RW"] = RW
    Medina.plotEdges(df, "RW", True)

    Matrix_Adj_edges = Medina.getAdjacencyMatrix()[1]
    print(Matrix_Adj_edges)


    

