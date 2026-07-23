#!/usr/bin/env python3
"""
Paso 7: Correlación comp vs obs por instante (slope, R², P95).
Genera figuras para una combinación dada.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import argparse
import pandas as pd
from src.utils.paths import centralidad_path, combinaciones_path
from src.analysis.correlate import correlate_stepwise, get_traffic_stats_per_instant
from src.analysis.threshold import find_optimal_threshold


def main():
    parser = argparse.ArgumentParser(description="Paso 7: Correlación paso a paso")
    parser.add_argument("--red", choices=["N505", "N1207"], required=True)
    parser.add_argument("--radio", type=int, choices=[0,1,2,3], required=True)
    parser.add_argument("--steps", type=int, choices=[2,5,9], required=True)
    parser.add_argument("--topology", choices=["BC","DiBC","CC","DiCC","DC","DiDC"], default="DiCC")
    parser.add_argument("--output-dir", default="results/figures")
    args = parser.parse_args()
    
    print(f"=== Paso 7: Correlación {args.red} r{args.radio}s{args.steps+1} {args.topology} ===")
    
    datos_comp = pd.read_csv(centralidad_path(args.red))
    datos_obs = pd.read_csv(combinaciones_path('mean', args.red, args.radio, args.steps))
    
    slopes, per95, r2s = correlate_stepwise(datos_comp, datos_obs, args.topology)
    
    print(f"Instantes: {len(slopes)}")
    print(f"Slope medio: {slopes.mean():.4f} ± {slopes.std():.4f}")
    print(f"P95 medio: {per95.mean():.4f}")
    print(f"R² medio: {r2s.mean():.4f}")
    
    # Umbral óptimo
    res = find_optimal_threshold(datos_comp, datos_obs, args.topology)
    print(f"\nUmbral óptimo: thr={res['best_threshold']:.3f}, R²={res['best_r2']:.3f}, slope={res['best_slope']:.3f}")


if __name__ == "__main__":
    main()