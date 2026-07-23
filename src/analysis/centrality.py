"""
Paso 4: Cálculo de centralidad de redes.
Genera BC, CC, DC para dirigidas y no dirigidas × 2 redes = 12 combinaciones.
"""

from __future__ import annotations
from pathlib import Path
import networkx as nx
import pandas as pd

from src.utils.paths import (
    get_config,
    network_data_path,
    centralidad_path,
    iter_redes,
    iter_topologia,
)


def compute_centrality(red: str) -> pd.DataFrame:
    """
    Calcula todas las centralidades para una red.
    Returns DataFrame con columnas: BC, CC, DC, DiBC, DiCC, DiDC, MaxOcupation, etc.
    """
    cfg = get_config()
    net_dir = network_data_path(red)
    img_ref = cfg.imagenes_dir / cfg.imagenes_referencia
    
    # Usar la clase NetworkData existente
    from src.network.GetDataFromNetwork import NetworkData
    
    nd = NetworkData(str(net_dir), str(img_ref))
    
    # Grafos
    DG_inter = nd.DG_inter
    UG_inter = nd.UG_inter
    DG_streets = nd.DG_streets
    UG_streets = nd.UG_streets
    
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
    results['DC_inter'] = nx.degree_centrality(UG_inter)
    
    # Random walk analytic
    results['mean_state_RW'] = nd.randomwalkAnalitic_edges()
    results['mean_state_RW_lim'] = nd.randomwalkAnalitic_nodes()
    
    # Max occupation (Ehrenfest scaling)
    results['MaxOcupation'] = nd.getMaxParticlesPerUrns()
    
    # Build DataFrame
    n_nodes = len(DG_streets.nodes())
    df = pd.DataFrame(index=range(n_nodes))
    for col, vals in results.items():
        df[col] = [vals.get(i, 0) for i in range(n_nodes)]
    
    return df


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