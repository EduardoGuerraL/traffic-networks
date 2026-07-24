"""
Paso 4: Cálculo de centralidad de redes.
Genera BC, CC, DC para dirigidas y no dirigidas × 2 redes = 12 combinaciones.

Utiliza redes serializadas via NetworkGraphLoader (no reconstruye la red).
"""

from __future__ import annotations
from pathlib import Path

import networkx as nx
import pandas as pd
import numpy as np

from src.utils.paths import (
    get_config,
    centralidad_path,
    iter_redes,
)
from src.network.load_network import NetworkGraphLoader


def compute_centrality(red: str) -> pd.DataFrame:
    """
    Calcula todas las centralidades para una red cargando la red serializada.

    Returns DataFrame con columnas: BC, CC, DC, DiBC, DiCC, DiDC.
    """
    cfg = get_config()

    # Directorio serializado
    serialized_dir = Path(__file__).parent.parent.parent / "data" / "network" / "serialized" / red
    loader = NetworkGraphLoader.load(str(serialized_dir))

    DG_streets = loader.DG_streets
    UG_streets = loader.UG_streets
    DG_inter = loader.DG_inter
    UG_inter = loader.UG_inter

    results = {}

    # Betweenness
    results['BC'] = nx.betweenness_centrality(UG_streets)
    results['DiBC'] = nx.betweenness_centrality(DG_streets)

    # Closeness
    results['CC'] = nx.closeness_centrality(UG_streets)
    results['DiCC'] = nx.closeness_centrality(DG_streets)

    # Degree
    results['DC'] = nx.degree_centrality(UG_streets)
    results['DiDC'] = nx.degree_centrality(DG_streets)

    # Intersection centralities (optional)
    results['BC_inter'] = nx.betweenness_centrality(UG_inter)
    results['CC_inter'] = nx.closeness_centrality(UG_inter)
    results['DC_inter'] = nx.degree_centrality(DG_inter)

    # Random walk analytic (using the same logic as old NetworkData)
    results['mean_state_RW'] = _randomwalk_analytic_edges(DG_streets)
    results['mean_state_RW_lim'] = _randomwalk_analytic_nodes(UG_inter)

    # Max occupation (Ehrenfest scaling)
    results['MaxOcupation'] = _get_max_particles_per_urns(
        loader.pos_intersections, loader.inter_conections
    )

    # Build DataFrame
    n_nodes = len(DG_streets.nodes())
    df = pd.DataFrame(index=range(n_nodes))
    for col, vals in results.items():
        df[col] = [vals.get(i, 0) for i in range(n_nodes)]

    return df


def _randomwalk_analytic_edges(DG_streets: nx.DiGraph) -> dict:
    """Random walk analítico sobre grafo dirigido de calles (replica el código viejo)."""
    Adjacency_matrix = np.array(
        nx.adjacency_matrix(DG_streets, nodelist=sorted(DG_streets.nodes())).todense()
    )
    Matrix_B = (Adjacency_matrix.T / np.sum(Adjacency_matrix.transpose(), axis=0)) - np.identity(
        len(Adjacency_matrix)
    )
    autovalores, autovectores = np.linalg.eig(Matrix_B)
    indice = next((i for i, valor in enumerate(autovalores) if abs(valor) < 1e-15), 0)
    Probabilidad = [i / sum(autovectores[:, indice]) for i in autovectores[:, indice]]
    Probabilidad = {i: np.real(valor) for i, valor in enumerate(Probabilidad)}
    return Probabilidad


def _randomwalk_analytic_nodes(UG_inter: nx.Graph) -> dict:
    """Random walk analítico sobre grafo no dirigido de intersecciones (replica el código viejo)."""
    Adjacency_matrix = np.array(
        nx.adjacency_matrix(UG_inter, nodelist=sorted(UG_inter.nodes())).todense()
    )
    Matrix_B = (Adjacency_matrix.T / np.sum(Adjacency_matrix.transpose(), axis=0)) - np.identity(
        len(Adjacency_matrix)
    )
    autovalores, autovectores = np.linalg.eig(Matrix_B)
    indice = next((i for i, valor in enumerate(autovalores) if abs(valor) < 1e-15), 0)
    Probabilidad = [i / sum(autovectores[:, indice]) for i in autovectores[:, indice]]
    Probabilidad = {i: np.real(valor) for i, valor in enumerate(Probabilidad)}
    return Probabilidad


def _get_max_particles_per_urns(
    pos_intersections: dict, inter_conections: list, factor_escala: float = 1.876
) -> dict:
    """Calcula capacidad máxima de autos por calle (replica el código viejo)."""
    def calcular_distancia(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    import math
    lenghts = {}
    for index, conection in enumerate(inter_conections):
        lenghts[index] = calcular_distancia(
            pos_intersections[list(conection)[0]],
            pos_intersections[list(conection)[1]],
        )
    return {indice: round(largo * factor_escala) for indice, largo in lenghts.items()}


def save_centrality(red: str, df: pd.DataFrame) -> Path:
    """Guarda DataFrame de centralidad en centralidad_path."""
    path = centralidad_path(red)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"  Guardado: {path} ({df.shape})")
    return path


def run_step4(redes: list[str] | None = None):
    """Calcula y guarda centralidades para todas las redes."""
    redes = redes or iter_redes()

    for r in redes:
        print(f"\n=== Centralidad: {r} ===")
        df = compute_centrality(r)
        save_centrality(r, df)


if __name__ == "__main__":
    run_step4()
