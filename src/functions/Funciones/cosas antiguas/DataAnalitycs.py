import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import re
import ast
from sklearn.preprocessing import normalize
from datetime import datetime, timedelta

class NetworkComparisonNodes:
    def __init__(self, path_file_Network_data_computation:str, path_file_Network_data_images:str) -> None:
        self.ComputationaldataFrame = pd.read_csv(str(path_file_Network_data_computation))
        self.ObservacionaldataFrame = pd.read_csv(str(path_file_Network_data_images))
        # Ordena las columnas en orden cronológico
        self.ObservacionaldataFrame = self.ObservacionaldataFrame.sort_index(axis=1)
        self.ComputationaldataFrame = self.ComputationaldataFrame.sort_index(axis=1)
    
    def getDistributionForTrafficForNode(self, number_of_node: int):

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

        data_for_obserb = self.ObservacionaldataFrame.iloc[number_of_node]
        columns_to_keep =  [col for col in data_for_obserb.index if col.startswith("/2023")] 
        columns_complete_to_keep = obtener_instantes_faltantes(columns_to_keep[0], columns_to_keep[-1])
        valores_de_nodo = []
        for col in columns_complete_to_keep:
            if col in columns_to_keep:
                valores_de_nodo.append(data_for_obserb[col])
            elif col not in columns_to_keep:
                valores_de_nodo.append(np.nan)
            else:
                print("Slgo malo pasa")

        columns_complete_to_keep = columns_complete_to_keep[:1000]
        valores_de_nodo = valores_de_nodo[:1000]
        # Crear el gráfico de la fila
        #plt.scatter(tiempo, col_for_integral)
        plt.plot(columns_complete_to_keep, valores_de_nodo)
        #plt.scatter(tiempo, col_for_promedios)
        plt.xlabel('Columnas')
        plt.ylabel('Valores')
        plt.xticks([0,200,500,900])
        plt.title(f'Gráfico de computational_data para la fila {number_of_node}')
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
        plt.show()
        
    def getDistributionForTrafficForSumOfAll(self, file_name_of_sum_colors):

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

        data_for_obserb = pd.read_csv(file_name_of_sum_colors)
        columns_to_keep =  [col for col in data_for_obserb["nombre"] if col.startswith("/2023")] 
        columns_complete_to_keep = obtener_instantes_faltantes(columns_to_keep[0], columns_to_keep[-1])
        valores_de_nodo = []
        count = 0
        for col in columns_complete_to_keep:
            if col in columns_to_keep:
                valores_de_nodo.append((data_for_obserb["63"]+data_for_obserb["127"]+data_for_obserb["191"]+data_for_obserb["255"])[count])
                count +=1
            elif col not in columns_to_keep:
                valores_de_nodo.append(np.nan)
            else:
                print("Slgo malo pasa")
        print(valores_de_nodo)
        # Crear el gráfico de la fila
        #plt.scatter(tiempo, col_for_integral)
        plt.plot(columns_complete_to_keep, valores_de_nodo)
        #plt.scatter(tiempo, col_for_promedios)
        plt.xlabel('Columnas')
        plt.ylabel('Valores')
        plt.xticks([])
        plt.title(f'Gráfico de computational_data para la fila')
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
        plt.show()

        from statsmodels.tsa.arima.model import ARIMA

        # Rellena los valores faltantes con NaN
        df = pd.DataFrame(valores_de_nodo, columns=['Valor'])

        # Genera un índice de tiempo equidistante
        df['Fecha'] = pd.date_range(start='2023-03-29', periods=len(df), freq='D')

        # Establece el índice de tiempo como el índice del DataFrame
        df.set_index('Fecha', inplace=True)

        # Rellena los valores faltantes utilizando un modelo ARIMA
        model = ARIMA(df['Valor'], order=(1, 0, 0))  # Configura el orden del modelo ARIMA
        model_fit = model.fit()
        df['Valor'] = model_fit.predict(start=0, end=len(df)-1)

        # Grafica los datos originales y la predicción
        plt.plot(df.index, df['Valor'], label='Predicción')
        plt.scatter(df.index, df['Valor'], label='Datos originales', color='red')
        plt.xlabel('Fecha')
        plt.ylabel('Valor')
        plt.title('Predicción utilizando modelo ARIMA')
        plt.legend()
        plt.show()

    def getDistributionForTraffucForHourInAllNodes(self, file_name_of_sum_colors):

        def get_column_in_particular_time(columnas, hour, minutes) -> list:
            """
            En caso de acotar a ciertas horas y minutos los datos observacionales. Nos devuelve una lista con las columnas que corresponden.
            """
            columns_to_keep = []
            hora = hour
            minutos = minutes
            if hora is False:
                columns_to_keep = [col for col in columnas if col.startswith("/2023")]     
            elif hora is not False and minutos is False:
                try:
                    hora = str(hour).zfill(2)
                    # Expresión regular para el formato de nombre de archivo especificado
                    regex = re.compile(rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}')
                    for archivo in columnas:
                        if regex.match(archivo):
                            columns_to_keep.append(archivo)
                except FileNotFoundError:
                    print(f"No encuentro archivos de esta forma:", rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}')

            return columns_to_keep

        def calcular_sumas(dataframe, nombres):
            # Filtrar el dataframe por los nombres especificados
            subconjunto = dataframe.loc[nombres]
            
            # Calcular la suma de las columnas para cada nombre
            sumas = subconjunto.sum(axis=0).tolist()

            return sumas
        def generar_grafico_caja(numeros, repeticiones):
            data = []
            for numero, repeticion in zip(numeros, repeticiones):
                data.extend([numero] * repeticion)
            
            plt.boxplot(data)
            plt.xlabel('Número')
            plt.ylabel('Repeticiones')
            plt.title('Gráfico de Caja')
            plt.show()

        data_for_obserb = pd.read_csv(file_name_of_sum_colors)
        data_for_obserb.set_index("nombre", inplace=True)
        columns_to_keep =  [col for col in data_for_obserb.index if col.startswith("/2023")] 
        
        probando_hora = get_column_in_particular_time(columns_to_keep, 20, False)
        
        frecuencias = calcular_sumas(data_for_obserb, probando_hora)
        generar_grafico_caja([127, 191, 255], frecuencias[1:])

    def getCIInMeanObsDataDistributionWithStdDev(self, 
                                                name_column_CompData: str,
                                                type_of_scale:str = "rescale",
                                                hour = False,
                                                minutes = False,
                                                graph:bool = True,
                                                max_v = 255,
                                                min_v = 0,
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
            if hora is False:
                columns_to_keep = [col for col in columnas if col.startswith("/2023")]     
            elif hora is not False and minutos is False:
                print("HOla")
                try:
                    hora = str(hour).zfill(2)
                    # Expresión regular para el formato de nombre de archivo especificado
                    regex = re.compile(rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}')
                    for archivo in columnas:
                        if regex.match(archivo):
                            columns_to_keep.append(archivo)
                except FileNotFoundError:
                    print(f"No encuentro archivos de esta forma:", rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}')
            elif hora is not False and minutos is not False:
                try:

                    hora = str(hour).zfill(2)
                    minutos = str(minutes).zfill(2)
                    # Expresión regular para el formato de nombre de archivo especificado
                    regex = re.compile(rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-{minutos}')
                    for archivo in columnas:
                        if regex.match(archivo):
                            columns_to_keep.append(archivo)
                except FileNotFoundError:
                    print(f"No encuentro archivos de esta forma:", rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-{minutos}')
            else:
                print("Problemas con encontrar columnas en horas y minutos indicados.")
       
            
            return columns_to_keep

        def get_mean_and_stdDev(dict_obs_data):
            mean_and_stdDev = []
            son_solo_ceros = 0
            for indice, lista in dict_obs_data.items():
                array = list(lista)
                promedio = round(np.mean(array),3)
                desviacion = round(np.std(array),3)
                mean_and_stdDev.append((indice, promedio, desviacion))

            # Ordenar por promedio
            mean_and_stdDev.sort(key=lambda x: x[1])
            mean_and_stdDev = {indice: (valor1, valor2) for indice, valor1, valor2 in mean_and_stdDev}
            
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
 
        def graficar(mean_and_stdDev, computational_data, name_column, prom_obs, prom_comp):
            indices = [x for x in mean_and_stdDev.keys()]
            promedios = [x[0] for x in mean_and_stdDev.values()]
            desviaciones = [x[1] for x in mean_and_stdDev.values()]

            plt.errorbar(range(1, len(indices) + 1), promedios, yerr=desviaciones, fmt='o', capsize=5, label='Promedio y Desviación Estándar')

            # Graficar puntos adicionales
            valores_adicionales = [computational_data[x] for x in indices]
            plt.scatter(range(1, len(indices) + 1), valores_adicionales, c='r', marker='*', label=str(name_column))
            
            # Graficar promedio
            plt.axhline(y=prom_obs, color='b', linestyle='--', label = "Mean of means in Obs data")
            plt.axhline(y=prom_comp, color='r', linestyle='--', label = "Mean Comp data")

            plt.xlabel("Number of Link")
            plt.ylabel('Centrality Index and Obs Value')
            plt.title('Mean Obs With Std Dev and Index of '+ str(name_column))

            # Mostrar etiquetas de índice originales en el eje X
            plt.xticks(range(1, len(indices) + 1), indices)
            plt.grid()
            plt.legend()
            plt.show()

        #Eligiendo tipo de dato observacional
        df_obs_data = self.ObservacionaldataFrame
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
        computational_data = self.ComputationaldataFrame.to_dict()[str(name_column_CompData)]
        computational_data = list(computational_data.values())
    
        #Igualando las escalas 
        dict_obs_data = igualandoEscalas(dict_obs_data, axis=3)
        computational_data = igualandoEscalas(computational_data)
        
        #convirtiendo en diccionario
        computational_data = {indice: valor for indice, valor in enumerate(computational_data)}
        #Calculo de algunos parametros para medir que tanto se parecen
        mean_and_stdDev = get_mean_and_stdDev(dict_obs_data)
        print("HOLA")
        
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
            graficar(mean_and_stdDev, computational_data, name_column_CompData, prom_obs= prom_prom_val_obs, prom_comp= prom_val_comp)
        elif not graph:
            pass
        else:
            print("No se especifica si graficar o no")

        return InsideStdDev, sgm_prom, sgm_max, sgm_min, means_diference
    
    def getCIInMeanObsDataDistributionWithStdDev2(self, 
                                                name_column_CompData: str,
                                                type_of_scale:str = "rescale",
                                                hour = False,
                                                minutes = False,
                                                graph:bool = True,
                                                max_v = 255,
                                                min_v = 0,
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
            if hora is False:
                columns_to_keep = [col for col in columnas if col.startswith("/2023")]     
            elif hora is not False and minutos is False:
                print("HOla")
                try:
                    hora = str(hour).zfill(2)
                    # Expresión regular para el formato de nombre de archivo especificado
                    regex = re.compile(rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}')
                    for archivo in columnas:
                        if regex.match(archivo):
                            columns_to_keep.append(archivo)
                except FileNotFoundError:
                    print(f"No encuentro archivos de esta forma:", rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-\d{{2}}')
            elif hora is not False and minutos is not False:
                try:

                    hora = str(hour).zfill(2)
                    minutos = str(minutes).zfill(2)
                    # Expresión regular para el formato de nombre de archivo especificado
                    regex = re.compile(rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-{minutos}')
                    for archivo in columnas:
                        if regex.match(archivo):
                            columns_to_keep.append(archivo)
                except FileNotFoundError:
                    print(f"No encuentro archivos de esta forma:", rf'/\d{{4}}-\d{{2}}-\d{{2}}_{hora}-{minutos}')
            else:
                print("Problemas con encontrar columnas en horas y minutos indicados.")
       
            
            return columns_to_keep

        def get_mean_and_stdDev(dict_obs_data):
            def calcular_desviacion_estandar(lista, promedio):
                diferencias = np.array(lista) - promedio
                diferencias_cuadrado = diferencias ** 2
                varianza = np.mean(diferencias_cuadrado)
                desviacion_estandar = np.sqrt(varianza)
                return desviacion_estandar
            
            """Probando
            numero_referencia = 6 
            dev1 = calcular_desviacion_estandar([1,2], numero_referencia)
            dev2 = calcular_desviacion_estandar([7,7], numero_referencia)
            print(dev1)
            print(dev2)
            """


            
            mean_and_stdDev = []
            for indice, lista in dict_obs_data.items():
                array = list(lista)
                promedio = round(np.mean(array),3)
                lista_up = [i for i in lista if i > promedio]
                lista_down = [i for i in lista if i < promedio]
                desviacion_abajo = calcular_desviacion_estandar(lista_down, promedio)
                desviacion_abajo = promedio - desviacion_abajo
                desviacion_arriba = calcular_desviacion_estandar(lista_up, promedio)
                desviacion_arriba = promedio + desviacion_abajo
                mean_and_stdDev.append((indice, promedio, desviacion_abajo, desviacion_arriba))

            # Ordenar por promedio
            mean_and_stdDev.sort(key=lambda x: x[1])
            mean_and_stdDev = {indice: (valor1, valor2, valor3) for indice, valor1, valor2, valor3 in mean_and_stdDev}
            
            
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
 
        def graficar(mean_and_stdDev, computational_data, name_column, prom_obs, prom_comp):
            indices = [x for x in mean_and_stdDev.keys()]
            promedios = [x[0] for x in mean_and_stdDev.values()]
            desviacion_abajo = [x[1] for x in mean_and_stdDev.values()]
            desviacion_arriba = [x[2] for x in mean_and_stdDev.values()]

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


        #Eligiendo tipo de dato observacional
        df_obs_data = self.ObservacionaldataFrame
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
        computational_data = self.ComputationaldataFrame.to_dict()[str(name_column_CompData)]
        computational_data = list(computational_data.values())
    
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
        if graph:
            graficar(mean_and_stdDev, computational_data, name_column_CompData, prom_obs= prom_prom_val_obs, prom_comp= prom_val_comp)
        elif not graph:
            pass
        else:
            print("No se especifica si graficar o no")

        return InsideStdDev, sgm_prom, sgm_max, sgm_min, means_diference
   
    def getCaracteristicas(self, 
                            name_column_CompData = None,
                            type_of_scale = None,
                            hour = None,
                            minutes = None,
                            graph = None,
                            max_v = None,
                            min_v = None,
                            with_zeros = None):
        

        if type_of_scale is  None:
            type_of_scale = "rescale"
        if minutes is  None:
            minutes = False
        if graph  is None:
            graph = True
        if max_v  is None:
            max_v = 255
        if min_v is  None:
            min_v = 0
        if with_zeros is  None:
            with_zeros = True


        def graficar(porcentaje, mean_sigma, means_diference):
            horas = range(len(porcentaje) - 1)
            fig, ax1 = plt.subplots()
            ax1.plot(horas, porcentaje[:-1],'b-')
            ax1.set_ylabel('Porcentaje', color='b')
            ax1.tick_params('y', colors='b')
            ax1.axhline(porcentaje[-1], color='b', linestyle='--', label = "Mean of means in Obs data")
            # Invertir el eje Y

            ax2 = ax1.twinx()
            ax2.plot(horas, means_diference[:-1],'r-')
            #ax2.plot(horas, mean_sigma[:-1],'k-')
            ax2.set_ylabel('Diferencia', color='r')
            ax2.tick_params('y', colors='r')
            ax2.invert_yaxis()
            ax2.axhline(means_diference[-1], color='r', linestyle='--', label = "Mean of Comp data")

            # Graficar el total de horas

            plt.title('Obs vs '+ str(name_column_CompData))
            plt.grid()
            plt.xticks(horas)
            plt.legend()
            plt.show()
        def graficar_all(porcentaje, mean_sigma, means_diference):
            
            horas = range(len(porcentajes[0]) - 1)

            y1 = porcentaje[0][:-1]
            y1_extra1 = porcentaje[1][:-1]
            y1_extra2 = porcentaje[2][:-1]
            y1_extra3 = porcentaje[3][:-1]

            y2 = means_diference[0][:-1]
            y2_extra1 = means_diference[1][:-1]
            y2_extra2 = means_diference[2][:-1]
            y2_extra3 = means_diference[3][:-1]

            fig, ax1 = plt.subplots()
            # Configurar el primer plot en el lado izquierdo
            color_ax1 = 'b'  # Color para las curvas en ax1
            ax1.plot(horas, y1, color_ax1 + '-', label='EBC_Conv')
            ax1.plot(horas, y1_extra1, color_ax1 + '--', label='New_EBC')
            ax1.plot(horas, y1_extra2, color_ax1 + '-.', label='New_ECC')
            ax1.plot(horas, y1_extra3, color_ax1 + ':', label='New_EDC')

            ax1.set_xlabel('Eje X')
            ax1.set_ylabel('Porcentaje comp dentro de stdDEv', color=color_ax1)
            ax1.tick_params('y', colors=color_ax1)

            # Crear el segundo plot y compartir el eje X con el primer plot
            ax2 = ax1.twinx()

            color_ax2 = 'r'  # Color para las curvas en ax2
            ax2.plot(horas, y2, color_ax2 + '-', label='EBC_Conv')
            ax2.plot(horas, y2_extra1, color_ax2 + '--', label='New_EBC')
            ax2.plot(horas, y2_extra2, color_ax2 + '-.', label='New_ECC')
            ax2.plot(horas, y2_extra3, color_ax2 + ':', label='Curva 4')
            ax2.invert_yaxis()
            ax2.set_ylabel("Diferencia entre promedios", color=color_ax2)
            ax2.tick_params('y', colors=color_ax2)

            # Mostrar leyendas
            handles, labels = ax1.get_legend_handles_labels()
            ax1.legend(labels, loc='upper left')

            plt.title("Obs vs CI" )
            plt.grid()
            plt.xticks(horas)

            # Mostrar el gráfico
            plt.show()
        porcentajes = []
        means_sigma = []
        means_diference = []
        for name in ["DiBC", "DiCC", "DiDC", "BC"]:
            porcentaje_OneName = []
            mean_sigma_OneName = []
            means_diference_OneName = []
            for i in range(25):
                if i < 24:
                    i_str = str(i).zfill(2)
                else:
                    i_str = False            
                
                result = self.getCIInMeanObsDataDistributionWithStdDev( name,
                                                                        type_of_scale,
                                                                        i_str,
                                                                        minutes,
                                                                        graph,
                                                                        max_v,
                                                                        min_v,
                                                                        with_zeros)
                porcentaje_OneName.append(result[0])
                mean_sigma_OneName.append(result[1])
                means_diference_OneName.append(result[4])
            porcentajes.append(porcentaje_OneName)
            means_sigma.append(mean_sigma_OneName)
            means_diference.append(means_diference_OneName)

        graficar_all(porcentajes, means_sigma, means_diference)

class NetworkComparisonEdges:
    def __init__(self, path_file_Network_data_computation:str, path_file_Image_data_observational:str) -> None:
        self.ComputationaldataFrame = pd.read_csv(str(path_file_Network_data_computation))
        self.ObservationaldataFrame = pd.read_csv(str(path_file_Image_data_observational))
        # Ordena las columnas en orden cronológico
        self.ObservationaldataFrame = self.ObservationaldataFrame.sort_index(axis=1)

    
    def getDistributionForTrafficForEdge(self, number_of_node: int):

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

        data_for_obserb = self.ObservacionaldataFrame.iloc[number_of_node]
        columns_to_keep =  [col for col in data_for_obserb.index if col.startswith("/2023")] 
        columns_complete_to_keep = obtener_instantes_faltantes(columns_to_keep[0], columns_to_keep[-1])
        valores_de_nodo = []
        for col in columns_complete_to_keep:
            if col in columns_to_keep:
                valores_de_nodo.append(data_for_obserb[col])
            elif col not in columns_to_keep:
                valores_de_nodo.append(np.nan)
            else:
                print("Slgo malo pasa")

        columns_complete_to_keep = columns_complete_to_keep[:1000]
        valores_de_nodo = valores_de_nodo[:1000]
        # Crear el gráfico de la fila
        #plt.scatter(tiempo, col_for_integral)
        plt.plot(columns_complete_to_keep, valores_de_nodo)
        #plt.scatter(tiempo, col_for_promedios)
        plt.xlabel('Columnas')
        plt.ylabel('Valores')
        plt.xticks([0,200,500,900])
        plt.title(f'Gráfico de computational_data para la fila {number_of_node}')
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
        plt.show()
        

    def getCIInMeanObsDataDistributionWithStdDev(self, 
                                                name_column_CompData: str,
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
        def getMax(dataFrame):
            for columna in dataFrame.columns:
                if columna.startswith('/2023'):
                    dataFrame[columna] = dataFrame[columna].apply(lambda lista: np.max(ast.literal_eval(lista)))
            
            return dataFrame
        def getMean(dataFrame):
            
            for columna in dataFrame.columns:
                if columna.startswith('/2023'):
                    dataFrame[columna] = dataFrame[columna].apply(lambda lista: np.mean(ast.literal_eval(lista)))
            
            return dataFrame


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
 
        def graficar(mean_and_stdDev, computational_data, name_column, prom_obs, prom_comp):
            indices = [x for x in mean_and_stdDev.keys()]
            promedios = [x[0] for x in mean_and_stdDev.values()]
            desviaciones = [x[1] for x in mean_and_stdDev.values()]

            plt.errorbar(range(1, len(indices) + 1), promedios, yerr=desviaciones, fmt='o', capsize=5, label='Promedio y Desviación Estándar')

            # Graficar puntos adicionales
            valores_adicionales = [computational_data[x] for x in indices]
            plt.scatter(range(1, len(indices) + 1), valores_adicionales, c='r', marker='*', label=str(name_column))
            
            # Graficar promedio
            plt.axhline(y=prom_obs, color='b', linestyle='--', label = "Mean of means in Obs data")
            plt.axhline(y=prom_comp, color='r', linestyle='--', label = "Mean Comp data")

            plt.xlabel("Number of Link")
            plt.ylabel('Centrality Index and Obs Value')
            plt.title('Mean Obs With Std Dev and Index of '+ str(name_column))

            # Mostrar etiquetas de índice originales en el eje X
            plt.xticks(range(1, len(indices) + 1), indices)
            plt.grid()
            plt.legend()
            plt.show()

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

        #Eligiendo tipo de dato observacional
        """
        if type_get_obs_link == "Max":
            df_obs_data = getMax(self.ObservationaldataFrame)
            df_obs_data.to_csv("MaxObsData.csv")
        elif type_get_obs_link == "Mean":
            df_obs_data = getMean(self.ObservationaldataFrame)    
            df_obs_data.to_csv("MeanObsData.csv")
        """
        
        df_obs_data = self.ObservationaldataFrame

        # Eliminar las columnas que no empiezan con "2023"
        # tomar solo las horas que deseamos
        columns_to_keep = get_column_in_particular_time(df_obs_data.columns)
        print(columns_to_keep)
        df_obs_data = df_obs_data[columns_to_keep]
        

        # Convertir el DataFrame en un dict_obs_data con índice: datos de la fila
        dict_obs_data = df_obs_data.to_dict(orient='index')
        # Modificar el dict_obs_data para tener solo los computational_data de las filas
        dict_obs_data = {indice: datos.values() for indice, datos in dict_obs_data.items()}
        
        #tomar o no los ceros
        dict_obs_data = dell_zeros(dict_obs_data)
        
        
        #Agregando Datos Computacionales
        computational_data = self.ComputationaldataFrame.to_dict()[str(name_column_CompData)]
        computational_data = list(computational_data.values())
        
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
            graficar(mean_and_stdDev, computational_data, "Hola", prom_prom_val_obs, prom_val_comp)
            graficar_scatter(mean_and_stdDev, computational_data)
            graficar_con_abajo_y_arriba(mean_and_stdDev, computational_data, "Hola")

        elif not graph:
            pass
        else:
            print("No se especifica si graficar o no")

        return InsideStdDev, sgm_prom, sgm_max, sgm_min, means_diference
    
    def getCaracteristicas(self, 
                            name_column_CompData = None,
                            type_get_obs_link = None,
                            type_of_scale = None,
                            hour = None,
                            minutes = None,
                            graph = None,
                            max_v = None,
                            min_v = None,
                            with_zeros = None):
        

        if type_get_obs_link is  None:
            type_get_obs_link = "Max"
        if type_of_scale is  None:
            type_of_scale = "rescale"
        if minutes is  None:
            minutes = False
        if graph  is None:
            graph = True
        if max_v  is None:
            max_v = 255
        if min_v is  None:
            min_v = 0
        if with_zeros is  None:
            with_zeros = True


        def graficar(porcentaje, mean_sigma, means_diference):
            horas = range(len(porcentaje) - 1)
            fig, ax1 = plt.subplots()
            ax1.plot(horas, porcentaje[:-1],'b-')
            ax1.set_ylabel('Porcentaje', color='b')
            ax1.tick_params('y', colors='b')
            ax1.axhline(porcentaje[-1], color='b', linestyle='--', label = "Mean of means in Obs data")
            # Invertir el eje Y

            ax2 = ax1.twinx()
            ax2.plot(horas, means_diference[:-1],'r-')
            #ax2.plot(horas, mean_sigma[:-1],'k-')
            ax2.set_ylabel('Diferencia', color='r')
            ax2.tick_params('y', colors='r')
            ax2.invert_yaxis()
            ax2.axhline(means_diference[-1], color='r', linestyle='--', label = "Mean of Comp data")

            # Graficar el total de horas

            plt.title('Obs vs '+ str(name_column_CompData))
            plt.grid()
            plt.xticks(horas)
            plt.legend()
            plt.show()
        
        def graficar_all(porcentaje, mean_sigma, means_diference):
            if minutes == False: 
                horas = range(24)
            if minutes == True:
                horas = range(len(porcentaje) - 4)

            

            y1 = porcentaje[0][:-1]
            print(len(y1))
            y1_extra1 = porcentaje[1][:-1]
            y1_extra2 = porcentaje[2][:-1]
            y1_extra3 = porcentaje[3][:-1]
            
            y2 = means_diference[0][:-1]
            y2_extra1 = means_diference[1][:-1]
            print(len(y2_extra1))
            print(y2_extra1)
            y2_extra2 = means_diference[2][:-1]
            y2_extra3 = means_diference[3][:-1]

            fig, ax1 = plt.subplots()
            # Configurar el primer plot en el lado izquierdo
            color_ax1 = 'b'  # Color para las curvas en ax1
            ax1.plot(horas, y1, color_ax1 + '-', label='10')
            ax1.plot(horas, y1_extra1, color_ax1 + '--', label='7')
            ax1.plot(horas, y1_extra2, color_ax1 + '-.', label='8')
            ax1.plot(horas, y1_extra3, color_ax1 + ':', label='15')

            ax1.set_xlabel('Eje X')
            ax1.set_ylabel('Porcentaje comp dentro de stdDEv', color=color_ax1)
            ax1.tick_params('y', colors=color_ax1)

            # Crear el segundo plot y compartir el eje X con el primer plot
            ax2 = ax1.twinx()

            color_ax2 = 'r'  # Color para las curvas en ax2
            ax2.plot(horas, y2, color_ax2 + '-', label='10')
            ax2.plot(horas, y2_extra1, color_ax2 + '--', label='7')
            ax2.plot(horas, y2_extra2, color_ax2 + '-.', label='8')
            ax2.plot(horas, y2_extra3, color_ax2 + ':', label='15')
            ax2.invert_yaxis()
            ax2.set_ylabel("Diferencia entre promedios", color=color_ax2)
            ax2.tick_params('y', colors=color_ax2)

            # Mostrar leyendas
            handles, labels = ax1.get_legend_handles_labels()
            ax1.legend(labels, loc='upper left')

            plt.title("Obs vs CI" )
            plt.grid()
            plt.xticks(horas)

            # Mostrar el gráfico
            plt.show()
        
        porcentajes = []
        means_sigma = []
        means_diference = []
        for name in ["simEhr_porcentual","simEhr5mAutos_porcentual","simEhr7mAutos_porcentual","simEhr15mAutos_porcentual"]:
            porcentaje_OneName = []
            mean_sigma_OneName = []
            means_diference_OneName = []
            if minutes == False:
                for i in range(25):
                    if i < 24:
                        i_str = str(i).zfill(2)
                    else:
                        i_str = False            
                    
                    result = self.getCIInMeanObsDataDistributionWithStdDev( name,
                                                                            type_get_obs_link,
                                                                            type_of_scale,
                                                                            i_str,
                                                                            minutes,
                                                                            graph,
                                                                            max_v,
                                                                            min_v,
                                                                            with_zeros)
                    porcentaje_OneName.append(result[0])
                    mean_sigma_OneName.append(result[1])
                    means_diference_OneName.append(result[4])
                
                porcentajes.append(porcentaje_OneName)
                means_sigma.append(mean_sigma_OneName)
                means_diference.append(means_diference_OneName)
            
            elif minutes  == True:
                for i in range(25):
                    if i < 24:
                        i_str = str(i).zfill(2)
                        for minutos in range(0, 46, 15):
                            minutos = str(minutos).zfill(2)                            
                            result = self.getCIInMeanObsDataDistributionWithStdDev( name,
                                                                                    type_get_obs_link,
                                                                                    type_of_scale,
                                                                                    i_str,
                                                                                    minutos,
                                                                                    graph,
                                                                                    max_v,
                                                                                    min_v,
                                                                                    with_zeros)
                            porcentaje_OneName.append(result[0])
                            mean_sigma_OneName.append(result[1])
                            means_diference_OneName.append(result[4])
                        porcentajes.append(porcentaje_OneName)
                        means_sigma.append(mean_sigma_OneName)
                        means_diference.append(means_diference_OneName)
                    else:
                        i_str = False
                        result = self.getCIInMeanObsDataDistributionWithStdDev( name,
                                                                                type_get_obs_link,
                                                                                type_of_scale,
                                                                                i_str,
                                                                                minutes,
                                                                                graph,
                                                                                max_v,
                                                                                min_v,
                                                                                with_zeros)
                        porcentaje_OneName.append(result[0])
                        mean_sigma_OneName.append(result[1])
                        means_diference_OneName.append(result[4])

                        porcentajes.append(porcentaje_OneName)
                        means_sigma.append(mean_sigma_OneName)
                        means_diference.append(means_diference_OneName)

        graficar_all(porcentajes, means_sigma, means_diference)

    def ehrenfestSimulationWithBounded_porcentual(self, dataframe):
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
    
def main():
    #nodos
    #PuntaArenasNodos = NetworkComparisonNodes( "temp/datos_red_prueba_nodos.dat", "datosNuevosNodosCoordenadas")
    #PuntaArenasNodos.getCIInMeanObsDataDistributionWithStdDev2("DiBC", type_of_scale="rescale", hour=False, with_zeros=False)
    #PuntaArenasNodos.getCaracteristicas(type_get_obs_link="Max" , graph=True, minutes=False)
    #PuntaArenasNodos.getDistributionForTraffucForHourInAllNodes("frecuencia_de_colores.csv")
    # "frecuencia_de_colores.csv"
    #Ejes
    PuntaArenas = NetworkComparisonEdges("datos+ehr+porc.csv", "data/DataImages/In_Streets_Coord/DataStreetsDetR1Step2.csv")
    #PuntaArenas.getCIInMeanObsDataDistributionWithStdDev("simEhr5mAutos_porcentual",type_of_scale="rescale", hour=7,minutes=15, with_zeros=True, type_get_obs_link="Mean")
    PuntaArenas.getDistributionForTrafficForEdge(10)
    
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

    def graficar(mean_and_stdDev, computational_data, name_column, prom_obs, prom_comp):
        indices = [x for x in mean_and_stdDev.keys()]
        promedios = [x[0] for x in mean_and_stdDev.values()]
        desviaciones = [x[1] for x in mean_and_stdDev.values()]

        plt.errorbar(range(1, len(indices) + 1), promedios, yerr=desviaciones, fmt='o', capsize=5, label='Promedio y Desviación Estándar')

        # Graficar puntos adicionales
        valores_adicionales = [computational_data[x] for x in indices]
        plt.scatter(range(1, len(indices) + 1), valores_adicionales, c='r', marker='*', label=str(name_column))
        
        # Graficar promedio
        plt.axhline(y=prom_obs, color='b', linestyle='--', label = "Mean of means in Obs data")
        plt.axhline(y=prom_comp, color='r', linestyle='--', label = "Mean Comp data")

        plt.xlabel("Number of Link")
        plt.ylabel('Centrality Index and Obs Value')
        plt.title('Mean Obs With Std Dev and Index of '+ str(name_column))

        # Mostrar etiquetas de índice originales en el eje X
        plt.xticks(range(1, len(indices) + 1), indices)
        plt.grid()
        plt.legend()
        plt.show()

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

    #Eligiendo tipo de dato observacional
    """
    if type_get_obs_link == "Max":
        df_obs_data = getMax(self.ObservationaldataFrame)
        df_obs_data.to_csv("MaxObsData.csv")
    elif type_get_obs_link == "Mean":
        df_obs_data = getMean(self.ObservationaldataFrame)    
        df_obs_data.to_csv("MeanObsData.csv")
    """
    
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

def getCaracteristicas(datos_observacionales,
                       computational_data,
                        type_of_scale = None,
                        minutes = None,
                        graph = None,
                        with_zeros = None):

    if type_of_scale is  None:
        type_of_scale = "rescale"
    if minutes is  None:
        minutes = False
    if graph  is None:
        graph = True
    if with_zeros is  None:
        with_zeros = True


    def graficar(porcentaje, mean_sigma, means_diference):
        horas = range(len(porcentaje) - 1)
        fig, ax1 = plt.subplots()
        ax1.plot(horas, porcentaje[:-1],'b-')
        ax1.set_ylabel('Porcentaje', color='b')
        ax1.tick_params('y', colors='b')
        ax1.axhline(porcentaje[-1], color='b', linestyle='--', label = "Mean of means in Obs data")
        # Invertir el eje Y

        ax2 = ax1.twinx()
        ax2.plot(horas, means_diference[:-1],'r-')
        #ax2.plot(horas, mean_sigma[:-1],'k-')
        ax2.set_ylabel('Diferencia', color='r')
        ax2.tick_params('y', colors='r')
        ax2.invert_yaxis()
        ax2.axhline(means_diference[-1], color='r', linestyle='--', label = "Mean of Comp data")

        # Graficar el total de horas

        plt.title('Obs vs ')
        plt.grid()
        plt.xticks(horas)
        plt.legend()
        plt.show()
    
    def graficar_all(porcentaje, mean_sigma, means_diference):
        if minutes == False: 
            horas = range(24)
        if minutes == True:
            horas = range(len(porcentaje) - 4)

        

        y1 = porcentaje[0][:-1]
        print(len(y1))
        y1_extra1 = porcentaje[1][:-1]
        y1_extra2 = porcentaje[2][:-1]
        y1_extra3 = porcentaje[3][:-1]
        
        y2 = means_diference[0][:-1]
        y2_extra1 = means_diference[1][:-1]
        print(len(y2_extra1))
        print(y2_extra1)
        y2_extra2 = means_diference[2][:-1]
        y2_extra3 = means_diference[3][:-1]

        fig, ax1 = plt.subplots()
        # Configurar el primer plot en el lado izquierdo
        color_ax1 = 'b'  # Color para las curvas en ax1
        ax1.plot(horas, y1, color_ax1 + '-', label='10')
        ax1.plot(horas, y1_extra1, color_ax1 + '--', label='7')
        ax1.plot(horas, y1_extra2, color_ax1 + '-.', label='8')
        ax1.plot(horas, y1_extra3, color_ax1 + ':', label='15')

        ax1.set_xlabel('Eje X')
        ax1.set_ylabel('Porcentaje comp dentro de stdDEv', color=color_ax1)
        ax1.tick_params('y', colors=color_ax1)

        # Crear el segundo plot y compartir el eje X con el primer plot
        ax2 = ax1.twinx()

        color_ax2 = 'r'  # Color para las curvas en ax2
        ax2.plot(horas, y2, color_ax2 + '-', label='10')
        ax2.plot(horas, y2_extra1, color_ax2 + '--', label='7')
        ax2.plot(horas, y2_extra2, color_ax2 + '-.', label='8')
        ax2.plot(horas, y2_extra3, color_ax2 + ':', label='15')
        ax2.invert_yaxis()
        ax2.set_ylabel("Diferencia entre promedios", color=color_ax2)
        ax2.tick_params('y', colors=color_ax2)

        # Mostrar leyendas
        handles, labels = ax1.get_legend_handles_labels()
        ax1.legend(labels, loc='upper left')

        plt.title("Obs vs CI" )
        plt.grid()
        plt.xticks(horas)

        # Mostrar el gráfico
        plt.show()
    
    porcentaje_OneName = []
    mean_sigma_OneName = []
    means_diference_OneName = []
    if minutes == False:
        for i in range(25):
            if i < 24:
                i_str = str(i).zfill(2)
            else:
                i_str = False            
            
            result = getCIInMeanObsDataDistributionWithStdDev( datos_observacionales,
                                                                    computational_data,
                                                                    type_of_scale,
                                                                    i_str,
                                                                    minutes,
                                                                    graph,
                                                                    with_zeros)
            porcentaje_OneName.append(result[0])
            mean_sigma_OneName.append(result[1])
            means_diference_OneName.append(result[4])
            
    elif minutes  == True:
        for i in range(25):
            if i < 24:
                i_str = str(i).zfill(2)
                for minutos in range(0, 46, 15):
                    minutos = str(minutos).zfill(2)                            
                    result = getCIInMeanObsDataDistributionWithStdDev( datos_observacionales,
                                                                    computational_data,
                                                                    type_of_scale,
                                                                    i_str,
                                                                    minutes,
                                                                    graph,
                                                                    with_zeros)
                    porcentaje_OneName.append(result[0])
                    mean_sigma_OneName.append(result[1])
                    means_diference_OneName.append(result[4])
            else:
                i_str = False
                result = getCIInMeanObsDataDistributionWithStdDev( datos_observacionales,
                                                                    computational_data,
                                                                    type_of_scale,
                                                                    i_str,
                                                                    minutes,
                                                                    graph,
                                                                    with_zeros)
                porcentaje_OneName.append(result[0])
                mean_sigma_OneName.append(result[1])
                means_diference_OneName.append(result[4])

    graficar(porcentaje_OneName, mean_sigma_OneName, means_diference_OneName)

if __name__ == "__main__":
    PuntaArenas = NetworkComparisonNodes("data/DataMakeNetwork/PuntaArenas","data/Images/screenshots" )