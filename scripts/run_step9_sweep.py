#!/usr/bin/env python3
"""
Paso 9: Barrido completo (sweep) - El objetivo principal.
Combinaciones: 2 redes × 4 radios × 3 steps × 6 topologías = 144 combinaciones
Para cada una: barrido de 200 umbrales → max R²
Salida: results/sweep_ranking.csv con ranking global.
"""

import argparse
import pandas as pd
import numpy as np
import scipy.stats
from pathlib import Path
from src.analysis.extract_traffic import ImageProcessor, TrafficConfig
from src.utils.paths import (
    get_config, combinaciones_path, centralidad_path,
    iter_redes, iter_radios, iter_steps, iter_topologia,
    n_boxes_for, sweep_csv_path, sweep_dir
)
from src.utils.basics import crearNintervalosOrdenados, obtener_nombres_con_H_M_sinFDS


def calculate_median_positions(X: list, Y: list, box_count: int):
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, box_count)
    y_median = [np.median(sub) for sub in intervalos_Y]
    x_median = []
    for i in range(box_count):
        if intervalos_X[i]:
            ancho = intervalos_X[i][-1] - intervalos_X[i][0]
            x_median.append(intervalos_X[i][-1] - ancho / 2)
    return y_median, x_median


def sweep_thresholds(slopes: list, per95: list, n_thresholds: int = 200) -> dict:
    """
    Barrido de umbrales para encontrar R² máximo.
    Returns: dict con best_threshold, best_r2, best_slope, n_points
    """
    if len(slopes) < 3:
        return {"best_threshold": None, "best_r2": -1, "best_slope": None, "n_points": len(slopes)}
    
    slopes = np.array(slopes)
    per95 = np.array(per95)
    
    # Rango de umbrales: min a max*0.8
    t_min, t_max = per95.min(), per95.max() * 0.8
    thresholds = np.linspace(t_min, t_max, n_thresholds)
    
    best_r2 = -1
    best_thr = None
    best_slope = None
    
    for thr in thresholds:
        mask = per95 >= thr
        if mask.sum() < 3:
            continue
        x_f = slopes[mask].reshape(-1, 1)
        y_f = per95[mask]
        model = LinearRegression().fit(x_f, y_f)
        r2 = model.score(x_f, y_f)
        if r2 > best_r2:
            best_r2 = r2
            best_thr = thr
            best_slope = model.coef_[0]
    
    return {
        "best_threshold": best_thr,
        "best_r2": best_r2,
        "best_slope": best_slope,
        "n_points": int((per95 >= best_thr).sum()) if best_thr else 0,
    }


def compute_slopes_per95(
    datos_obs: pd.DataFrame,
    datos_comp: np.ndarray,
    n_boxes: int
) -> tuple[list, list]:
    """
    Para cada instante temporal, calcula slope (medianas) y P95.
    Returns: (slopes, per95)
    """
    cfg = get_config()
    time_cols = [c for c in datos_obs.columns if c not in ['connection', 'lanes', 'length']]
    if cfg.solo_dias_semana:
        time_cols = obtener_nombres_con_H_M_sinFDS(time_cols)
    
    # Normalizar datos computacionales
    data_comp = (datos_comp - datos_comp.min()) / (datos_comp.max() - datos_comp.min())
    
    slopes = []
    per95 = []
    
    for col in time_cols:
        obs_vals = datos_obs[col].values / 255.0
        means = obs_vals
        p95 = np.percentile(means, 95)
        
        y_med, x_med = calculate_median_positions(data_comp, means, n_boxes)
        if len(x_med) >= 2:
            slope, _, _, _, _ = scipy.stats.linregress(x_med, y_med)
            slopes.append(slope)
            per95.append(p95)
    
    return slopes, per95


