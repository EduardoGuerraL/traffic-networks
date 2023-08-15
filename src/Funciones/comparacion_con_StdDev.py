import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import re
from sklearn.preprocessing import normalize

def getCIInMeanObsDataDistributionWithStdDev(datos_observacionales ,computational_data, 
                                            type_of_scale:str = "rescale",
                                            hour = False,
                                            minutes = False,
                                            graph:bool = True,
                                            with_zeros: bool = True):
    """
    Entregamos el dato computacional que queremos comparar y el tipo de calculo que se obtuvo para obtener el dato de un solo link, es decir,
    si se tomó solo el mayor dato dentro del link o un promedio.
    Devuelve un gráfico donde podemos comparar el promedio de valor 
    observacional para cada Link y el valor de indice que necesitemos para cierta hora y minuto.
    
    Nos entrega alguna información relevante sobre la comparación de los datos observacionales y computacionales.

    Args
    ----

        name_column_CompData(str): nombre del indice de centralidad que queremos mostrar.
        
        type_get_obs_link(str): El tipo de valor observacional que se mostrará:
                            - Int: la suma de los computational_data de una calle (borrar luego)
                            - Max: El maximo de los computational_data de una calle
                            - Prom: El promedio de los computational_data de una calle
        
        type_of_scale: Tipo de reescalado que se desea hacer a los datos, para poder hacer una comparación a la misma escala.
                        Podemos elegir entre: ("normalized", "rescale", "norm_and_res").

                        "normalized": Aplicar la norma euclidiana a los datos. (normalizar sobre todos los datos y normalizar por sobre los de un nodo.)
                        "rescale": Se reescala todo suponiendo que 255 es el maximo y 0 el minimo para los datos observacionales. para los
                                    datos computacionales se usa el max y min de la lista.
                        "norm_and_res:  Se aplica ambos, primero normalizamos y luego reescalamos. En este caso se tiene que usar para ambos una reescalación
                                        de min y max.
        
        hour: Hora para la cual queremos acotar los datos observacionales. (0-23)
        
        minute: por si queremos acotar los datos en minutos (0,15,30,45)
        
        graph: True or False si queremos obtener el grafico o no.

        max_v = max: valor maximo que se toma para reescalar(x) x -> 1
        
        min_v = min: valor minimo para reescalar(y) y -> 0

        with_zeros (bool): True para calcular con los computational_data que son 0 para los datos observacionales, que suelen ser muchos.
                            False para no usarlos. 
        

    Return:
    -------
        -Gráfico.
        -InsideStdDev, sgm_prom, sgm_max, sgm_min, means_diference
    """
    def dell_zeros(diccionario):
        """
        Por si quiero eliminar los ceros, es decir, cuando no hay taco.
        """
        dict_sin_ceros = {}
        if with_zeros == True:
            return diccionario
        elif with_zeros == False:
            for indice, lista in diccionario.items():
                lista_sin_ceros = [valor for valor in lista if valor != 0]
                if not lista_sin_ceros:  # Verificar si la lista está vacía
                    lista_sin_ceros.append(0)
                dict_sin_ceros[indice] = lista_sin_ceros 
            return dict_sin_ceros
        
    def get_column_in_particular_time(columnas) -> list:
        """
        En caso de acotar a ciertas horas y minutos los datos observacionales. Nos devuelve una lista con las columnas que corresponden.
        """
        columns_to_keep = []
        hora = hour
        minutos = minutes
        if hora == False:
            columns_to_keep = [col for col in columnas if col.startswith("/2023")]     
        elif hora != False and minutos == False:
            try:
                hora = str(hour).zfill(2)
                # Expresión regular para el formato de nombre de archivo especificado
                regex = re.compile(rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}\.png')
                for archivo in columnas:
                    if regex.match(archivo):
                        columns_to_keep.append(archivo)
            except FileNotFoundError:
                print(f"No encuentro archivos de esta forma:", rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}\.png')
        elif hora != False and minutos != False:
            try:
                hora = str(hour).zfill(2)
                minutos = str(minutes).zfill(2)
                # Expresión regular para el formato de nombre de archivo especificado
                regex = re.compile(rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-{minutos}\.png')
                for archivo in columnas:
                    if regex.match(archivo):
                        columns_to_keep.append(archivo)
            except FileNotFoundError:
                print(f"No encuentro archivos de esta forma:", rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-{minutos}\.png')
        else:
            print("Problemas con encontrar columnas en horas y minutos indicados.")
    
        
        return columns_to_keep

    def get_mean_and_stdDev(dict_obs_data):
        mean_and_stdDev = []
    
        def calcular_desviacion_estandar(lista, promedio):
            diferencias = np.array(lista) - promedio
            diferencias_cuadrado = diferencias ** 2
            varianza = np.mean(diferencias_cuadrado)
            desviacion_estandar = np.sqrt(varianza)
            return desviacion_estandar
        
        mean_and_stdDev = []
        for indice, lista in dict_obs_data.items():
            array = list(lista)
            promedio = round(np.mean(array),3)
            desviacion = round(np.std(array),3)
            lista_up = [i for i in lista if i > promedio]
            lista_down = [i for i in lista if i < promedio]
            desviacion_abajo = calcular_desviacion_estandar(lista_down, promedio)
            print(desviacion_abajo)
            desviacion_abajo = promedio - desviacion_abajo
            desviacion_arriba = calcular_desviacion_estandar(lista_up, promedio)
            print(desviacion_arriba)
            desviacion_arriba = promedio + desviacion_abajo
            mean_and_stdDev.append((indice, promedio, desviacion, desviacion_abajo, desviacion_arriba))


        # Ordenar por promedio
        mean_and_stdDev.sort(key=lambda x: x[1])
        mean_and_stdDev = {indice: (valor1, valor2, valor3, valor4) for indice, valor1, valor2, valor3, valor4 in mean_and_stdDev}
        
        return mean_and_stdDev

    def igualandoEscalas(data, axis = 3):
        """
        Para poder comparar los datos necesitamos reescalar los datos para que tenga lógica comparar los datos
        computacionales con los observacionales.

        Hay 3 formas de normalizar: 
            1. Normalizar todos los datos de un nodo.
            2. Normalizar un nodo con respecto a todos los datos de todos los nodos dada una sola imagen.
            3. Normalizar un nodo con respecto a todos los datos de todos los nodos de todas las imagenes 
        
        Las 3 formas son solo para los datos observacionales, para el caso de los datos computacionales solo tenemos una lista,
        así que se hace de la forma 2. 
        Args:
        -----
        axis: 1,2,3, son las formas de normalizar los datos.
        """
        def normalizar(data):
            
            Cantidad_de_nodos_con_norma_nula = 0
            #Para datos observacionales
            if isinstance(data, dict):
                if axis == 1:
                    for N_nodo, lista in data.items():
                        # Calcular la norma euclidiana de la lista
                        norma = math.sqrt(sum([x**2 for x in lista]))
                        if norma == 0:
                            data[N_nodo] = [0]
                            Cantidad_de_nodos_con_norma_nula +=1
                        else:
                            data[N_nodo]= [round(x / norma, 3) for x in lista]
                elif axis == 2:
                    # Obtener todas las posiciones presentes en las listas del diccionario
                    posiciones = set()
                    for lista in data.values():
                        posiciones.update(range(len(lista)))
                    

                    # Normalizar euclidianamente todas las posiciones de las listas
                    elementos_normalizados = []
                    for posicion in posiciones:
                        elementos = [list(lista)[posicion] for lista in data.values()]
                        elementos_normalizados.append( normalize([elementos], norm='l2')[0])
                        print(elementos_normalizados)
                    # Asignar los elementos normalizados de vuelta al diccionario en las posiciones correspondientes
                    
                    new_data = {}
                    for indice  in range(len(elementos_normalizados[0])):
                        lista = []
                        for posicion in posiciones:
                            lista = [i[posicion] for i in elementos_normalizados]
                        new_data[indice] = lista
                    
                    data = new_data
                    
                elif axis == 3:
                    todos = np.concatenate([list(lista) for lista in data.values()])
                    norma = np.linalg.norm(todos)
                    for indice, lista in data.items():
                        lista_normalisada = [i/norma for i in lista]
                        data[indice] = lista_normalisada
                else:
                    print("no se está eligiendo ningun tipo de normalización.")
            
            #para una lista
            elif isinstance(data, list):
                norma = math.sqrt(sum([x**2 for x in data]))
                data = [round(x / norma, 3) for x in data]
            else:
                raise ValueError("Para normalizar necesitamos que sea un diccionario o una lista.")
            return data
            
        def reescalar(data, max_v, min_v):
            if isinstance(data, dict):  # Verificar si es un dict_obs_data #Para los datos obs.
                if axis == 1:
                    for clave, lista in data.items():
                        max_valor = max(lista) if str(max_v) == "max" else float(max_v)
                        min_valor = min(lista) if str(min_v) == "min" else float(min_v)
                                
                        if min_valor == max_valor:
                            data[clave] = lista ### hay que revisar si es bueno dejar asi las listas, pues pede que sirva solo si son ambos 0
                        else:
                            data[clave] = [round((float(valor) - min_valor)/(max_valor - min_valor),3) for valor in lista]
                elif axis == 2:
                    # Obtener todas las posiciones presentes en las listas del diccionario
                    posiciones = set()
                    for lista in data.values():
                        posiciones.update(range(len(lista)))

                    elementos_escalados = []
                    # Normalizar euclidianamente todas las posiciones de las listas
                    for posicion in posiciones:
                        elementos = [lista[posicion] for lista in data.values()]
                        max_valor = max(elementos)
                        min_valor = min(elementos)
                        elementos_escalados.append([round((float(valor) - min_valor)/(max_valor - min_valor),3) for valor in elementos])
                    # Asignar los elementos normalizados de vuelta al diccionario en las posiciones correspondientes
                    new_data = {}
                    for indice  in range(len(elementos_escalados[0])):
                        lista = []
                        for posicion in posiciones:
                            lista = [i[posicion] for i in elementos_escalados]
                        new_data[indice] = lista
                    
                    data = new_data
                
                elif axis == 3:
                    todos = np.concatenate([list(lista) for lista in data.values()])
                    max_valor = max(todos) if str(max_v) == "max" else float(max_v)
                    min_valor = min(todos) if str(min_v) == "min" else float(min_v)            
                    for indice, lista in data.items():
                        lista_reescalada = [(i-min_valor)/(max_valor - min_valor) for i in lista]
                        data[indice] = lista_reescalada
                
                else:
                    print("No se tomó ningun eje en el cual reescalar")
            
            elif isinstance(data, list):  # Verificar si es una lista #Este se ocupara para los datos comp.
                max_valor = max(data)
                min_valor = min(data)
                
                if min_valor == 0 and max_valor == 0:
                    pass
                else:
                    data = [round((valor - min_valor) / (max_valor - min_valor),3) for valor in data]
            else:
                raise ValueError("Tipo de dato no válido. Se espera un dict o una lista.")

            return data

        #Reescalando o normalizando datos.
        if type_of_scale == "normalized":
            data = normalizar(data)
        elif type_of_scale == "rescale":
            data = reescalar(data, 255, 0)
        elif type_of_scale == "norm_and_res":
            data_norm = normalizar(data)
            data = reescalar(data_norm, max_v="max", min_v="min")
        else:
            print("No es ningun tipo de scale")
        
        return data
    
    def get_sigma(Datos_comp, Datos_Obs):
        sigmas = []
        for clave, lista in Datos_Obs.items():
            if all(num == 0 for num in lista):
                media = 0
                desviacion = 0
            else:
                array = list(lista)
                media = round(np.mean(array),3)
                desviacion = round(np.std(array),3)
                if desviacion != 0:
                    sigmas.append((Datos_comp[clave] - media) / desviacion)
        if not sigmas:
            sigmas.append(0)  
        return sigmas
    
    def getPercentOfCompuInObsStdDev(computational_data, mean_and_stdDev):
        between_stdDev = 0
        for indice, valor in computational_data.items():
            lim_inferior = mean_and_stdDev[indice][0] - mean_and_stdDev[indice][1]  
            lim_superior = mean_and_stdDev[indice][0] + mean_and_stdDev[indice][1]  
            if valor <= lim_superior and valor >= lim_inferior:
                between_stdDev += 1
    
        porcentaje_dentro = round(between_stdDev/len(computational_data) * 100, 3)
        
        return porcentaje_dentro 

    def graficar_scatter(mean_and_stdDev, computational_data):
        indices = [x for x in mean_and_stdDev.keys()]
        promedios = [x[0] for x in mean_and_stdDev.values()]
        promedios = [x/max(promedios) for x in promedios]
        print(promedios)
        desviaciones = [x[1] for x in mean_and_stdDev.values()]

        valores_adicionales = [computational_data[x] for x in indices]
        print(valores_adicionales)
        plt.scatter(promedios, valores_adicionales, c='r', marker='*')
        
        # Graficar promedio
        #plt.axhline(y=prom_obs, color='b', linestyle='--', label = "Mean of means in Obs data")
        #plt.axhline(y=prom_comp, color='r', linestyle='--', label = "Mean Comp data")

        plt.xlabel("Promedio de link en el tiempo")
        plt.ylabel('Ehrenfest con tope')
        plt.title("Probando ehr vs prom")

        # Mostrar etiquetas de índice originales en el eje X
        plt.grid()
        plt.legend()
        plt.show()

    def graficar_con_abajo_y_arriba(mean_and_stdDev, computational_data, name_column):
        indices = [x for x in mean_and_stdDev.keys()]
        promedios = [x[0] for x in mean_and_stdDev.values()]
        desviacion_abajo = [x[2] for x in mean_and_stdDev.values()]
        desviacion_arriba = [x[3] for x in mean_and_stdDev.values()]

        # Graficar puntos adicionales
        valores_adicionales = [computational_data[x] for x in indices]
        plt.scatter(range(1, len(indices) + 1), valores_adicionales, c='r', marker='*', label=str(name_column))
        
        # Configuración de colores
        color_promedio = 'blue'
        color_desviacion = 'gray'  # Color tenue para la zona entre las curvas
        color_fill = 'lightblue'  # Color para rellenar la zona entre las curvas

        # Graficar las curvas
        plt.plot(promedios, color=color_promedio, label='Promedio')
        plt.plot(desviacion_abajo, color=color_desviacion, linestyle='--', label='Desviación Estándar (abajo)')
        plt.plot(desviacion_arriba, color=color_desviacion, linestyle='--', label='Desviación Estándar (arriba)')

        # Rellenar la zona entre las curvas
        plt.fill_between(range(len(promedios)), desviacion_abajo, desviacion_arriba, color=color_fill, alpha=0.5)

        # Configuración del gráfico
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.title('Gráfico de tres curvas')
        plt.legend()

        # Mostrar el gráfico
        plt.show()


    df_obs_data = datos_observacionales

    # Eliminar las columnas que no empiezan con "2023"
    # tomar solo las horas que deseamos
    columns_to_keep = get_column_in_particular_time(df_obs_data.columns)
    df_obs_data = df_obs_data[columns_to_keep]
    

    # Convertir el DataFrame en un dict_obs_data con índice: datos de la fila
    dict_obs_data = df_obs_data.to_dict(orient='index')
    # Modificar el dict_obs_data para tener solo los computational_data de las filas
    dict_obs_data = {indice: datos.values() for indice, datos in dict_obs_data.items()}
    
    #tomar o no los ceros
    dict_obs_data = dell_zeros(dict_obs_data)
    
    
    #Agregando Datos Computacionales
    #computational_data = ComputationaldataFrame.to_dict()[str(name_column_CompData)]
    #computational_data = list(computational_data.values())
    
    #Igualando las escalas 
    dict_obs_data = igualandoEscalas(dict_obs_data, axis=3)
    computational_data = igualandoEscalas(computational_data)

    #convirtiendo en diccionario
    computational_data = {indice: valor for indice, valor in enumerate(computational_data)}

    #Calculo de algunos parametros para medir que tanto se parecen
    mean_and_stdDev = get_mean_and_stdDev(dict_obs_data)
    
    #Promedio de valores computacionales:
    prom_val_comp = np.mean(list(computational_data.values()))
    #promedio de promedio de valores observacionales
    prom_prom_val_obs = np.mean([tupla[0] for tupla in mean_and_stdDev.values()])
    #Sus diferencias de promedios
    means_diference = round(prom_val_comp-prom_prom_val_obs, 3)
    
    sigmas = get_sigma(computational_data, dict_obs_data)
    sgm_max = round(max(sigmas),3)
    sgm_min = round(min(sigmas),3)
    sgm_prom = round(np.mean(sigmas),3)
    
    InsideStdDev = getPercentOfCompuInObsStdDev(computational_data, mean_and_stdDev)
    print(InsideStdDev)
    if graph:
        #graficar(mean_and_stdDev, computational_data, "Hola", prom_prom_val_obs, prom_val_comp)
        graficar_scatter(mean_and_stdDev, computational_data)
        graficar_con_abajo_y_arriba(mean_and_stdDev, computational_data, "Hola")

    elif not graph:
        pass
    else:
        print("No se especifica si graficar o no")

    return InsideStdDev, sgm_prom, sgm_max, sgm_min, means_diference

def getCIInMeanObsDataDistributionWithStdDev_max(datos_observacionales ,computational_data, 
                                            type_of_scale:str = "rescale",
                                            hour = False,
                                            minutes = False,
                                            graph:bool = True,
                                            with_zeros: bool = True):
    """
    Entregamos el dato computacional que queremos comparar y el tipo de calculo que se obtuvo para obtener el dato de un solo link, es decir,
    si se tomó solo el mayor dato dentro del link o un promedio.
    Devuelve un gráfico donde podemos comparar el promedio de valor 
    observacional para cada Link y el valor de indice que necesitemos para cierta hora y minuto.
    
    Nos entrega alguna información relevante sobre la comparación de los datos observacionales y computacionales.

    Args
    ----

        name_column_CompData(str): nombre del indice de centralidad que queremos mostrar.
        
        type_get_obs_link(str): El tipo de valor observacional que se mostrará:
                            - Int: la suma de los computational_data de una calle (borrar luego)
                            - Max: El maximo de los computational_data de una calle
                            - Prom: El promedio de los computational_data de una calle
        
        type_of_scale: Tipo de reescalado que se desea hacer a los datos, para poder hacer una comparación a la misma escala.
                        Podemos elegir entre: ("normalized", "rescale", "norm_and_res").

                        "normalized": Aplicar la norma euclidiana a los datos. (normalizar sobre todos los datos y normalizar por sobre los de un nodo.)
                        "rescale": Se reescala todo suponiendo que 255 es el maximo y 0 el minimo para los datos observacionales. para los
                                    datos computacionales se usa el max y min de la lista.
                        "norm_and_res:  Se aplica ambos, primero normalizamos y luego reescalamos. En este caso se tiene que usar para ambos una reescalación
                                        de min y max.
        
        hour: Hora para la cual queremos acotar los datos observacionales. (0-23)
        
        minute: por si queremos acotar los datos en minutos (0,15,30,45)
        
        graph: True or False si queremos obtener el grafico o no.

        max_v = max: valor maximo que se toma para reescalar(x) x -> 1
        
        min_v = min: valor minimo para reescalar(y) y -> 0

        with_zeros (bool): True para calcular con los computational_data que son 0 para los datos observacionales, que suelen ser muchos.
                            False para no usarlos. 
        

    Return:
    -------
        -Gráfico.
        -InsideStdDev, sgm_prom, sgm_max, sgm_min, means_diference
    """
    def dell_zeros(diccionario):
        """
        Por si quiero eliminar los ceros, es decir, cuando no hay taco.
        """
        dict_sin_ceros = {}
        if with_zeros == True:
            return diccionario
        elif with_zeros == False:
            for indice, lista in diccionario.items():
                lista_sin_ceros = [valor for valor in lista if valor != 0]
                if not lista_sin_ceros:  # Verificar si la lista está vacía
                    lista_sin_ceros.append(0)
                dict_sin_ceros[indice] = lista_sin_ceros 
            return dict_sin_ceros
        
    def get_column_in_particular_time(columnas) -> list:
        """
        En caso de acotar a ciertas horas y minutos los datos observacionales. Nos devuelve una lista con las columnas que corresponden.
        """
        columns_to_keep = []
        hora = hour
        minutos = minutes
        if hora == False:
            columns_to_keep = [col for col in columnas if col.startswith("/2023")]     
        elif hora != False and minutos == False:
            try:
                hora = str(hour).zfill(2)
                # Expresión regular para el formato de nombre de archivo especificado
                regex = re.compile(rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}\.png')
                for archivo in columnas:
                    if regex.match(archivo):
                        columns_to_keep.append(archivo)
            except FileNotFoundError:
                print(f"No encuentro archivos de esta forma:", rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}\.png')
        elif hora != False and minutos != False:
            try:
                hora = str(hour).zfill(2)
                minutos = str(minutes).zfill(2)
                # Expresión regular para el formato de nombre de archivo especificado
                regex = re.compile(rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-{minutos}\.png')
                for archivo in columnas:
                    if regex.match(archivo):
                        columns_to_keep.append(archivo)
            except FileNotFoundError:
                print(f"No encuentro archivos de esta forma:", rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-{minutos}\.png')
        else:
            print("Problemas con encontrar columnas en horas y minutos indicados.")
    
        
        return columns_to_keep

    def get_mean_and_stdDev(dict_obs_data):
        maximos = []
        
        for indice, lista in dict_obs_data.items():
            array = list(lista)
            maximo = round(max(array),3)
            maximos.append((indice, maximo))


        # Ordenar por promedio
        maximos.sort(key=lambda x: x[1])
        maximos = {indice: valor1 for indice, valor1 in maximos}
        
        return maximos

    def igualandoEscalas(data, axis = 3):
        """
        Para poder comparar los datos necesitamos reescalar los datos para que tenga lógica comparar los datos
        computacionales con los observacionales.

        Hay 3 formas de normalizar: 
            1. Normalizar todos los datos de un nodo.
            2. Normalizar un nodo con respecto a todos los datos de todos los nodos dada una sola imagen.
            3. Normalizar un nodo con respecto a todos los datos de todos los nodos de todas las imagenes 
        
        Las 3 formas son solo para los datos observacionales, para el caso de los datos computacionales solo tenemos una lista,
        así que se hace de la forma 2. 
        Args:
        -----
        axis: 1,2,3, son las formas de normalizar los datos.
        """
        def normalizar(data):
            
            Cantidad_de_nodos_con_norma_nula = 0
            #Para datos observacionales
            if isinstance(data, dict):
                if axis == 1:
                    for N_nodo, lista in data.items():
                        # Calcular la norma euclidiana de la lista
                        norma = math.sqrt(sum([x**2 for x in lista]))
                        if norma == 0:
                            data[N_nodo] = [0]
                            Cantidad_de_nodos_con_norma_nula +=1
                        else:
                            data[N_nodo]= [round(x / norma, 3) for x in lista]
                elif axis == 2:
                    # Obtener todas las posiciones presentes en las listas del diccionario
                    posiciones = set()
                    for lista in data.values():
                        posiciones.update(range(len(lista)))
                    

                    # Normalizar euclidianamente todas las posiciones de las listas
                    elementos_normalizados = []
                    for posicion in posiciones:
                        elementos = [list(lista)[posicion] for lista in data.values()]
                        elementos_normalizados.append( normalize([elementos], norm='l2')[0])
                        print(elementos_normalizados)
                    # Asignar los elementos normalizados de vuelta al diccionario en las posiciones correspondientes
                    
                    new_data = {}
                    for indice  in range(len(elementos_normalizados[0])):
                        lista = []
                        for posicion in posiciones:
                            lista = [i[posicion] for i in elementos_normalizados]
                        new_data[indice] = lista
                    
                    data = new_data
                    
                elif axis == 3:
                    todos = np.concatenate([list(lista) for lista in data.values()])
                    norma = np.linalg.norm(todos)
                    for indice, lista in data.items():
                        lista_normalisada = [i/norma for i in lista]
                        data[indice] = lista_normalisada
                else:
                    print("no se está eligiendo ningun tipo de normalización.")
            
            #para una lista
            elif isinstance(data, list):
                norma = math.sqrt(sum([x**2 for x in data]))
                data = [round(x / norma, 3) for x in data]
            else:
                raise ValueError("Para normalizar necesitamos que sea un diccionario o una lista.")
            return data
            
        def reescalar(data, max_v, min_v):
            if isinstance(data, dict):  # Verificar si es un dict_obs_data #Para los datos obs.
                if axis == 1:
                    for clave, lista in data.items():
                        max_valor = max(lista) if str(max_v) == "max" else float(max_v)
                        min_valor = min(lista) if str(min_v) == "min" else float(min_v)
                                
                        if min_valor == max_valor:
                            data[clave] = lista ### hay que revisar si es bueno dejar asi las listas, pues pede que sirva solo si son ambos 0
                        else:
                            data[clave] = [round((float(valor) - min_valor)/(max_valor - min_valor),3) for valor in lista]
                elif axis == 2:
                    # Obtener todas las posiciones presentes en las listas del diccionario
                    posiciones = set()
                    for lista in data.values():
                        posiciones.update(range(len(lista)))

                    elementos_escalados = []
                    # Normalizar euclidianamente todas las posiciones de las listas
                    for posicion in posiciones:
                        elementos = [lista[posicion] for lista in data.values()]
                        max_valor = max(elementos)
                        min_valor = min(elementos)
                        elementos_escalados.append([round((float(valor) - min_valor)/(max_valor - min_valor),3) for valor in elementos])
                    # Asignar los elementos normalizados de vuelta al diccionario en las posiciones correspondientes
                    new_data = {}
                    for indice  in range(len(elementos_escalados[0])):
                        lista = []
                        for posicion in posiciones:
                            lista = [i[posicion] for i in elementos_escalados]
                        new_data[indice] = lista
                    
                    data = new_data
                
                elif axis == 3:
                    todos = np.concatenate([list(lista) for lista in data.values()])
                    max_valor = max(todos) if str(max_v) == "max" else float(max_v)
                    min_valor = min(todos) if str(min_v) == "min" else float(min_v)            
                    for indice, lista in data.items():
                        lista_reescalada = [(i-min_valor)/(max_valor - min_valor) for i in lista]
                        data[indice] = lista_reescalada
                
                else:
                    print("No se tomó ningun eje en el cual reescalar")
            
            elif isinstance(data, list):  # Verificar si es una lista #Este se ocupara para los datos comp.
                max_valor = max(data)
                min_valor = min(data)
                
                if min_valor == 0 and max_valor == 0:
                    pass
                else:
                    data = [round((valor - min_valor) / (max_valor - min_valor),3) for valor in data]
            else:
                raise ValueError("Tipo de dato no válido. Se espera un dict o una lista.")

            return data

        #Reescalando o normalizando datos.
        if type_of_scale == "normalized":
            data = normalizar(data)
        elif type_of_scale == "rescale":
            data = reescalar(data, 255, 0)
        elif type_of_scale == "norm_and_res":
            data_norm = normalizar(data)
            data = reescalar(data_norm, max_v="max", min_v="min")
        else:
            print("No es ningun tipo de scale")
        
        return data
    
    def get_sigma(Datos_comp, Datos_Obs):
        sigmas = []
        for clave, lista in Datos_Obs.items():
            if all(num == 0 for num in lista):
                media = 0
                desviacion = 0
            else:
                array = list(lista)
                media = round(np.mean(array),3)
                desviacion = round(np.std(array),3)
                if desviacion != 0:
                    sigmas.append((Datos_comp[clave] - media) / desviacion)
        if not sigmas:
            sigmas.append(0)  
        return sigmas
    
    def getPercentOfCompuInObsStdDev(computational_data, mean_and_stdDev):
        between_stdDev = 0
        for indice, valor in computational_data.items():
            lim_inferior = mean_and_stdDev[indice][0] - mean_and_stdDev[indice][1]  
            lim_superior = mean_and_stdDev[indice][0] + mean_and_stdDev[indice][1]  
            if valor <= lim_superior and valor >= lim_inferior:
                between_stdDev += 1
    
        porcentaje_dentro = round(between_stdDev/len(computational_data) * 100, 3)
        
        return porcentaje_dentro 

    def graficar_scatter(mean_and_stdDev, computational_data):
        indices = [x for x in mean_and_stdDev.keys()]
        promedios = [x[0] for x in mean_and_stdDev.values()]
        promedios = [x/max(promedios) for x in promedios]
        print(promedios)

        valores_adicionales = [computational_data[x] for x in indices]
        print(valores_adicionales)
        plt.scatter(promedios, valores_adicionales, c='r', marker='*')
        
        # Graficar promedio
        #plt.axhline(y=prom_obs, color='b', linestyle='--', label = "Mean of means in Obs data")
        #plt.axhline(y=prom_comp, color='r', linestyle='--', label = "Mean Comp data")

        plt.xlabel("Promedio de link en el tiempo")
        plt.ylabel('Ehrenfest con tope')
        plt.title("Probando ehr vs prom")

        # Mostrar etiquetas de índice originales en el eje X
        plt.grid()
        plt.legend()
        plt.show()

    def graficar_con_abajo_y_arriba(mean_and_stdDev, computational_data, name_column):
        indices = [x for x in mean_and_stdDev.keys()]
        promedios = [x[0] for x in mean_and_stdDev.values()]

        # Graficar puntos adicionales
        valores_adicionales = [computational_data[x] for x in indices]
        plt.scatter(range(1, len(indices) + 1), valores_adicionales, c='r', marker='*', label=str(name_column))
        
        # Configuración de colores
        color_promedio = 'blue'
   
        # Graficar las curvas
        plt.plot(promedios, color=color_promedio, label='Promedio')

        # Configuración del gráfico
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.title('Gráfico de tres curvas')
        plt.legend()

        # Mostrar el gráfico
        plt.show()


    df_obs_data = datos_observacionales

    # Eliminar las columnas que no empiezan con "2023"
    # tomar solo las horas que deseamos
    columns_to_keep = get_column_in_particular_time(df_obs_data.columns)
    df_obs_data = df_obs_data[columns_to_keep]
    

    # Convertir el DataFrame en un dict_obs_data con índice: datos de la fila
    dict_obs_data = df_obs_data.to_dict(orient='index')
    # Modificar el dict_obs_data para tener solo los computational_data de las filas
    dict_obs_data = {indice: datos.values() for indice, datos in dict_obs_data.items()}
    
    #tomar o no los ceros
    dict_obs_data = dell_zeros(dict_obs_data)
    
    
    #Agregando Datos Computacionales
    #computational_data = ComputationaldataFrame.to_dict()[str(name_column_CompData)]
    #computational_data = list(computational_data.values())
    
    #Igualando las escalas 
    dict_obs_data = igualandoEscalas(dict_obs_data, axis=3)
    computational_data = igualandoEscalas(computational_data)

    #convirtiendo en diccionario
    computational_data = {indice: valor for indice, valor in enumerate(computational_data)}

    #Calculo de algunos parametros para medir que tanto se parecen
    mean_and_stdDev = get_mean_and_stdDev(dict_obs_data)
    
    #Promedio de valores computacionales:
    prom_val_comp = np.mean(list(computational_data.values()))
    #promedio de promedio de valores observacionales
    prom_prom_val_obs = np.mean([tupla[0] for tupla in mean_and_stdDev.values()])
    #Sus diferencias de promedios
    means_diference = round(prom_val_comp-prom_prom_val_obs, 3)
    
    sigmas = get_sigma(computational_data, dict_obs_data)
    sgm_max = round(max(sigmas),3)
    sgm_min = round(min(sigmas),3)
    sgm_prom = round(np.mean(sigmas),3)
    
    InsideStdDev = getPercentOfCompuInObsStdDev(computational_data, mean_and_stdDev)
    print(InsideStdDev)
    if graph:
        #graficar(mean_and_stdDev, computational_data, "Hola", prom_prom_val_obs, prom_val_comp)
        graficar_scatter(mean_and_stdDev, computational_data)
        graficar_con_abajo_y_arriba(mean_and_stdDev, computational_data, "Hola")

    elif not graph:
        pass
    else:
        print("No se especifica si graficar o no")

    return InsideStdDev, sgm_prom, sgm_max, sgm_min, means_diference


#BASICO NODOS

observacional = pd.read_csv("data/DataImages/In_Intersection_Coord/Normal/intersectionCoord_basic.csv")
computacional = pd.read_csv("data/DataNetwork/InterAsNode/Basic_and_advaced_data_network_nodes.csv")

data_BC = list(computacional["CC"])


getCIInMeanObsDataDistributionWithStdDev_max(observacional, data_BC)