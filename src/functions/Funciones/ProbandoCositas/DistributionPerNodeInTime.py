import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from scipy.optimize import curve_fit
from scipy.interpolate import splrep, splev

import numpy as np
from scipy.interpolate import splrep, splev

def ajuste_datos_ciclicos(datos):
    # Encontrar índices de datos no nulos
    indices_no_nulos = np.where(~np.isnan(datos))[0]

    # Datos conocidos (sin valores NaN)
    datos_conocidos = datos[indices_no_nulos]

    # Interpolación no lineal
    tck = splrep(indices_no_nulos, datos_conocidos, k=3, s=0)

    # Predicción de datos faltantes
    indices_prediccion = np.where(np.isnan(datos))[0]
    datos_prediccion = splev(indices_prediccion, tck)

    # Combinar datos conocidos y predichos
    datos_completos = np.copy(datos)
    datos_completos[indices_prediccion] = datos_prediccion

    return datos_completos

def exponential_func(x, a, b, c):
    return a * np.exp(b * x) + c

def plot_nonlinear_regression(x, y):
    # Eliminar los puntos con valores NaN
    valid_indices = np.logical_not(np.isnan(y))
    x_valid = np.array(x)[valid_indices]
    y_valid = np.array(y)[valid_indices]

    # Ajuste de regresión no lineal
    popt, pcov = curve_fit(exponential_func, x_valid, y_valid)

    # Crear datos para la curva ajustada
    x_fit = np.linspace(min(x_valid), max(x_valid), 100)
    y_fit = exponential_func(x_fit, *popt)

    # Graficar los puntos y la curva ajustada
    plt.scatter(x_valid, y_valid, label='Puntos')
    plt.plot(x_fit, y_fit, 'r-', label='Regresión no lineal')

    # Configuración de etiquetas y título
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Regresión no lineal')

    # Mostrar leyenda
    plt.legend()

    # Mostrar gráfico
    plt.show()
"""
def obtener_instantes_faltantes(inicio, fin):
            format_string = "/%Y-%m-%d_%H-%M.png"
            instantes = []

            inicio_dt = datetime.strptime(inicio, format_string)
            fin_dt = datetime.strptime(fin, format_string)

            # Añadir el primer instante
            instantes.append(inicio)

            # Calcular los instantes de tiempo faltantes
            while inicio_dt < fin_dt:
                inicio_dt += timedelta(minutes=15)

                instante_faltante = inicio_dt.strftime(format_string)
                instantes.append(instante_faltante)

            return instantes
"""

def format_xticks(date_str):
    # Convertir la cadena de fecha a objeto de fecha
    date = datetime.strptime(date_str, '/%Y-%m-%d_%H-%M.png')
    # Obtener el nombre del día de la semana y el tiempo en formato "Día Hora:Minuto"
    formatted_date = date.strftime('%A %H:%M')
    return formatted_date


def graph(indice_i):
    df = pd.read_csv("data/DataImages/In_Streets_Coord/DataStreetsDetR1Step2_mean.csv")
    # Seleccionar la columna del índice específico
    datos_indice = df.iloc[indice_i][4:-1] 
    columns_complete_to_keep = obtener_instantes_faltantes(datos_indice.index[0], datos_indice.index[-1])
    valores_de_nodo = []
    for col in columns_complete_to_keep:
        if col in datos_indice.index:
            valores_de_nodo.append(datos_indice[col])
        elif col not in datos_indice.index:
            valores_de_nodo.append(np.nan)
        else:
            print("Slgo malo pasa")

    columns_complete_to_keep = columns_complete_to_keep[:3500]
    valores_de_nodo = valores_de_nodo[:3500]

    valores_de_undia = valores_de_nodo[:96*3]

    while len(valores_de_undia) < len(valores_de_nodo):
        valores_de_undia += valores_de_undia

    # Ajustar el tamaño de la lista1 al tamaño de la lista2
        valores_de_undia = valores_de_undia[:len(valores_de_nodo)]

    
    ## Graficar el avance en el tiempo del índice i
    plt.scatter(columns_complete_to_keep, valores_de_nodo)
    plt.plot(columns_complete_to_keep, valores_de_undia, color = "red")
    plt.xlabel('tiempo')
    plt.ylabel('particulas')
    plt.title(f'Avance en el tiempo de la calle {indice_i}')

     # Agregar cuadrado de color
    week_start = columns_complete_to_keep[0]
    week_end = columns_complete_to_keep[96*3]
    plt.axvspan(columns_complete_to_keep[0], columns_complete_to_keep[96*3], facecolor='red', alpha=0.2)
    plt.axvspan(columns_complete_to_keep[96*10],columns_complete_to_keep[96*17], facecolor='red', alpha=0.2)
    plt.axvspan(columns_complete_to_keep[96*24],columns_complete_to_keep[96*31], facecolor='red', alpha=0.2)

    # Configurar los marcadores y etiquetas del eje x
    intervalo = 96  # Mostrar un marcador y etiqueta cada 1 elemento
    marcadores = plt.gca().get_xticks()[::intervalo]
    etiquetas = [format_xticks(xtick) for xtick in columns_complete_to_keep[::intervalo]]
    plt.xticks(marcadores, etiquetas, rotation=45)
    for x in marcadores:
        plt.axvline(x=x, color='gray', linestyle='dashed', linewidth=0.5)
    
    plt.show()
    
