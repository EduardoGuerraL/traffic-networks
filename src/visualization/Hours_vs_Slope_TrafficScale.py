"""
Importante: Existen estos valores computacionales:
    nombres = ["BC","CC","DC","DiBC","DiCC","DiDC","MaxOcupation","mean_state_RW","mean_state_RW_lim","mean_state_RWM","mean_state_RWM_lim"]
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import seaborn as sns
from functions.basics import reescalar_lista_de_listas, obtener_nombres_con_H_M_sinFDS, crearNintervalosOrdenados


def guardar_lista_en_archivo(lista, nombre_archivo):
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            for elemento in lista:
                archivo.write(f"{elemento}\n")
    except Exception as e:
        print(f"Error al guardar la lista en el archivo: {e}")


def calculate_median_positions(X: list, Y: list, box_count: int):
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, box_count)
    y_median_box = []
    x_median_box = []
    for i in range(box_count):
        if intervalos_X[i]:
            ancho = (intervalos_X[i][-1] - intervalos_X[i][0])
            positions = [intervalos_X[i][-1] - (ancho / 2)]
            x_median_box.append(positions[0])
    y_median_box = [np.median(subconjunto) for subconjunto in intervalos_Y]
    return y_median_box, x_median_box


def hour_to_minutes(hour):
    h, m = map(int, hour.split(':'))
    return h * 60 + m


def generate_boundaries(N):
    step = 1 / N
    boundaries = [[i * step, (i + 1) * step] for i in range(N)]
    return boundaries


def generate_colors(N):
    step = 1 / (N-1)
    boundaries = [(i * step, i * step, i * step) for i in range(N)]
    return boundaries


def run_hours_vs_slope(datos_comp, datos_obs, label, output_path=None):
    """
    Genera el gráfico de pendientes de correlación vs tiempo para una red.

    Args:
        datos_comp: DataFrame con datos computacionales de la red.
        datos_obs: DataFrame con datos observacionales de la red.
        label: Nombre de la red (e.g. 'N505', 'N1207').
        output_path: Ruta para guardar el PNG. Si es None, muestra en pantalla.
    """
    colors = {'DiBC': 'green', 'BC': 'green', 'DiCC': 'blue', 'CC': 'blue', 'DiDC': 'red', 'DC': 'red'}
    for key in list(colors.keys()):
        if not key.startswith('Di'):
            base_color = colors[key]
            lighter_color = sns.light_palette(base_color)[2]
            colors[key] = lighter_color

    fig, axs = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'width_ratios': [20, 1]})
    axs[0].tick_params(axis='both', which='both', labelsize=12, width=2)
    axs[1].tick_params(axis='both', which='both', labelsize=14, width=2)

    P95_per_instant_of_time = []
    instants_of_observation = []
    mean_per_instant_of_time = []

    hora_inicial, hora_final = 0, 24
    for hora_in in range(hora_inicial, hora_final):
        for minuto_in in range(0, 60, 15):
            columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
            data_obs_iter = datos_obs[columnas_elejidas].values.tolist()
            data_obs_iter = reescalar_lista_de_listas(data_obs_iter, 255)

            list_of_mean_of_each_node = [np.mean(data) for data in data_obs_iter]
            percentil_95 = np.percentile(list_of_mean_of_each_node, 95)
            P95_per_instant_of_time.append(percentil_95)
            instants_of_observation.append(f"{hora_in}:{minuto_in}".format(hora_in, minuto_in))
            mean_per_instant_of_time.append(list_of_mean_of_each_node)

    names = ["DiBC", "BC", "DiCC", "CC", "DiDC", "DC"]
    set_of_all_fitSlopes = []
    for type_of_comp_data in names:
        dats_for_one_type_of_comput = datos_comp[type_of_comp_data]
        dats_for_one_type_of_comput = [(i - min(dats_for_one_type_of_comput)) / (max(dats_for_one_type_of_comput) - min(dats_for_one_type_of_comput)) for i in dats_for_one_type_of_comput]

        fitSlope_per_instante_of_time = []
        for instant_mean in mean_per_instant_of_time:
            if type_of_comp_data in ["DiDC", "DC"]:
                n_boxes = 3
            elif type_of_comp_data in ["DiBC", "BC"]:
                n_boxes = 15
            elif type_of_comp_data in ["DiCC", "CC"]:
                n_boxes = 20

            y_medians, x_medians = calculate_median_positions(dats_for_one_type_of_comput, instant_mean, n_boxes)
            medians_params = scipy.stats.linregress(x_medians, y_medians)
            fitSlope_per_instante_of_time.append(medians_params[0])

        set_of_all_fitSlopes.append(fitSlope_per_instante_of_time)

    intervals_minutes = [hour_to_minutes(interval) for interval in instants_of_observation]
    intervals_minutes_end = intervals_minutes[1:] + [hour_to_minutes('24:0')]

    for fitSlope_per_instant, name in zip(set_of_all_fitSlopes, names):
        axs[0].plot(intervals_minutes, fitSlope_per_instant, label=f"{label} - {name}", color=colors[name])

    for i, f, perc in zip(intervals_minutes, intervals_minutes_end, P95_per_instant_of_time):
        prec = (perc - min(P95_per_instant_of_time)) / (max(P95_per_instant_of_time) - min(P95_per_instant_of_time))
        axs[0].axvspan(i - 7.5, f - 7.5, facecolor=(prec, prec, prec), alpha=0.9)
    axs[0].axvspan(intervals_minutes_end[-1] - 7.5, intervals_minutes_end[-1], facecolor=(0, 0, 0), alpha=0.9)

    boundaries = generate_boundaries(50)
    discrete_colors = generate_colors(50)
    for i, (interval, color) in enumerate(zip(boundaries, discrete_colors)):
        axs[1].barh(interval[0] + (interval[1] - interval[0]) / 2, 1, left=0, color=color, alpha=0.9, height=interval[1] - interval[0])

    axs[1].set_ylim(0, 1)
    axs[1].set_xlim(0, 1)
    axs[1].set_yticks([min(P95_per_instant_of_time), max(P95_per_instant_of_time)])
    axs[1].tick_params(axis='y', labelright=True, labelleft=False)

    axs[0].set_xlabel('Tiempo (minutos)')
    axs[0].set_ylabel('pendiente')
    axs[0].set_title(f'Pendientes de correlación - {label}')
    axs[0].set_xticks(np.arange(0, 24 * 60 + 1, 60))
    axs[0].set_xticklabels([f"{hour // 60}" for hour in np.arange(0, 24 * 60 + 1, 60)])
    axs[0].set_xlim(0, 24 * 60)
    all_slopes = [s for slopes in set_of_all_fitSlopes for s in slopes]
    if output_path is None and all_slopes:
        ymin, ymax = min(all_slopes), max(all_slopes)
        margin = (ymax - ymin) * 0.05 if ymax > ymin else 0.05
        axs[0].set_ylim(ymin - margin, ymax + margin)
    axs[0].grid(True, which='both', linestyle='--', linewidth=0.5)
    axs[0].legend(loc='upper center', bbox_to_anchor=(0.6, -0.2), fancybox=False, shadow=False, ncol=6)
    plt.subplots_adjust(left=0.07, right=0.93, bottom=0.22, top=0.92, wspace=0.05)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales
    datos_comp_N505 = pd.read_csv(Datos_computacionales[0])
    datos_obs_N505 = pd.read_csv(Datos_observacionales[4])
    run_hours_vs_slope(datos_comp_N505, datos_obs_N505, "N505")
