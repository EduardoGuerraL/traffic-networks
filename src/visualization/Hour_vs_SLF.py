import os
import matplotlib.pyplot as plt

def cargar_datos_desde_txt(label, hora_in, minuto_in):
    """
    Carga los datos desde un archivo .txt correspondiente a un intervalo de tiempo y un nodo.

    Args:
        label (str): Identificador del nodo.
        hora_in (int): Hora inicial del intervalo.
        minuto_in (int): Minuto inicial del intervalo.

    Returns:
        list: Lista de valores cargados desde el archivo.
    """
    filename = f'data/RepValdi/density_{label}/{label}_{hora_in:02d}:{minuto_in:02d}.txt'
    if not os.path.exists(filename):
        raise FileNotFoundError(f"El archivo {filename} no existe.")
    
    with open(filename, 'r') as file:
        data = [float(line.strip()) for line in file if line.strip()]
    return data

def procesar_datos(labels, intervals_minutes, hora_inicio=7, minuto_inicio=0):
    """
    Procesa datos cargándolos desde archivos .txt para cada nodo y intervalo de tiempo.

    Args:
        labels (list): Lista de identificadores de nodos.
        intervals_minutes (int): Duración del intervalo en minutos.
        hora_inicio (int): Hora de inicio del análisis.
        minuto_inicio (int): Minuto de inicio del análisis.

    Returns:
        dict: Diccionario con datos procesados para cada nodo.
    """
    datos = {}
    for label in labels:
        mean_per_node = []
        hora_in = hora_inicio
        minuto_in = minuto_inicio
        
        while hora_in < 23 or (hora_in == 23 and minuto_in < 60):
            try:
                # Cargar datos desde el archivo correspondiente
                valores = cargar_datos_desde_txt(label, hora_in, minuto_in)
                mean_per_node.append(valores)
            except FileNotFoundError as e:
                print(e)
            
            # Avanzar al siguiente intervalo
            minuto_in += intervals_minutes
            if minuto_in >= 60:
                hora_in += minuto_in // 60
                minuto_in %= 60
        
        datos[label] = mean_per_node
    return datos

def calcular_estadisticas_porcentiles(mean_per_node):
    """
    Calcula los percentiles y otros estadísticos a partir de los datos procesados.

    Args:
        mean_per_node (list): Lista de valores por intervalo.

    Returns:
        dict: Diccionario con los resultados.
    """
    import numpy as np
    percentiles = [25, 50, 75]
    resultados = {
        "percentiles": {p: [np.percentile(intervalo, p) for intervalo in mean_per_node] for p in percentiles},
        "medias": [np.mean(intervalo) for intervalo in mean_per_node],
    }
    return resultados

def graficar_resultados(intervals_minutes, resultados, labels, colores):
    """
    Genera un gráfico de los resultados.

    Args:
        intervals_minutes (int): Intervalo de tiempo en minutos.
        resultados (dict): Datos procesados por nodo.
        labels (list): Lista de etiquetas de nodos.
        colores (dict): Colores para cada nodo.
    """
    n_intervalos = len(resultados[labels[0]]["medias"])
    horas = [i * intervals_minutes / 60 for i in range(n_intervalos)]
    plt.figure(figsize=(10, 6))
    for label in labels:
        plt.plot(horas, resultados[label]["medias"], label=f"Media {label}", color=colores[label])
        for p, vals in resultados[label]["percentiles"].items():
            plt.fill_between(horas, vals, alpha=0.2, label=f"Percentil {p} {label}")
    plt.xlabel("Horas")
    plt.ylabel("Valores")
    plt.title("Resultados por Intervalos")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    labels = ["N505", "N506"]  # Ejemplo de etiquetas
    intervals_minutes = 30
    colores = {"N505": "blue", "N506": "red"}  # Colores para el gráfico
    
    # Procesar datos desde los archivos .txt
    datos = procesar_datos(labels, intervals_minutes)
    
    # Calcular estadísticas para cada nodo
    resultados = {}
    for label, mean_per_node in datos.items():
        resultados[label] = calcular_estadisticas_porcentiles(mean_per_node)
    
    # Graficar resultados
    graficar_resultados(
        intervals_minutes,
        resultados,
        labels,
        colores
    )

if __name__ == "__main__":
    main()