def graph_node(indice, filtrar = True):
    def quitar_sabado_domingo(df):
        # Convierte las columnas de fecha a tipo datetime
        fechas = pd.to_datetime(df.columns, format="/%Y-%m-%d_%H-%M")
        
        # Obtiene el índice de las columnas que corresponden a los sábados y domingos
        columnas_sabado_domingo = df.columns[(fechas.weekday == 5) | (fechas.weekday == 6)]
        
        # Elimina las columnas correspondientes a los sábados y domingos
        df_filtrado = df.drop(columnas_sabado_domingo, axis=1)
        
        return df_filtrado

    def obtener_instantes_faltantes(inicio, fin):
        format_string = "/%Y-%m-%d_%H-%M"
        instantes = []

        inicio_dt = datetime.strptime(inicio, format_string)
        fin_dt = datetime.strptime(fin, format_string)

        # Añadir el primer instante
        instantes.append(inicio)

        # Calcular los instantes de tiempo faltantes
        while inicio_dt < fin_dt:
            inicio_dt += timedelta(minutes=15)

            instante_faltante = inicio_dt.strftime(format_string)
            instantes.append(instante_faltante)

        return instantes
    
    def format_xticks(date_str):
        # Convertir la cadena de fecha a objeto de fecha
        date = datetime.strptime(date_str, '/%Y-%m-%d_%H-%M')
        # Obtener el nombre del día de la semana y el tiempo en formato "Día Hora:Minuto"
        formatted_date = date.strftime('%A %H:%M')
        return formatted_date

     
    df = pd.read_csv("data/DataImages/In_Intersection_Coord/intersectionCoord.csv")

    # Seleccionar la columna del índice específico
    datos_indice = df.iloc[indice][3:-1]
    columns_complete_to_keep = obtener_instantes_faltantes(datos_indice.index[0], datos_indice.index[-1])
    
    
    valores_de_nodo = []
    for col in columns_complete_to_keep:
        if col in datos_indice.index:
            valores_de_nodo.append(datos_indice[col])
        elif col not in datos_indice.index:
            valores_de_nodo.append(np.nan)
        else:
            print("Slgo malo pasa")

    if filtrar:
        # Crear el DataFrame
        new_df = pd.DataFrame(columns=columns_complete_to_keep)
        new_df.loc[0] = valores_de_nodo

        new_df = quitar_sabado_domingo(new_df)
        columns_complete_to_keep  = new_df.columns
        valores_de_nodo = list(new_df.iloc[0])

    #columns_complete_to_keep = columns_complete_to_keep[:1000]
    #valores_de_nodo = valores_de_nodo[:1000]
    
    ## Graficar el avance en el tiempo del índice i
    plt.scatter(columns_complete_to_keep, valores_de_nodo)
    #plt.plot(columns_complete_to_keep, valores_de_undia, color = "red")
    plt.xlabel('tiempo')
    plt.ylabel('particulas')
    plt.title(f'Avance en el tiempo del nodo {indice}')
    # Configurar los marcadores y etiquetas del eje x
    intervalo = 96  # Mostrar un marcador y etiqueta cada 1 elemento
    marcadores = plt.gca().get_xticks()[::intervalo]
    etiquetas = [format_xticks(xtick) for xtick in columns_complete_to_keep[::intervalo]]
    plt.xticks(marcadores, etiquetas, rotation=90)
    plt.show()

    
    import statsmodels.api as sm

    # Crea un DataFrame con la serie de datos
    df = pd.DataFrame(valores_de_nodo, columns=['Valor'])

    # Rellena los valores faltantes con interpolación lineal
    df['Valor'] = df['Valor'].interpolate()

    # Calcula la autocorrelación
    autocorrelation = sm.tsa.acf(df['Valor'], nlags=len(df)-1)

    # Grafica la autocorrelación
    plt.stem(autocorrelation)
    plt.xlabel('Retraso')
    plt.ylabel('Autocorrelación')
    plt.title('Autocorrelación de los datos')

     # Configurar los marcadores y etiquetas del eje x
    intervalo = 96 * 7  # Mostrar un marcador y etiqueta cada 1 elemento
    marcadores = plt.gca().get_xticks()[::intervalo]
    plt.show()



if __name__ == "__main__":
    graph_node(200, False)