def run_full_sweep(
    redes: list[str] | None = None,
    radios: list[int] | None = None,
    steps_list: list[int] | None = None,
    topologias: list[str] | None = None,
    n_thresholds: int = 200,
    output_csv: str | None = None,
) -> pd.DataFrame:
    """
    Barrido completo de todas las combinaciones.
    
    Returns DataFrame con columnas:
    red, radio, steps, topologia, threshold_opt, R2_max, slope_opt, n_points
    """
    cfg = get_config()
    
    redes = redes or iter_redes()
    radios = radios or iter_radios()
    steps_list = steps_list or iter_steps()
    topologias = topologias or iter_topologia()
    
    print(f"=== SWEEP COMPLETO ===")
    print(f"Redes: {redes}")
    print(f"Radios: {radios}")
    print(f"Steps: {steps_list} (S=steps+1)")
    print(f"Topologías: {topologias}")
    print(f"Umbrales por combinación: {n_thresholds}")
    
    total = len(redes) * len(radios) * len(steps_list) * len(topologias)
    print(f"Total combinaciones: {total}")
    
    results = []
    count = 0
    
    for red in redes:
        # Cargar datos computacionales una vez por red
        df_comp = pd.read_csv(centralidad_path(red))
        
        for radio in radios:
            for steps in steps_list:
                # Cargar datos observacionales una vez por (red, radio, steps)
                mean_path = combinaciones_path('mean', red, radio, steps)
                if not mean_path.exists():
                    print(f"  [SKIP] {red} r{radio}s{steps+1}: no existe")
                    continue
                
                df_obs = pd.read_csv(mean_path)
                
                for topo in topologias:
                    count += 1
                    print(f"  [{count}/{total}] {red} r{radio}s{steps+1} {topo}...", end=" ", flush=True)
                    
                    if topo not in df_comp.columns:
                        print("TOPO NO EXISTE")
                        continue
                    
                    n_boxes = n_boxes_for(topo)
                    data_comp = df_comp[topo].values
                    
                    slopes, per95 = compute_slopes_per95(df_obs, data_comp, n_boxes)
                    
                    if len(slopes) < 3:
                        print("DATOS INSUFICIENTES")
                        continue
                    
                    sweep_result = sweep_thresholds(slopes, per95, n_thresholds)
                    
                    results.append({
                        "red": red,
                        "radio": radio,
                        "steps": steps,
                        "S": steps + 1,
                        "topologia": topo,
                        "threshold_opt": sweep_result["best_threshold"],
                        "R2_max": sweep_result["best_r2"],
                        "slope_opt": sweep_result["best_slope"],
                        "n_points": sweep_result["n_points"],
                        "n_instantes": len(slopes),
                    })
                    
                    print(f"R²={sweep_result['best_r2']:.4f} thr={sweep_result['best_threshold']:.4f}")
    
    df = pd.DataFrame(results)
    df = df.sort_values("R2_max", ascending=False).reset_index(drop=True)
    
    if output_csv:
        output_csv = Path(output_csv)
        output_csv.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_csv, index=False)
        print(f"\nGuardado: {output_csv}")
    
    return df


def main():
    parser = argparse.ArgumentParser(description="Paso 9: Barrido completo (Sweep)")
    parser.add_argument("--red", choices=["N505", "N1207"], help="Red específica")
    parser.add_argument("--radio", type=int, choices=[0,1,2,3], help="Radio específico")
    parser.add_argument("--steps", type=int, choices=[2,5,9], help="Steps específico")
    parser.add_argument("--topologia", choices=["BC", "DiBC", "CC", "DiCC", "DC", "DiDC"], help="Topología específica")
    parser.add_argument("--n-thresholds", type=int, default=200, help="Puntos de barrido de umbral")
    parser.add_argument("-o", "--output", default="results/sweep_ranking.csv", help="CSV de salida")
    args = parser.parse_args()
    
    redes = [args.red] if args.red else None
    radios = [args.radio] if args.radio is not None else None
    steps_list = [args.steps] if args.steps is not None else None
    topologias = [args.topologia] if args.topologia else None
    
    run_full_sweep(
        redes=redes,
        radios=radios,
        steps_list=steps_list,
        topologias=topologias,
        n_thresholds=args.n_thresholds,
        output_csv=args.output,
    )


if __name__ == "__main__":
    main()