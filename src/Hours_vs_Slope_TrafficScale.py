"""
Importante: Existen estos valores computacionales:
    nombres = ["BC","CC","DC","DiBC","DiCC","DiDC","MaxOcupation","mean_state_RW","mean_state_RW_lim","mean_state_RWM","mean_state_RWM_lim"]
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scienceplots
import seaborn as sns
from functions.basics import reescalar_lista_de_listas, obtener_nombres_con_H_M_sinFDS, crearNintervalosOrdenados
from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales


# Funcion para dividir eje x en cajas
def calculate_median_positions(X: list, Y: list, box_count: int):
    # Dividir X e Y en box_count intervalos
    
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, box_count)
    
    # Gráfico de diagrama de caja en el primer subplot
    y_median_box = []
    x_median_box = []
    for i in range(box_count):
        if intervalos_X[i]:
            ancho = (intervalos_X[i][-1] - intervalos_X[i][0])
            positions = [intervalos_X[i][-1] - (ancho / 2)]
                    
            # Guardando datos[punto medio de x boxes, mean de Y, median de Y]
            x_median_box.append(positions[0])
    
    y_median_box = [np.median(subconjunto) for subconjunto in intervalos_Y]
    return y_median_box, x_median_box

# Función para convertir las horas en minutos
def hour_to_minutes(hour):
    h, m = map(int, hour.split(':'))
    return h * 60 + m

# Función para crear una lista de listas de 0 a 1 de la forma [[a, a+1],[a+1,a+2],...,[a+(N-1), a+N]] 
def generate_boundaries(N):
    """
    Generates a list of boundaries with N elements between 0 and 1.
    
    Parameters:
        N (int): Number of elements.
        
    Returns:
        list: List of boundary pairs.
    """
    step = 1 / N
    boundaries = [[i * step, (i + 1) * step] for i in range(N)]
    return boundaries

# Función que da para cada intervalo de generate_boundaries un pixel (x,x,x).
def generate_colors(N):
    """
    Generates a list of boundaries with N elements between 0 and 1.
    
    Parameters:
        N (int): Number of elements.
        
    Returns:
        list: List of boundary pairs.
    """
    step = 1 / (N-1)
    boundaries = [(i * step, i * step, i * step) for i in range(N)]
    return boundaries


# Crear la figura y los subgráficos
fig, axs = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [20, 1]})  # 1 fila, 2 columnas
axs[0].tick_params(axis='both', which='both', labelsize=12, width=2)  # Ajustar tamaño y grosor de las marcas en los ejes
axs[1].tick_params(axis='both', which='both', labelsize=14, width=2)  # Ajustar tamaño y grosor de las marcas en los ejes

# Diccionario de colores para cada tipo de convinacion de topo
colors = {'DiBC': 'green', 'BC': 'green', 'DiCC': 'blue', 'CC': 'blue', 'DiDC': 'red', 'DC': 'red'}
for key in list(colors.keys()):
    if not key.startswith('Di'):
        base_color = colors[key]
        lighter_color = sns.light_palette(base_color)[2]  # Tomar el tercer color más claro de la paleta
        colors[key] = lighter_color

#Conjunto de archivos
N505 = [Datos_computacionales[0], Datos_observacionales[2]]
N1207 = [Datos_computacionales[1], Datos_observacionales[0]]
datos_comp_N505 = pd.read_csv(N505[0])
datos_obs_N505 = pd.read_csv(N505[1])
datos_comp_N1207 = pd.read_csv(N1207[0])
datos_obs_N1207 = pd.read_csv(N1207[1])
data_observacional = [datos_obs_N505,datos_obs_N1207]
data_computacional  = [datos_comp_N505, datos_comp_N1207]

P95_per_instant_of_time_both = []
for datos_comp, datos_obs, label in zip(data_computacional, data_observacional, ["N505", "N1207"]):
    ## Tomamos todos los valores observacionales, los dividimos en horas y obtenemos el promedio de cada calle
    # en un instante de tiempo, ademas obtenermos el P95 de el total de datos en el instante de tiempo
    P95_per_instant_of_time = []
    instants_of_observation = []
    mean_per_instant_of_time = []

    hora_inicial, hora_final = 0, 24
    for hora_in in range(hora_inicial, hora_final):
        for minuto_in in range(0, 60, 15):

            columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
            data_observacional = datos_obs[columnas_elejidas].values.tolist()
            data_observacional = reescalar_lista_de_listas(data_observacional, 255) # Reescalando los data_observacional de 0 a 1

            # Obtener el promedio de cada nodo sobre los dias en el instante de tiempo
            list_of_mean_of_each_node = [np.mean(data) for data in data_observacional]
            percentil_95 = np.percentile(list_of_mean_of_each_node, 95)

            #Guardanto datos
            P95_per_instant_of_time.append(percentil_95)
            instants_of_observation.append(f"{hora_in}:{minuto_in}".format(hora_in, minuto_in))
            mean_per_instant_of_time.append(list_of_mean_of_each_node)


    ## Ahora necesitamos obtener la pendiente del fiteo de cada instante de tiempo al hacer scatter de Obs_vs_Comp.

    set_of_all_fitSlopes = []
    names = ["DiBC","BC","DiCC", "CC", "DiDC", "DC"]
    for type_of_comp_data in names:
        dats_for_one_type_of_comput = datos_comp[type_of_comp_data]
        dats_for_one_type_of_comput = [(i-min(dats_for_one_type_of_comput))/(max(dats_for_one_type_of_comput)-min(dats_for_one_type_of_comput)) for i in dats_for_one_type_of_comput]
                
        fitSlope_per_instante_of_time = []
        for instant_mean in mean_per_instant_of_time:
            if type_of_comp_data in ["DiDC", "DC"]:
                n_boxes = 3
            if type_of_comp_data in ["DiBC", "BC"]:
                n_boxes = 15
            if type_of_comp_data in ["DiCC", "CC"]:
                n_boxes = 20

            y_medians, x_medians = calculate_median_positions(dats_for_one_type_of_comput,
                                                            instant_mean,
                                                            n_boxes)
            
            ## REGRESION LINEAL
            #(slope, intercept, r_value, p_value, std_err)
            medians_params = scipy.stats.linregress(x_medians, y_medians)
            fitSlope_per_instante_of_time.append(medians_params[0])

        set_of_all_fitSlopes.append(fitSlope_per_instante_of_time)

     # Crear una lista de inicio y fin de intervalos en minutos
    intervals_minutes = [hour_to_minutes(interval) for interval in instants_of_observation]
    intervals_minutes_end = intervals_minutes[1:] + [hour_to_minutes('24:0')]

    linestyle = '-' if label == 'N505' else '--'
    # agregar grafico de typo de dat computacional
    for fitSlope_per_instant, name in zip(set_of_all_fitSlopes, names):
        axs[0].plot(intervals_minutes, fitSlope_per_instant, label = f"{label} - {name}", color=colors[name], linestyle=linestyle)

    P95_per_instant_of_time_both.append(P95_per_instant_of_time)

# Configuración de la gráfica

print(P95_per_instant_of_time_both)
P95_per_instant_of_time = P95_per_instant_of_time_both[0]
# Iterar sobre los intervalos y dibujar las áreas
for i, f, perc in zip(intervals_minutes, intervals_minutes_end, P95_per_instant_of_time):
    prec = (perc - min(P95_per_instant_of_time))/(max(P95_per_instant_of_time)-min(P95_per_instant_of_time))


    gris  = prec #continuos

    #Opcion1
    '''
    if prec >= 0.95:
        gris = 1
    elif (prec >= 0.75) and (prec < 0.95) :
        gris = 0.666
    elif (prec >= 0.50) and (prec < 0.75) :
        gris = 0.333
    else:
        gris = 0     
    '''
    '''
    #Opcion2
    if prec >= 0.95:
        gris = 1
    elif (prec >= 0.85) and (prec < 0.95) :
        gris = 0.8
    elif (prec >= 0.70) and (prec < 0.85) :
        gris = 0.6
    elif (prec >= 0.50) and (prec < 0.70) :
        gris = 0.4
    elif (prec >= 0.25) and (prec < 0.50) :
        gris = 0.2
    else:
        gris = 0     
    '''


    axs[0].axvspan(i-7.5, f-7.5, facecolor=(gris,gris,gris), alpha = 0.9)
axs[0].axvspan(intervals_minutes_end[-1]-7.5, intervals_minutes_end[-1], facecolor=(0,0,0), alpha = 0.9)

'''#Opcion2
boundaries = [[0.0, 0.25],[0.25,0.50],[0.5, 0.70],[0.70,0.85],[0.85, 0.95],[0.95, 1]]
discrete_colors = [(0,0,0), (0.2,0.2,0.2), (0.4,0.4,0.4), (0.6,0.6,0.6), (0.8,0.8,0.8), (1,1,1)]

'''
'''
#Opcion1
boundaries = [[0.0, 0.50],[0.5, 0.75],[0.75, 0.95],[0.95, 1]]
discrete_colors = [(0,0,0), (0.33,0.33,0.33), (0.66,0.66,0.66), (1,1,1)]
'''


# continuos
boundaries = generate_boundaries(50)
discrete_colors = generate_colors(50)


for i, (interval, color) in enumerate(zip(boundaries, discrete_colors)):
    axs[1].barh(interval[0]+(interval[1]-interval[0])/2, 1, left=0, color=color, alpha=0.9, height=interval[1]-interval[0])  # Barras horizontales para resaltar intervalos

axs[1].set_ylim(0, 1)  # Invertir el eje y para que el intervalo más bajo esté arriba
axs[1].set_xlim(0, 1)  # Invertir el eje y para que el intervalo más bajo esté arriba
axs[1].set_yticks([min(P95_per_instant_of_time_both[0]), max(P95_per_instant_of_time_both[0])])
#axs[1].set_yticks(np.arange(0, 1, 0.05))
#axs[1].set_yticklabels([])  # Eliminar las etiquetas de los ticks del eje y
#axs[1].set_yticks([0, 0.25 ,0.5,  0.70, 0.85, 0.95, 1])
#axs[1].set_yticks([0 ,0.5, 0.75, 0.95, 1])
axs[1].tick_params(axis='y', labelright=True, labelleft=False)  # Mover las marcas del eje y a la derecha y ocultar las etiquetas del eje y

# Configuración del gráfico principal (usando métodos de ax_main)
axs[0].set_xlabel('Tiempo (minutos)')  # Usa set_xlabel en lugar de xlabel
axs[0].set_ylabel('pendiente')  # Usa set_ylabel en lugar de ylabel
axs[0].set_title('Indices de la red vs la pendiente de correlacion en cada instante de tiempo')  # Usa set_title en lugar de title
axs[0].set_xticks(np.arange(0, 24*60+1, 60))
#axs[0].set_xticklabels([f"{hour // 60}:{hour % 60}" for hour in np.arange(0, 24*60+1, 60)], rotation=90)  # Usa set_xticklabels en lugar de xticks
axs[0].set_xticklabels([f"{hour // 60}" for hour in np.arange(0, 24*60+1, 60)])  # Usa set_xticklabels en lugar de xticks

axs[0].set_xlim(0, 24*60)  # Usa set_xlim en lugar de xlim
axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)  # No se necesita cambiar, la cuadrícula se configura correctamente

# Mostrar la gráfica
axs[0].legend(loc='upper center', bbox_to_anchor=(0.6, -0.2), 
          fancybox=False, shadow=False, ncol=6)  # No se necesita cambiar, la leyenda se configura correctamente
plt.subplots_adjust(left=0.05, right=0.95, wspace=0.3)  # Ajustar los márgenes y el espacio entre los subgráficos
plt.tight_layout()
plt.show()
