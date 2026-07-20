import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
import os
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
        # node_conections --> intersection_2_intersection (inter_conection)
        # lanes --> street_lanes
        fraction_pos_intersections = eval(open(str(path_dir_network_data)+"/node_positions.dat", "r").readline())
        self.inter_conections = eval(open(str(path_dir_network_data)+"/node_conections.dat", "r").readline()) #Conexiones
        self.street_lanes = eval(open(str(path_dir_network_data)+"/lanes_of_link.dat", "r").readline())#Carriles por calle
        
        
        # Rezise position of intersections to img coordinates
        self.pos_intersections = {} # {0: [301, 719], 1: [298, 717], 2: [300, 714], ... , N_inter: [x, y]}
        for i, tupla in enumerate(fraction_pos_intersections):
            self.pos_intersections[i] = list([int(tupla[0]*self.img_without_traffic.shape[1]), int(tupla[1]*self.img_without_traffic.shape[0])])        


        ## Pass intersections to links and streets to nodes.
        
        Intersections_of_street =  dict(enumerate(self.inter_conections)) #{0: (0, 3), 1: (3, 6), ... , N_street: (N_inter_i, N_inter_f)} ## NODOS
        self.conection_btw_streets = []
        for i in range(len(Intersections_of_street)):
            for j in range(len(Intersections_of_street)):
                if (Intersections_of_street[i][1]) == Intersections_of_street[j][0] and j!=i:
                    self.conection_btw_streets.append((i,j))
    
        # Coordinates conections for street
        self.Streets_coordinates = {} # {0: ([301, 719], [303, 715]), 1: ([303, 715], [331, 675]), ..., N_street: [x,y]_i,[x,y]_f}
        for N_street, (N_inter_i, N_inter_f) in Intersections_of_street.items():
            self.Streets_coordinates[N_street] = (self.pos_intersections[N_inter_i], self.pos_intersections[N_inter_f])
        print('\n', self.Streets_coordinates)

        ## Use Networkx to make network
        # DiGraph --> DG
        # Graph --> UG
        
        # Intersections To Nodes(_inter)
        self.DG_inter = nx.DiGraph(self.inter_conections)
        self.UG_inter = nx.Graph(self.inter_conections)
        
        # Streets to Nodes
        self.DG_streets = nx.DiGraph(self.conection_btw_streets)
        self.UG_streets = nx.Graph(self.conection_btw_streets)
    
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

    #Funciones de entrega de caracteristicas
    def getAdjacencyMatrix(self):
        Adjacency_matrix_edges = np.array(nx.adjacency_matrix(self.UG_streets, nodelist=sorted(self.UG_streets.nodes())).todense())
        Adjacency_matrix_nodes = np.array(nx.adjacency_matrix(self.UG_inter, nodelist=sorted(self.UG_inter.nodes())).todense())

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
        

        largo_de_calles = long_of_streets(self.pos_intersections, self.inter_conections)
        
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
        indices_ordenado = [indice[i] for i in self.DG_inter.nodes()]

        #grafica para direccionados
        if directed is True:
            
            nx.draw_networkx_edges(self.DG_inter, self.pos_intersections, width= 0.3 , arrowsize=5, node_size=15)
            nodes=nx.draw_networkx_nodes(self.DG_inter, self.pos_intersections, node_size= width_node, node_color=indices_ordenado, cmap= plt.cm.Reds)
            plt.axis('off')
                
        #grafica para no direccionados
        elif directed is not True:
            nx.draw_networkx_edges(self.UG_inter, self.pos_intersections, width= 0.3, node_size=15)
            nodes=nx.draw_networkx_nodes(self.UG_inter, self.pos_intersections, node_size= width_node, node_color=indices_ordenado, cmap= plt.cm.Reds)

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
        indices_ordenado = [indice[i] for i in self.DG_streets.nodes()]

        #grafica para direccionados
        if directed is True:
            
            #nx.draw_networkx_edges(self.DG_inter, self.pos_intersections, width= 0.3 , arrowsize=5, node_size=15)
            plt.axis('off')
            edges = nx.draw_networkx_edges(self.DG_inter,
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
        Adjacency_matrix = np.array(nx.adjacency_matrix(self.DG_streets, nodelist=sorted(self.DG_streets.nodes())).todense())
        
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


def save_dictionary(dictionary, path):
    # Obtener el directorio (ruta sin el nombre del archivo)
    directory = os.path.dirname(path)
    
    # Si el directorio no existe, créalo
    if directory and not os.path.exists(directory):
        try:
            os.makedirs(directory)
            print(f'Directory {directory} created.')
        except OSError as e:
            print(f'Error creating directory {directory}: {e}')
            return
    
    # Guardar el diccionario en el archivo
    try:
        with open(path, 'w') as file:
            keys_of_dict = sorted(dictionary.keys())
            ordered_values = [dictionary[key] for key in keys_of_dict]
            for key, value in zip(keys_of_dict, ordered_values):
                file.write(f'{key}\t{value}\n')
        print(f'The dictionary has been successfully saved to {path}.')
    except IOError as e:
        print(f'Error trying to save the dictionary to {path}: {e}')

if __name__ == "__main__":
    
    def save_data_centrality_for_models_networks():
        
        path_to_save_centrality = 'data/processed/DataNetwork/centrality_for_models'

        #Our Models
        DGN1207 = PA_N1207.DG_streets
        DGN505 = PA_N505.DG_streets
        UGN1207 = PA_N1207.UG_streets
        UGN505 = PA_N505.UG_streets

        #DGN1207
        BC_DGN1207 = nx.betweenness_centrality(DGN1207)
        CC_DGN1207 = nx.closeness_centrality(DGN1207)
        DC_DGN1207 = nx.degree_centrality(DGN1207)
        
        #DGN505
        BC_DGN505 = nx.betweenness_centrality(DGN505)
        CC_DGN505 = nx.closeness_centrality(DGN505)
        DC_DGN505 = nx.degree_centrality(DGN505)
        
        #UGN1207
        BC_UGN1207 = nx.betweenness_centrality(UGN1207)
        CC_UGN1207 = nx.closeness_centrality(UGN1207)
        DC_UGN1207 = nx.degree_centrality(UGN1207)
        
        #UGN505
        BC_UGN505 = nx.betweenness_centrality(UGN505)
        CC_UGN505 = nx.closeness_centrality(UGN505)
        DC_UGN505 = nx.degree_centrality(UGN505)
    
        ## SAVE DATA
        save_dictionary(BC_DGN1207, path_to_save_centrality + '/BC_DGN1207.dat')
        save_dictionary(BC_DGN505, path_to_save_centrality + '/BC_DGN505.dat')
        save_dictionary(BC_UGN1207, path_to_save_centrality + '/BC_UGN1207.dat')
        save_dictionary(BC_UGN505, path_to_save_centrality + '/BC_UGN505.dat')
        save_dictionary(CC_DGN1207, path_to_save_centrality + '/CC_DGN1207.dat')
        save_dictionary(CC_DGN505, path_to_save_centrality + '/CC_DGN505.dat')
        save_dictionary(CC_UGN1207, path_to_save_centrality + '/CC_UGN1207.dat')
        save_dictionary(CC_UGN505, path_to_save_centrality + '/CC_UGN505.dat')
        save_dictionary(DC_DGN1207, path_to_save_centrality + '/DC_DGN1207.dat')
        save_dictionary(DC_DGN505, path_to_save_centrality + '/DC_DGN505.dat')
        save_dictionary(DC_UGN1207, path_to_save_centrality + '/DC_UGN1207.dat')
        save_dictionary(DC_UGN505, path_to_save_centrality + '/DC_UGN505.dat')

    def save_streets_coordinates():
        path_to_save = 'data/processed/DataNetwork/streets_coordinates'
        
        #Our Models
        N1207 = PA_N1207.Streets_coordinates
        N505  = PA_N505.Streets_coordinates

        save_dictionary(N1207, path_to_save + '/N1207_coordinates.dat')
        save_dictionary(N505, path_to_save + '/N505_coordinates.dat')

    def save_Adj_matrix(matrix, path_to_save):
        """
        Guarda una matriz en un archivo y verifica que contenga solo valores 0 o 1.
        
        Args:
            matrix (numpy.ndarray): Matriz a procesar.
            filename (str): Nombre del archivo para guardar la matriz.

        Returns:
            dict: Diccionario con el tamaño de la matriz (filas, columnas) y la cantidad de 1s encontrados.
        """
        # Verificar que la matriz solo contenga valores 0 o 1
        if not np.all(np.isin(matrix, [0, 1])):
            raise ValueError("La matriz contiene valores distintos de 0 y 1.")

        # Guardar la matriz en el archivo
        np.savetxt(path_to_save, matrix, fmt='%d', delimiter=',')

        # Calcular el tamaño de la matriz y la cantidad de 1s
        rows, cols = matrix.shape
        ones_count = np.sum(matrix)

        # Retornar resultados
        return {
            "size": (rows, cols),
            "ones_count": ones_count
        }

        

    path_img_no_traffic = "data/raw/Images/screenshots/CleanScreenshot.png"
    path_network_N505 = "data/processed/from_networkCreator/PuntaArenas"
    path_network_N1207 = "data/processed/from_networkCreator/PuntaArenasDetallado"

    PA_N1207 = NetworkData(path_network_N1207, path_img_no_traffic)
    PA_N505 = NetworkData(path_network_N505, path_img_no_traffic)

    matrix_intersections1, matrix_streets1 = PA_N505.getAdjacencyMatrix()
    matrix_intersections2, matrix_streets2 = PA_N1207.getAdjacencyMatrix()
    save_Adj_matrix( matrix_intersections1, 'data/RepValdi/UGN505_intersection_adjacency_matrix.txt')
    save_Adj_matrix( matrix_streets1, 'data/RepValdi/UGN505_street_adjacency_matrix.txt')
    
    save_Adj_matrix( matrix_intersections2, 'data/RepValdi/UGN1207_intersection_adjacency_matrix.txt')
    save_Adj_matrix( matrix_streets2,'data/RepValdi/UGN1207_street_adjacency_matrix.txt')
    
    
    #save_data_centrality_for_models_networks()
    #save_streets_coordinates()
    


    

