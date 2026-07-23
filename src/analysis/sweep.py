"""
Paso 9: Barrido completo (Full Sweep).
Ejecuta todas las combinaciones: 2 redes × 4 radios × 3 steps × 6 topologías × 200 umbrales.
Genera CSV ranking con la mejor combinación global.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from itertools import product
import time

from src.utils.paths import (
    get_config,
    centralidad_path,
    combinaciones_path,
    iter_redes,
    iter_radios,
    iter_steps,
    iter_topologia,
    sweep_csv_path,
    results_dir,
)
from src.analysis.correlate import correlate_stepwise
from src.analysis.threshold import find_optimal_threshold


def run_single_sweep(
    red: str,
    radio: int,
    steps: int,
    topologies: list[str] | None = None,
    n_thresholds: int = 200,
) -> list[dict]:
    """
    Ejecuta barrido de umbrales para una combinación (red, radio, steps).
    Returns lista de dicts con resultados por topología.
    """
    # Cargar datos
    datos_comp = pd.read_csv(centralidad_path(red))
    mean_path = combinaciones_path('mean', red, radio, steps)
    
    if not mean_path.exists():
        return [{"error": f"no existe {mean_path}"}]
    
    datos_obs = pd.read_csv(mean_path)
    
    topologies = topologies or ['BC', 'DiBC', 'CC', 'DiCC', 'DC', 'DiDC']
    results = []
    
    for topo in topologies:
        res = find_optimal_threshold(
            datos_comp, datos_obs, topo,
            n_thresholds=n_thresholds
        )
        if "error" not in res:
            results.append({
                'red': red,
                'radio': radio,
                'steps': steps,
                'S': steps + 1,
                'topology': topo,
                'threshold': res['best_threshold'],
                'r2': res['best_r2'],
                'slope': res['best_slope'],
                'n_points': res['n_points_used'],
            })
    
    return results


def run_full_sweep(
    redes: list[str] | None = None,
    radios: list[int] | None = None,
    steps_list: list[int] | None = None,
    topologies: list[str] | None = None,
    n_thresholds: int = 200,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """
    Barrido completo sobre todas las combinaciones.
    
    Returns:
        DataFrame con columnas: red, radio, steps, S, topology, threshold, r2, slope, n_points
        Ordenado por R² descendente.
    """
    cfg = get_config()
    redes = redes or iter_redes()
    radios = radios or iter_radios()
    steps_list = steps_list or iter_steps()
    topologies = topologies or iter_topologia()
    output = output_path or sweep_csv_path()
    
    total = len(redes) * len(radios) * len(steps_list)
    print(f"\n=== FULL SWEEP ===")
    print(f"Redes: {redes}")
    print(f"Radios: {radios}")
    print(f"Steps: {steps_list} (S = steps+1)")
    print(f"Topologías: {topologies}")
    print(f"Total combinaciones red×radio×steps: {total}")
    print(f"Umbrales por topología: {n_thresholds}")
    print(f"Output: {output}")
    
    all_results = []
    count = 0
    start = time.time()
    
    for red, radio, steps in product(redes, radios, steps_list):
        count += 1
        print(f"\n[{count}/{total}] {red} r{radio}s{steps+1}")
        
        try:
            res = run_single_sweep(red, radio, steps, topologies, n_thresholds)
            all_results.extend(res)
        except Exception as e:
            print(f"  ERROR: {e}")
            all_results.append({
                'red': red, 'radio': radio, 'steps': steps, 'S': steps+1,
                'topology': 'ERROR', 'threshold': None, 'r2': None, 'slope': None,
                'n_points': 0, 'error': str(e)
            })
    
    df = pd.DataFrame(all_results)
    df = df.sort_values('r2', ascending=False).reset_index(drop=True)
    
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    
    elapsed = time.time() - start
    print(f"\n{'='*50}")
    print(f"Completado en {elapsed/60:.1f} min")
    print(f"Resultados guardados en: {output}")
    print(f"Total filas: {len(df)}")
    
    # Top 10
    print("\n--- TOP 10 ---")
    print(df.head(10).to_string(index=False))
    
    return df


def run_sweep_and_report(
    top_n: int = 20,
    **kwargs,
) -> pd.DataFrame:
    """Ejecuta sweep y muestra reporte resumido."""
    df = run_full_sweep(**kwargs)
    
    print(f"\n=== REPORTE: Top {top_n} ===")
    for i, row in df.head(top_n).iterrows():
        print(f"  {i+1:2d}. {row['red']} r{row['radio']}s{row['S']} "
              f"{row['topology']:6s} → R²={row['r2']:.4f} "
              f"(thr={row['threshold']:.3f}, slope={row['slope']:.3f}, "
              f"n={int(row['n_points'])})")
    
    return df


if __name__ == "__main__":
    # Ejecución completa
    df = run_sweep_and_report()