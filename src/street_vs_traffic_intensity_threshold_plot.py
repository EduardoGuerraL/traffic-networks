from functions.basics import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
Dado un limite inferior(threshold), muestra como es el promedio(negro) de cada calle para cierta hora especifica.
"""

Threshold = 100

def apply_threshold(lista_de_listas, N):
    # Recorremos todas las listas en la lista de listas
    for lista in lista_de_listas:
        # Utilizamos una comprensión de lista para filtrar los números mayores o iguales a N
        lista[:] = [x for x in lista if x >= N]

        # Si la lista quedó vacía después de eliminar los elementos menores a N, agregamos un 0
        if not lista:
            lista.append(0)

    return lista_de_listas

def graficar_lista_de_listas(lista_de_listas, treshold):
    
    """
    for i, lista in enumerate(lista_de_listas):
        X_down = []
        X_up = []
        Y_down = []
        Y_up = []
        for elemento in lista:
            if elemento < treshold:
                X_down.append(i)
                Y_down.append(elemento)
            elif elemento >= treshold:
                X_up.append(i) 
                Y_up.append(elemento) 
        
        plt.scatter(X_down, Y_down, c = "k", alpha=0.03)
        plt.scatter(X_up, Y_up, c = "r", alpha=0.03)
    """

    X = np.arange(len(lista_de_listas))
    X_down = []
    Y_down = []
    X_up = []
    Y_up = []
    Y_promedio = []

    for i, lista in enumerate(lista_de_listas):
        mask_down = np.array(lista) < treshold
        mask_up = ~mask_down
        X_down.extend(X[i] * np.ones(np.sum(mask_down)))
        Y_down.extend(np.array(lista)[mask_down])
        X_up.extend(X[i] * np.ones(np.sum(mask_up)))
        Y_up.extend(np.array(lista)[mask_up])
    
    
    # Scatter plots
    plt.scatter(X_down, Y_down, c="blue", alpha=0.01)
    plt.scatter(X_up, Y_up, c="red", alpha=0.10)


    # Calcular el promedio de Y_up para cada lista
    promedios = [np.mean(np.array(lista)[np.array(lista) >= treshold]) for lista in lista_de_listas]

    # Scatter plot de Numero de Calle vs Promedio
    plt.scatter(X, promedios, c="black", label="Promedio de Y_up")
    
    
    # Etiquetas y leyenda
    plt.xlabel('Numero de Calle')
    plt.ylabel("Escala de Trafico[Valor Pixel]")
    plt.legend()

    # Mostrar la gráfica
    plt.show()

## Abriendo datos
#"data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv"
name = "data/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv"
datos = pd.read_csv(name)

## Obtener columnas que corresponden a hora y minutos
columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos.columns, hora_exacta=(8,00))#rango_horas=(8,20)

## Obtenemos los datos para cada nodo en esa hora
datos = datos[columnas_elejidas].values.tolist()

graficar_lista_de_listas(datos, Threshold)