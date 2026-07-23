#!/usr/bin/env python3
"""
Paso 8: Barrido de umbral para una combinación (red, radio, steps, topología).
Encuentra threshold que maximiza R².
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import pandas as pd
from src.utils.paths import centralidad_path, combinaciones_path
from src.analysis.threshold import find_optimal_threshold, threshold_sweep_all_topologies


def main():
    parser = argparse.ArgumentParser(description="Paso 8: Barrido umbral óptimo")
    parser.add_argument("--red", choices=["N505", "N1207"], required=True)
    parser.add_argument("--radio", type=int, choices=[0,1,2,3], required=True)
    parser.add_argument("--steps", type=int, choices=[2,5,9], required=True)
    parser.add_argument("--topology", choices=["BC","DiBC","CC","DiCC","DC","DiDC"], 
                       help="Topología específica (default: todas)")
    parser.add_argument("--n-thresholds", type=int, default=200)
    args = parser.parse_args()
    
    print(f"=== Paso 8: Threshold sweep {args.red} r{args.radio}s{args.steps+1} ===")
    
    datos_comp = pd.read_csv(centralidad_path(args.red))
    datos_obs = pd.read_csv(combinaciones_path('mean', args.red, args.radio, args.steps))
    
    if args.topology:
        res = find_optimal_threshold(datos_comp, datos_obs, args.topology, n_thresholds=args.n_thresholds)
        if "error" in res:
            print(f"Error: {res['error']}")
            return
        print(f"\n=== {args.topology} ===")
        print(f"  Threshold óptimo: {res['best_threshold']:.3f}")
        print(f"  R² máximo: {res['best_r2']:.4f}")
        print(f"  Slope: {res['best_slope']:.4f}")
        print(f"  Puntos usados: {res['n_points_used']}")
    else:
        df = threshold_sweep_all_topologies(
            pd.read_csv("data/processed/DataNetwork/StreetAsNode/all_data_SimpleNet_new.csv" if args.red=="N505" else "data/processed/DataNetwork/StreetAsNode/all_data_ComplexNet_new.csv"),
            pd.read_csv(combinaciones_path('mean', args.red, args.radio, args.steps)),
            n_thresholds=args.n_thresholds
        )
        print(df.to_string(index=False))


if __name__ == "__main__":
    main()