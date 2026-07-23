import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scienceplots
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy import stats
from functions.basics import reescalar_lista_de_listas, crearNintervalosOrdenados, obtener_nombres_con_H_M_sinFDS
import math

N_BOXES_MAP = {"DiBC": 15, "BC": 15, "DiCC": 20, "CC": 20, "DiDC": 3, "DC": 3}


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


def calculate_slopes_for_fit_medians_and_Per95(datos_obs, datos_comp, n_boxes):
    Slopes = []
    Per95 = []
    hora_inicial, hora_final = 0, 24
    for hora_in in range(hora_inicial, hora_final):
        for minuto_in in range(0, 60, 15):
            columnas_elejidas = obtener_nombres_con_H_M_sinFDS(datos_obs.columns, hora_exacta=(hora_in, minuto_in))
            data_observacional = datos_obs[columnas_elejidas].values.tolist()
            data_observacional = reescalar_lista_de_listas(data_observacional, 255)
            promedios = [np.mean(data) for data in data_observacional]
            percentil_95 = np.percentile(promedios, 95)
            y_medians, x_medians = calculate_median_positions(datos_comp, promedios, n_boxes)
            medians_params = scipy.stats.linregress(x_medians, y_medians)
            Slopes.append(medians_params[0])
            Per95.append(percentil_95)
    return Slopes, Per95


def find_values_matrix(data):
    X = list(data[0])
    Y = list(data[1])
    Z = list(data[2])
    X_max = max(X)
    indice_X_max = X.index(X_max)
    Y_X_max = Y[indice_X_max]
    Z_X_max = Z[indice_X_max]
    Y_max = max(Y)
    indice_Y_max = Y.index(Y_max)
    X_Y_max = X[indice_Y_max]
    Z_Y_max = Z[indice_Y_max]
    return X_Y_max, Y_max, Z_Y_max


def run_median_slopes_vs_r2(datos_comp, datos_obs, label, topology_names=None, output_path=None):
    """
    Barre umbrales y encuentra el threshold que maximiza R² para cada topology index.

    Args:
        datos_comp: DataFrame con datos computacionales.
        datos_obs: DataFrame con datos observacionales.
        label: Nombre de la red.
        topology_names: Lista de columnas topológicas (default: ['CC', 'DiCC']).
        output_path: Ruta para guardar PNG. Si es None, imprime en consola.
    """
    if topology_names is None:
        topology_names = ['CC', 'DiCC']

    print(f"\n=== {label} ===")
    for name_column in topology_names:
        data_computational = datos_comp[name_column]
        data_computational = [(i - min(data_computational)) / (max(data_computational) - min(data_computational)) for i in data_computational]
        n_boxes = N_BOXES_MAP.get(name_column, 20)

        Slopes, Per95 = calculate_slopes_for_fit_medians_and_Per95(datos_obs=datos_obs, datos_comp=data_computational, n_boxes=n_boxes)

        umbrales = np.linspace(min(Per95), max(Per95) - 0.2 * max(Per95), 200)
        Todos_los_datos = []
        r2_list = []
        slopes_list = []
        Trh = []
        for threshold in umbrales:
            threshold = math.trunc(threshold * 1000) / 1000
            datos_filtrados = [(x, y) for x, y in zip(Slopes, Per95) if y >= threshold]
            X_filtrado, Y_filtrado = zip(*datos_filtrados)
            medians_params = scipy.stats.linregress(X_filtrado, Y_filtrado)
            r2_list.append(math.trunc((medians_params[2] ** 2) * 1000) / 1000)
            slopes_list.append(math.trunc((medians_params[0]) * 1000) / 1000)
            Trh.append(threshold)

        Todos_los_datos.append(slopes_list)
        Todos_los_datos.append(r2_list)
        Todos_los_datos.append(Trh)
        print(f"  {name_column}: {find_values_matrix(Todos_los_datos)}")

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f'Resultados guardados en consola\n{label}', ha='center', va='center', fontsize=14)
        ax.set_axis_off()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()


if __name__ == "__main__":
    from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales
    datos_comp_N505 = pd.read_csv(Datos_computacionales[0])
    datos_obs_N505 = pd.read_csv(Datos_observacionales[2])
    run_median_slopes_vs_r2(datos_comp_N505, datos_obs_N505, "N505")
