import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scienceplots
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from functions.basics import reescalar_lista_de_listas, obtener_nombres_con_H_M_sinFDS, crearNintervalosOrdenados

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


def calculate_slopes_for_fit_medians_and_Per95(datos_obs, datos_comp, box_count):
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
            y_medians, x_medians = calculate_median_positions(datos_comp, promedios, box_count)
            medians_params = scipy.stats.linregress(x_medians, y_medians)
            Slopes.append(medians_params[0])
            Per95.append(percentil_95)
    return Slopes, Per95


def run_three_slopes_vs_per95(datos_comp, datos_obs, label, topology_indices=None, thresholds=None, output_path=None):
    """
    Grafica Slope vs P95 para 3 índices topológicos superpuestos.

    Args:
        datos_comp: DataFrame con datos computacionales.
        datos_obs: DataFrame con datos observacionales.
        label: Nombre de la red.
        topology_indices: Lista de 3 nombres de columnas topológicas.
        thresholds: Lista de 3 thresholds alpha correspondientes.
        output_path: Ruta para guardar PNG. Si es None, muestra en pantalla.
    """
    if topology_indices is None:
        topology_indices = ["BC", "CC", "DC"]
    if thresholds is None:
        thresholds = [0.38, 0.328, 0.305]

    markers = ['o', 's', '^']
    box_counts = [N_BOXES_MAP[idx] for idx in topology_indices]
    colores = ['green', 'blue', 'red']

    plt.rcParams.update({"text.usetex": False})
    plt.style.use(["science", "notebook", "grid"])
    plt.tick_params(axis='both', labelsize=18)
    if output_path is None:
        # Modo notebook: límites dinámicos para ver todos los datos
        _all_x, _all_y = [], []
    else:
        plt.xlim(-0.1, 0.32)
        plt.ylim(0.2, 0.7)

    for indice, index_name in enumerate(topology_indices):
        data_computational = datos_comp[index_name]
        data_computational = [(i - min(data_computational)) / (max(data_computational) - min(data_computational)) for i in data_computational]
        Slopes, Per95 = calculate_slopes_for_fit_medians_and_Per95(datos_obs=datos_obs, datos_comp=data_computational, box_count=box_counts[indice])

        datos_filtrados = [(x, y) for x, y in zip(Slopes, Per95) if y > thresholds[indice]]
        if len(datos_filtrados) < 2:
            continue
        if output_path is None:
            _all_x.extend(Slopes)
            _all_y.extend(Per95)
        X_filtrado, Y_filtrado = zip(*datos_filtrados)
        X_filtrado = np.array(X_filtrado).reshape(-1, 1)
        Y_filtrado = np.array(Y_filtrado)

        modelo = LinearRegression().fit(X_filtrado, Y_filtrado)
        pendiente = modelo.coef_[0]

        plt.scatter(Slopes, Per95, edgecolors=colores[indice], facecolors='white', marker=markers[indice], label=index_name)
        X_plot = np.linspace(min(X_filtrado), max(X_filtrado), 100)
        plt.plot(X_plot, modelo.predict(X_plot), color='k', linestyle="--", label='_nolegend_')
        plt.axhline(thresholds[indice], linestyle='--', color=colores[indice], label='_nolegend_')

    plt.xlabel('Slope Linear Fit')
    plt.ylabel(r'$P_{95}$(Traffic Intensity)')
    plt.title(f'{label} - BC/CC/DC')

    if output_path is None and _all_x:
        plt.xlim(min(_all_x) - 0.02, max(_all_x) + 0.02)
        plt.ylim(min(_all_y) - 0.02, max(_all_y) + 0.02)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales
    datos_comp_N1207 = pd.read_csv(Datos_computacionales[1])
    datos_obs_N1207 = pd.read_csv(Datos_observacionales[0])
    run_three_slopes_vs_per95(datos_comp_N1207, datos_obs_N1207, "N1207")
