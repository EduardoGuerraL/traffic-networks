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


def calculate_slopes_for_fit_medians_and_Per95(datos_obs, datos_comp, n_boxes=20):
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


def run_median_slopes_vs_per95(datos_comp, datos_obs, label, topology_index='DiCC', threshold=0.33, output_path=None):
    """
    Genera scatter de Slope vs P95(traffic intensity) con fit line y R².

    Args:
        datos_comp: DataFrame con datos computacionales.
        datos_obs: DataFrame con datos observacionales.
        label: Nombre de la red.
        topology_index: Columna de índice topológico (e.g. 'DiCC', 'CC').
        threshold: Umbral alpha para filtrar puntos.
        output_path: Ruta para guardar PNG. Si es None, muestra en pantalla.
    """
    data_computational = datos_comp[topology_index]
    data_computational = [(i - min(data_computational)) / (max(data_computational) - min(data_computational)) for i in data_computational]
    n_boxes = N_BOXES_MAP.get(topology_index, 20)

    Slopes, Per95 = calculate_slopes_for_fit_medians_and_Per95(datos_obs=datos_obs, datos_comp=data_computational, n_boxes=n_boxes)

    plt.style.use(["science", "notebook", "grid"])
    plt.tick_params(axis='both', labelsize=18)

    datos_filtrados = [(x, y) for x, y in zip(Slopes, Per95) if y > threshold]
    if len(datos_filtrados) < 2:
        print(f"Warning: solo {len(datos_filtrados)} puntos tras filtrar con threshold={threshold}")
        return
    X_filtrado, Y_filtrado = zip(*datos_filtrados)
    X_filtrado = np.array(X_filtrado).reshape(-1, 1)
    Y_filtrado = np.array(Y_filtrado)

    modelo = LinearRegression().fit(X_filtrado, Y_filtrado)
    pendiente = modelo.coef_[0]
    interseccion = modelo.intercept_
    y_pred = modelo.predict(X_filtrado)
    r2 = r2_score(Y_filtrado, y_pred)

    plt.scatter(Slopes, Per95, edgecolors='black', facecolors='white')
    X_plot = np.linspace(min(X_filtrado), max(X_filtrado), 100)
    plt.plot(X_plot, modelo.predict(X_plot), color='k', label=f'Fit\n (y = {pendiente:.2f} x + {interseccion:.2f})', linestyle="--")
    plt.axhline(threshold, linestyle='--', color='gray')

    if output_path is None:
        # Modo notebook: ajustar límites a los datos reales para ver todos los puntos
        all_x = np.array(Slopes)
        all_y = np.array(Per95)
        plt.xlim(max(0, all_x.min() - 0.02), all_x.max() + 0.02)
        plt.ylim(all_y.min() - 0.02, all_y.max() + 0.02)
    else:
        plt.xlim(0, 0.32)
        plt.ylim(0.2, 0.7)

    residuals = Y_filtrado - y_pred
    std_dev = np.std(residuals)

    plt.text(0.2, 0.9, f'$R^2$= {r2:.3f}',
        horizontalalignment='center', verticalalignment='center',
        transform=plt.gca().transAxes, fontsize=16)

    plt.title(f'{label} - {topology_index}')
    plt.xlabel('Slope Linear Fit')
    plt.ylabel(r'$P_{95}$(Traffic Intensity)')

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


if __name__ == "__main__":
    from functions.RutasDeArchivos import Datos_computacionales, Datos_observacionales
    datos_comp_N505 = pd.read_csv(Datos_computacionales[0])
    datos_obs_N505 = pd.read_csv(Datos_observacionales[2])
    run_median_slopes_vs_per95(datos_comp_N505, datos_obs_N505, "N505", topology_index='DiCC', threshold=0.329)
