"""
Paso 8: Búsqueda de umbral óptimo (threshold sweep).
Para una combinación (red, radio, steps, topología): barrer threshold en P95 → max R².
"""

from __future__ import annotations
import numpy as np
import pandas as pd
import scipy.stats
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from src.analysis.correlate import correlate_stepwise


def find_optimal_threshold(
    datos_comp: pd.DataFrame,
    datos_obs: pd.DataFrame,
    topology_index: str,
    n_thresholds: int = 200,
    threshold_range_factor: float = 0.8,
) -> dict:
    """
    Barrer umbrales de P95 y encontrar el que maximiza R².
    
    Args:
        datos_comp: DataFrame con centralidades
        datos_obs: DataFrame con tráfico observacional
        topology_index: columna de centralidad (e.g. 'DiCC')
        n_thresholds: número de puntos de umbral a probar
        threshold_range_factor: límite superior = max(P95) * factor
    
    Returns:
        dict con: best_threshold, best_r2, best_slope, all_thresholds, all_r2, all_slopes
    """
    slopes, per95, _ = correlate_stepwise(datos_comp, datos_obs, topology_index)
    
    if len(slopes) < 2:
        return {"error": "insuficientes puntos"}
    
    # Rango de umbrales
    p95_min = np.min(per95)
    p95_max = np.max(per95) * threshold_range_factor
    thresholds = np.linspace(p95_min, p95_max, n_thresholds)
    
    best_r2 = -1
    best_thr = None
    best_slope = None
    all_r2 = []
    all_slopes = []
    
    for thr in thresholds:
        mask = per95 >= thr
        if np.sum(mask) < 3:
            all_r2.append(0)
            all_slopes.append(0)
            continue
        
        X = slopes[mask].reshape(-1, 1)
        Y = per95[mask]
        
        model = LinearRegression().fit(X, Y)
        y_pred = model.predict(X)
        r2 = r2_score(Y, y_pred)
        
        all_r2.append(r2)
        all_slopes.append(model.coef_[0])
        
        if r2 > best_r2:
            best_r2 = r2
            best_thr = thr
            best_slope = model.coef_[0]
    
    return {
        "topology_index": topology_index,
        "best_threshold": float(best_thr) if best_thr else None,
        "best_r2": float(best_r2),
        "best_slope": float(best_slope) if best_slope else None,
        "n_points_used": int(np.sum(per95 >= best_thr)) if best_thr else 0,
        "thresholds": thresholds.tolist(),
        "r2_values": all_r2,
        "slope_values": all_slopes,
    }


def threshold_sweep_all_topologies(
    datos_comp: pd.DataFrame,
    datos_obs: pd.DataFrame,
    topologies: list[str] | None = None,
    **kwargs,
) -> pd.DataFrame:
    """
    Ejecuta barrido de umbrales para múltiples topologías.
    Returns DataFrame con resultados por topología.
    """
    if topologies is None:
        topologies = ['BC', 'DiBC', 'CC', 'DiCC', 'DC', 'DiDC']
    
    results = []
    for topo in topologies:
        print(f"  Threshold sweep: {topo}...")
        res = find_optimal_threshold(datos_comp, datos_obs, topo, **kwargs)
        if "error" not in res:
            results.append({
                'topology': topo,
                'threshold': res['best_threshold'],
                'r2': res['best_r2'],
                'slope': res['best_slope'],
                'n_points': res['n_points_used'],
            })
    
    return pd.DataFrame(results)


if __name__ == "__main__":
    # Test
    from src.utils.paths import centralidad_path
    datos_comp = pd.read_csv(centralidad_path("N505"))
    datos_obs = pd.read_csv("data/processed/combinaciones/traffic_mean_N505_r1s6.csv")
    
    res = find_optimal_threshold(datos_comp, datos_obs, "DiCC")
    print(f"Best: thr={res['best_threshold']:.3f}, R²={res['best_r2']:.3f}, slope={res['best_slope']:.3f}")
    
    df = threshold_sweep_all_topologies(datos_comp, datos_obs)
    print(df)