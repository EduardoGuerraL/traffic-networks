#!/usr/bin/env python3
"""
Barrido completo: centralidad vs tráfico agregado.
Genera un CSV con slope y R² por combinación (red × radio × steps × topología × slot).
"""

from __future__ import annotations
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from src.utils.paths import (
    centralidad_path, combinaciones_dir, iter_redes, iter_radios,
    iter_steps, iter_topologia,
)
from src.analysis.correlate import correlate_with_aggregated, SLOT_COLUMNS


STATS_TYPES = ["mean", "median", "std", "iqr"]
FILTERS = ["weekdays", "allweek"]


def build_output_path(
    base_dir: Path, red: str, radio: int, steps: int,
    stat_type: str, traffic_stat: str, filter_suffix: str,
) -> Path:
    """Construye la ruta de salida para los resultados de correlación."""
    s_label = steps + 1
    fname = f"corr_{stat_type}_{traffic_stat}_{red}_r{radio}s{s_label}_{filter_suffix}.csv"
    return base_dir / fname


def run_single_combination(
    datos_comp: pd.DataFrame,
    red: str,
    radio: int,
    steps: int,
    stat_type: str = "mean",
    traffic_stat: str = "mean",
    filter_suffix: str = "weekdays",
    topologias: list[str] | None = None,
    n_boxes: int | None = None,
) -> pd.DataFrame:
    """
    Correlaciona centralidad vs tráfico agregado para una combinación.

    Returns:
        DataFrame con columnas: topology, slot, slope, r2, p95, n_used
    """
    cdir = combinaciones_dir()
    s_label = steps + 1
    fname = f"traffic_stats_{stat_type}_{traffic_stat}_{red}_r{radio}s{s_label}_{filter_suffix}.csv"
    traffic_path = cdir / fname

    if not traffic_path.exists():
        print(f"  [SKIP] {traffic_path.name}: no existe")
        return pd.DataFrame()

    datos_obs = pd.read_csv(traffic_path)
    topologias = topologias or iter_topologia()

    results = []
    for topo in topologias:
        if topo not in datos_comp.columns:
            print(f"  [SKIP] {topo}: columna no existe en centralidad")
            continue

        df_corr = correlate_with_aggregated(datos_comp, datos_obs, topo, n_boxes=n_boxes)
        df_corr.insert(0, "topology", topo)
        results.append(df_corr)

    if not results:
        return pd.DataFrame()

    return pd.concat(results, ignore_index=True)


def main():
    parser = argparse.ArgumentParser(description="Barrido centralidad vs tráfico agregado")
    parser.add_argument("--red", choices=["N505", "N1207"], help="Red específica")
    parser.add_argument("--radio", type=int, choices=[0, 1, 2, 3], help="Radio específico")
    parser.add_argument("--steps", type=int, choices=[2, 5, 9], help="Steps específico")
    parser.add_argument("--topology", choices=["BC", "DiBC", "CC", "DiCC", "DC", "DiDC"],
                        help="Topología específica")
    parser.add_argument("--stat-type", choices=STATS_TYPES, default="mean",
                        help="Tipo de estadística de tráfico (default: mean)")
    parser.add_argument("--traffic-stat", choices=["mean", "max"], default="mean",
                        help="Estadística de tráfico original (default: mean)")
    parser.add_argument("--filter", choices=FILTERS, default="weekdays",
                        help="Filtro temporal (default: weekdays)")
    parser.add_argument("-o", "--output", default="results/correlation_aggregated.csv",
                        help="CSV de salida")
    args = parser.parse_args()

    redes = [args.red] if args.red else iter_redes()
    radios = [args.radio] if args.radio is not None else iter_radios()
    steps_list = [args.steps] if args.steps is not None else iter_steps()
    topologias = [args.topology] if args.topology else None

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    all_results = []
    total = len(redes) * len(radios) * len(steps_list)
    count = 0

    for red in redes:
        df_comp = pd.read_csv(centralidad_path(red))
        print(f"\n=== {red} ({df_comp.shape[0]} aristas) ===")

        for radio in radios:
            for steps in steps_list:
                count += 1
                s_label = steps + 1
                print(f"  [{count}/{total}] r{radio}s{s_label}...", end=" ", flush=True)

                df_corr = run_single_combination(
                    df_comp, red, radio, steps,
                    stat_type=args.stat_type,
                    traffic_stat=args.traffic_stat,
                    filter_suffix=args.filter,
                    topologias=topologias,
                )

                if df_corr.empty:
                    print("sin datos")
                    continue

                df_corr.insert(0, "red", red)
                df_corr.insert(1, "radio", radio)
                df_corr.insert(2, "steps", steps)
                df_corr.insert(3, "S", steps + 1)
                all_results.append(df_corr)

                mean_r2 = df_corr["r2"].mean()
                print(f"R² medio={mean_r2:.4f}")

    if not all_results:
        print("\nNo se generaron resultados")
        return

    df_final = pd.concat(all_results, ignore_index=True)
    df_final.to_csv(output_path, index=False)
    print(f"\nGuardado: {output_path}")
    print(f"Total filas: {len(df_final)}")

    # Resumen por topología
    print("\n=== Resumen por topología ===")
    summary = df_final.groupby("topology").agg(
        r2_mean=("r2", "mean"),
        r2_median=("r2", "median"),
        slope_mean=("slope", "mean"),
    ).sort_values("r2_mean", ascending=False)
    print(summary.to_string())


if __name__ == "__main__":
    main()
