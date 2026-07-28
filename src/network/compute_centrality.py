"""
Genera y guarda los datos computacionales de ambas redes serializadas.

Salida:
    data/network/serialized/{N505,N1207}/centrality/
        - indices_centralidad.csv   (DiBC, DiCC, DiDC, BC, CC, DC)
        - all_data.csv              (centralidad + conections)
"""

from __future__ import annotations

import sys
from pathlib import Path

import networkx as nx
import pandas as pd
import numpy as np
import math

_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.network.load_network import NetworkGraphLoader


SERIALIZED_DIR = Path(_project_root) / "data" / "network" / "serialized"

NETWORKS = {
    "N505": SERIALIZED_DIR / "N505",
    "N1207": SERIALIZED_DIR / "N1207",
}


def compute_centrality(loader: NetworkGraphLoader) -> pd.DataFrame:
    """Calcula centralidades desde la red serializada."""
    DG_streets = loader.DG_streets
    UG_streets = loader.UG_streets

    nodes = sorted(DG_streets.nodes())
    inter_conections = loader.inter_conections
    conections = {i: tuple(c) for i, c in enumerate(inter_conections)}

    DiBC = nx.betweenness_centrality(DG_streets)
    DiCC = nx.closeness_centrality(DG_streets)
    DiDC = nx.degree_centrality(DG_streets)
    BC = nx.betweenness_centrality(UG_streets)
    CC = nx.closeness_centrality(UG_streets)
    DC = nx.degree_centrality(UG_streets)

    df = pd.DataFrame({
        "Nodo": nodes,
        "Conections": [str(conections[n]) for n in nodes],
        "DiBC": [DiBC[n] for n in nodes],
        "DiCC": [DiCC[n] for n in nodes],
        "DiDC": [DiDC[n] for n in nodes],
        "BC": [BC[n] for n in nodes],
        "CC": [CC[n] for n in nodes],
        "DC": [DC[n] for n in nodes],
    })
    df.set_index("Nodo", inplace=True)
    return df


def main():
    for red_key, net_dir in NETWORKS.items():
        print(f"\n=== {red_key} ===")

        loader = NetworkGraphLoader.load(str(net_dir))
        print(f"  Cargada: {loader}")

        df = compute_centrality(loader)

        out_dir = net_dir / "centrality"
        out_dir.mkdir(parents=True, exist_ok=True)

        # Guardar solo centralidad
        centrality_path = out_dir / "indices_centralidad.csv"
        df.to_csv(centrality_path)
        print(f"  Guardado: {centrality_path} ({df.shape})")

        # Guardar all_data (mismo formato que los CSVs originales en ResultData)
        all_data_path = out_dir / "all_data.csv"
        df.to_csv(all_data_path)
        print(f"  Guardado: {all_data_path} ({df.shape})")

    print("\nListo.")


if __name__ == "__main__":
    main()
