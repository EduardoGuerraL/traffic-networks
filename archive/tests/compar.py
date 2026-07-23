
import numpy as np
import os
import networkx as nx
import matplotlib.pyplot as plt
import scipy
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import scienceplots


adj_matrix = 'data/RepValdi/DGN505_street_adjacency_matrix.txt'

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
def load_matrix_from_csv(filename):
    """
    Abre un archivo CSV y devuelve la matriz escrita dentro.

    Args:
        filename (str): Nombre del archivo CSV.

    Returns:
        numpy.ndarray: Matriz cargada desde el archivo.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"El archivo {filename} no existe.")

    # Cargar la matriz desde el archivo CSV
    matrix = np.loadtxt(filename, delimiter=',', dtype=int)
    return matrix
def load_DensityTraffic_from_txt(filename):
    """
    Abre un archivo CSV y devuelve la matriz escrita dentro.

    Args:
        filename (str): Nombre del archivo CSV.

    Returns:
        numpy.ndarray: Matriz cargada desde el archivo.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"El archivo {filename} no existe.")

    # Cargar la matriz desde el archivo CSV
    matrix = np.loadtxt(filename, delimiter='\t', dtype=float)
    return matrix
def adjacency_matrix_to_graph(matrix):
    """
    Convierte una matriz de adyacencia en un grafo de NetworkX.

    Args:
        matrix (numpy.ndarray): Matriz de adyacencia.

    Returns:
        networkx.Graph: Grafo generado a partir de la matriz de adyacencia.
    """
    # Crear el grafo desde la matriz de adyacencia
    graph = nx.from_numpy_array(matrix)
    return graph
def scatter_and_boxplot(X, Y, N):
    ## GRAFICANDO SCATTER CON BOXPLOT

    # Dividir X e Y en N intervalos
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, N)

    # Crear un subplot con dos gráficos en la misma fila
    plt.style.use(["science", "notebook", "grid"])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 11), gridspec_kw={'width_ratios': [10, 1]}, sharey=True)
    ax1.grid(True)
    # Gráfico de diagrama de caja en el primer subplot
    Medianas = []
    Posiciones_X = []
    ancho = 1/N
    for i in range(N):
        if intervalos_X[i]:
            #ancho = (intervalos_X[i][-1] - intervalos_X[i][0]) ANCHO VARIABLE
            pos_x_to_plot = [ancho*(i + 1/2)]
            pos_x_to_save = [np.mean(intervalos_X[i])]
            ax1.boxplot(intervalos_Y[i], positions=pos_x_to_plot, widths=ancho, showfliers=False, patch_artist=True, boxprops={'facecolor': 'gray', 'alpha': 0.4}, medianprops={'color': 'black', 'linewidth': 3})
            # Guardando datos[punto medio de x boxes, mean de Y, median de Y]
            Posiciones_X.append(pos_x_to_plot[0])
  
    Medianas = [np.median(subconjunto) for subconjunto in intervalos_Y]

    # Configuración del primer subplot (gráfico de caja)
    ax1.scatter(X, Y, label="Scatter Plot", color='gray', alpha=0.1, s=20, edgecolor='black', marker='o')

    ax1.set_xlim(0,1)
    ax1.set_ylim(0,1)
    ax1.set_xticks([])
    #ax1.legend(loc='upper right')

    # Ajustar el tamaño de las fuentes en el gráfico
    xticks_values = [min(X), max(X)]
    formatted_xticks = ["{:.0f}".format(value) for value in xticks_values]
    
    ax1.set_xticks(xticks_values, formatted_xticks)

    
    # Gráfico de densidad en el segundo subplot (rotado en 90 grados)
    sns.kdeplot(Y, ax=ax2, color='blue', vertical=True, common_norm = True)
    plt.hist(Y, orientation="horizontal", density=True, bins=40, color="blue", alpha = 0.3)
    ax2.set_xlabel("")
    ax2.set_ylim(0,1)
    ax2.set_xlim(0,12)
    ax2.set_xticks([])
    return Medianas, Posiciones_X, ax1, ax2
def guardar_lista_en_archivo(lista, nombre_archivo):
    """
    Guarda una lista en un archivo de texto, escribiendo cada elemento en una línea separada.

    Args:
        lista (list): La lista a guardar.
        nombre_archivo (str): El nombre del archivo donde guardar la lista.
    """
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            for elemento in lista:
                archivo.write(f"{elemento}\n")
        print(f"Lista guardada exitosamente en {nombre_archivo}")
    except Exception as e:
        print(f"Error al guardar la lista en el archivo: {e}")



Adj = load_matrix_from_csv(adj_matrix)
Graph = adjacency_matrix_to_graph(Adj)
centrality = list(nx.closeness_centrality(Graph).values())
# Convertir a un arreglo 2D para usar con MinMaxScaler
valores_array = np.array(centrality).reshape(-1, 1)

# Inicializar el escalador
scaler = MinMaxScaler()

# Ajustar y transformar los valores
valores_normalizados = scaler.fit_transform(valores_array)

# Convertir de nuevo a 1D si es necesario
centrality = valores_normalizados.flatten()

Slopes = []

hora_inicial, hora_final = 0, 24
for hora_in in range(hora_inicial, hora_final):
    for minuto_in in range(0, 60, 15):
        avg_per_time = 'data/processed/DataImages/N505/avg_per_time/R_1_S_6/' + str(hora_in) + '_' + str(minuto_in)

        NTD = load_DensityTraffic_from_txt(avg_per_time)
        NTD = [i/4 for i in NTD[:, 1]]

        ## GRAFICANDO 
        ### Agregando Cajas
        medians_box, pos_box, ax1, ax2 = scatter_and_boxplot(list(centrality), list(NTD), 20)

        ## REGRESION LINEAL
        #(slope, intercept, r_value, p_value, std_err)
        medians_params = scipy.stats.linregress(pos_box, medians_box)    

        x = np.linspace(-10, 10, 100)
        y = medians_params[0] * x + medians_params[1]

        Slopes.append(medians_params[0])


        ax1.plot(x, y, '-r', label='y = {}x + {}'.format(medians_params[0], medians_params[1]))

        ## Guardando los graficos
        plt.tight_layout()
        # Ajustar la distancia entre los subgráficos
        plt.subplots_adjust(wspace=0)

        #plt.show()
    
guardar_lista_en_archivo(Slopes, 'data/RepValdi/DGN505_SLF.txt')