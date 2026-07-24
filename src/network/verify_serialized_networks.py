"""
Script de verificación: compara centralidades computadas desde redes serializadas
con los CSVs guardados en ResultData/.

Ejecutar desde la raíz del proyecto:
    python -m src.network.verify_serialized_networks
"""

from __future__ import annotations

import sys
from pathlib import Path

import networkx as nx
import pandas as pd
import numpy as np

_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.network.load_network import NetworkGraphLoader


RESULTDATA_DIR = Path(_project_root) / "data" / "processed" / "DataNetwork" / "StreetAsNode" / "ResultData"
SERIALIZED_DIR = Path(_project_root) / "data" / "network" / "serialized"

NETWORK_MAP = {
    "N505": {
        "csv_prefix": "SimpleNet",
        "serialized": SERIALIZED_DIR / "N505",
    },
    "N1207": {
        "csv_prefix": "ComplexNet",
        "serialized": SERIALIZED_DIR / "N1207",
    },
}

TOLERANCE = 1e-10


def compute_centrality_from_serialized(red_key: str) -> pd.DataFrame:
    """Computa centralidades desde la red serializada (misma lógica que el código viejo)."""
    info = NETWORK_MAP[red_key]
    loader = NetworkGraphLoader.load(str(info["serialized"]))

    DG_streets = loader.DG_streets
    UG_streets = loader.UG_streets

    # Nodos ordenados (enteros)
    nodes = sorted(DG_streets.nodes())

    # Directed centralities (sobre DG_streets)
    DiBC = nx.betweenness_centrality(DG_streets)
    DiCC = nx.closeness_centrality(DG_streets)
    DiDC = nx.degree_centrality(DG_streets)

    # Undirected centralities (sobre UG_streets)
    BC = nx.betweenness_centrality(UG_streets)
    CC = nx.closeness_centrality(UG_streets)
    DC = nx.degree_centrality(UG_streets)

    # Conections (same as old code: dict(enumerate(inter_conections)))
    inter_conections = loader.inter_conections
    conections = {i: tuple(c) for i, c in enumerate(inter_conections)}

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


def load_saved_csv(red_key: str) -> pd.DataFrame:
    """Carga el CSV guardado en ResultData/."""
    info = NETWORK_MAP[red_key]
    csv_path = RESULTDATA_DIR / f"{info['csv_prefix']}_IndicesCentralidad.csv"
    df = pd.read_csv(csv_path, index_col="Nodo")
    return df


def compare_values(computed: pd.DataFrame, saved: pd.DataFrame, label: str) -> bool:
    """Compara dos DataFrames columna por columna. Retorna True si son iguales."""
    all_ok = True

    for col in ["DiBC", "DiCC", "DiDC", "BC", "CC", "DC"]:
        if col not in computed.columns:
            print(f"  [FAIL] {label} - Columna '{col}' no encontrada en computed")
            all_ok = False
            continue
        if col not in saved.columns:
            print(f"  [FAIL] {label} - Columna '{col}' no encontrada en saved")
            all_ok = False
            continue

        c_vals = computed[col].values.astype(float)
        s_vals = saved[col].values.astype(float)

        if len(c_vals) != len(s_vals):
            print(f"  [FAIL] {label} - '{col}': distintas longitudes ({len(c_vals)} vs {len(s_vals)})")
            all_ok = False
            continue

        max_diff = np.max(np.abs(c_vals - s_vals))
        mean_diff = np.mean(np.abs(c_vals - s_vals))

        if max_diff < TOLERANCE:
            print(f"  [OK]   {label} - {col:6s}  max_diff={max_diff:.2e}  mean_diff={mean_diff:.2e}")
        else:
            # Find first mismatch
            idx = np.argmax(np.abs(c_vals - s_vals))
            print(f"  [FAIL] {label} - {col:6s}  max_diff={max_diff:.2e}  "
                  f"FIRST MISMATCH at idx={idx}: computed={c_vals[idx]:.15f} vs saved={s_vals[idx]:.15f}")
            all_ok = False

    return all_ok


def compare_conections(computed: pd.DataFrame, saved: pd.DataFrame, label: str) -> bool:
    """Compara la columna Conections."""
    if "Conections" not in computed.columns or "Conections" not in saved.columns:
        print(f"  [SKIP] {label} - Columna 'Conections' no disponible para comparar")
        return True

    match = (computed["Conections"] == saved["Conections"]).all()
    if match:
        print(f"  [OK]   {label} - Conections: todas coinciden")
    else:
        mismatches = (computed["Conections"] != saved["Conections"]).sum()
        print(f"  [FAIL] {label} - Conections: {mismatches} diferencias")
    return match


def main():
    print("=" * 70)
    print("  VERIFICACIÓN: Redes serializadas vs CSVs guardados")
    print("=" * 70)

    all_ok = True

    for red_key in NETWORK_MAP:
        print(f"\n--- {red_key} ---")

        print("  Computando centralidades desde red serializada...")
        computed = compute_centrality_from_serialized(red_key)
        print(f"  shape: {computed.shape}")

        print(f"  Cargando CSV guardado...")
        saved = load_saved_csv(red_key)
        print(f"  shape: {saved.shape}")

        # Compare Conections
        ok_conections = compare_conections(computed, saved, red_key)

        # Compare centrality values
        ok_centrality = compare_values(computed, saved, red_key)

        if ok_conections and ok_centrality:
            print(f"\n  RESULTADO: {red_key} - TODOS LOS VALORES COINCIDEN")
        else:
            print(f"\n  RESULTADO: {red_key} - HAY DIFERENCIAS")
            all_ok = False

    print("\n" + "=" * 70)
    if all_ok:
        print("  VERIFICACIÓN COMPLETA: TODAS LAS REDES COINCIDEN")
    else:
        print("  VERIFICACIÓN COMPLETA: HAY DIFERENCIAS - revisar arriba")
    print("=" * 70)


if __name__ == "__main__":
    main()
