"""
Genera scatter+boxplot de intensidad de tráfico vs valor topológico por instante de tiempo.
Guarda un PNG por instante de tiempo.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import seaborn as sns
from functions import CrearCarpeta, obtener_nombres_con_H_M_sinFDS, reescalar_lista_de_listas, crearNintervalosOrdenados
import scienceplots


def scatter_and_boxplot(X, Y, N):
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, N)
    plt.style.use(["science", "notebook", "grid"])
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 11), gridspec_kw={'width_ratios': [10, 1]}, sharey=True)
    ax1.grid(True)
    Medianas = []
    Posiciones_X = []
    ancho = 1 / N
    for i in range(N):
        if intervalos_X[i]:
            pos_x_to_plot = [ancho * (i + 1 / 2)]
            pos_x_to_save = [np.mean(intervalos_X[i])]
            ax1.boxplot(intervalos_Y[i], positions=pos_x_to_plot, widths=ancho, showfliers=False, patch_artist=True, boxprops={'facecolor': 'gray', 'alpha': 0.4}, medianprops={'color': 'black', 'linewidth': 3})
            Posiciones_X.append(pos_x_to_plot[0])

    Medianas = [np.median(subconjunto) for subconjunto in intervalos_Y]
    ax1.scatter(X, Y, label="Scatter Plot", color='gray', alpha=0.1, s=20, edgecolor='black', marker='o')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_xticks([])

    sns.kdeplot(y=Y, ax=ax2, color='blue', common_norm=True)
    plt.hist(Y, orientation="horizontal", density=True, bins=40, color="blue", alpha=0.3)
    ax2.set_xlabel("")
    ax2.set_ylim(0, 1)
    ax2.set_xlim(0, 12)
    ax2.set_xticks([])
    return Medianas, Posiciones_X, ax1, ax2


def scatter4MeanObsValues(compu_data, list_of_list_of_Obs, carpetaSup, title, xlabel="x"):
    promedios = [np.mean(data) for data in list_of_list_of_Obs]
    medians_box, pos_box, ax1, ax2 = scatter_and_boxplot(list(compu_data), list(promedios), 3)

    medians_params = scipy.stats.linregress(pos_box, medians_box)
    x = np.linspace(-10, 10, 100)
    y = medians_params[0] * x + medians_params[1]
    ax1.plot(x, y, '-r', label='y = {}x + {}'.format(medians_params[0], medians_params[1]))

    plt.tight_layout()
    plt.subplots_adjust(wspace=0)
    plt.savefig(os.path.join(carpetaSup, f"Boxscatter_{xlabel}_{title}.png"), dpi=150, bbox_inches='tight')
    plt.close()
    return medians_params


def run_traffic_vs_network(datos_comp, datos_obs, label, topology_name='DC', output_dir=None):
    """
    Genera scatter+boxplot para cada instante de tiempo y guarda PNGs.

    Args:
        datos_comp: DataFrame con datos computacionales.
        datos_obs: DataFrame con datos observacionales.
        label: Nombre de la red.
        topology_name: Columna de índice topológico (e.g. 'DC', 'CC').
        output_dir: Directorio donde guardar los PNGs.
    """
    data_computational = datos_comp[topology_name]
    data_computational = [(i - min(data_computational)) / (max(data_computational) - min(data_computational)) for i in data_computational]

    if output_dir is None:
        output_dir = f"results/{label}_{topology_name}"
    CrearCarpeta(output_dir)

    hora_inicial, hora_final = 0, 24
    for hora_in in range(hora_inicial, hora_final):
        for minuto_in in range(0, 60, 15):
            columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
            data_observacional = datos_obs[columnas_elejidas].values.tolist()
            data_observacional = reescalar_lista_de_listas(data_observacional, 255)

            scatter4MeanObsValues(data_computational, data_observacional, carpetaSup=output_dir, xlabel=topology_name, title=f"{hora_in}_{minuto_in}")


if __name__ == "__main__":
    from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales
    datos_comp_N1207 = pd.read_csv(Datos_computacionales[1])
    datos_obs_N1207 = pd.read_csv(Datos_observacionales[0])
    run_traffic_vs_network(datos_comp_N1207, datos_obs_N1207, "N1207")
