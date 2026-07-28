"""
Paso 7: Correlación paso a paso (instante × instante).
Para cada instante temporal: reg lineal (centralidad vs tráfico) → slope, R², P95.
"""

from __future__ import annotations
import numpy as np
import pandas as pd
import scipy.stats
from src.utils.paths import centralidad_path, n_boxes_for
from src.utils.basics import crearNintervalosOrdenados


def calculate_median_positions(X: list, Y: list, box_count: int) -> tuple[list, list]:
    """Calcula medianas de Y por intervalos de X (boxplot cuantílico)."""
    intervalos_X, intervalos_Y = crearNintervalosOrdenados(X, Y, box_count)
    x_median = []
    y_median = []
    for i in range(box_count):
        if intervalos_X[i]:
            ancho = intervalos_X[i][-1] - intervalos_X[i][0]
            x_median.append(intervalos_X[i][-1] - ancho / 2)
            y_median.append(np.median(intervalos_Y[i]))
    return x_median, y_median


def correlate_stepwise(
    datos_comp: pd.DataFrame,
    datos_obs: pd.DataFrame,
    topology_index: str,
    n_boxes: int | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Para cada instante (columnas de datos_obs): regresión lineal medianas.
    
    Returns:
        slopes: pendiente por instante (shape: n_instantes)
        per95: percentil 95 de tráfico por instante
        r2_vals: R² de cada regresión
    """
    if n_boxes is None:
        n_boxes = n_boxes_for(topology_index)
    
    data_computational = datos_comp[topology_index].values
    # Normalizar 0-1
    data_computational = (data_computational - data_computational.min()) / (
        data_computational.max() - data_computational.min()
    )
    
    # Columnas de tráfico (excluir metadata)
    meta_cols = ['connection', 'lanes', 'length']
    traffic_cols = [c for c in datos_obs.columns if c not in meta_cols]
    
    slopes = []
    per95 = []
    r2_vals = []
    
    for col in traffic_cols:
        obs_vals = datos_obs[col].values
        obs_vals = obs_vals / 255.0  # normalizar 0-1
        
        x_med, y_med = calculate_median_positions(data_computational, obs_vals, n_boxes)
        
        if len(x_med) < 3:
            slopes.append(0)
            per95.append(np.percentile(obs_vals, 95))
            r2_vals.append(0)
            continue
        
        slope, intercept, r_val, _, _ = scipy.stats.linregress(x_med, y_med)
        slopes.append(slope)
        per95.append(np.percentile(obs_vals, 95))
        r2_vals.append(r_val ** 2)
    
    return np.array(slopes), np.array(per95), np.array(r2_vals)


def get_traffic_stats_per_instant(datos_obs: pd.DataFrame) -> pd.DataFrame:
    """Estadísticas descriptivas de tráfico por instante."""
    meta_cols = ['connection', 'lanes', 'length']
    traffic_cols = [c for c in datos_obs.columns if c not in meta_cols]
    
    stats = []
    for col in traffic_cols:
        vals = datos_obs[col].values / 255.0
        stats.append({
            'instante': col,
            'mean': np.mean(vals),
            'median': np.median(vals),
            'p95': np.percentile(vals, 95),
            'max': np.max(vals),
            'std': np.std(vals),
        })
    return pd.DataFrame(stats)


SLOT_COLUMNS = [f"{h:02d}-{m:02d}" for h in range(24) for m in (0, 15, 30, 45)]


def correlate_with_aggregated(
    datos_comp: pd.DataFrame,
    datos_obs: pd.DataFrame,
    topology_index: str,
    n_boxes: int | None = None,
) -> pd.DataFrame:
    """
    Correlaciona centralidad vs tráfico agregado por slot de 15 min.

    Para cada uno de los 96 slots, calcula pendiente y R² de la regresión
    lineal entre centralidad ( bins cuantílicos ) y tráfico mediano.

    Args:
        datos_comp: DataFrame de centralidad (una fila por arista).
                    Debe contener columna 'Conections' y la topología pedida.
        datos_obs:  DataFrame de tráfico agregado (traffic_stats_*_mean_*.csv).
                    Debe contener 'connection' y columnas de slot 'HH-MM'.
        topology_index: Nombre de la columna de centralidad (p.ej. 'DiCC').
        n_boxes: Número de bins cuantílicos. Si None, usa config.

    Returns:
        DataFrame con columnas: slot, slope, r2, p95, n_used
    """
    if n_boxes is None:
        n_boxes = n_boxes_for(topology_index)

    centr_col = datos_comp[topology_index].values.astype(float)
    c_min, c_max = centr_col.min(), centr_col.max()
    centr_norm = (centr_col - c_min) / (c_max - c_min) if c_max > c_min else centr_col * 0

    comp_conns = datos_comp["Conections"].astype(str).str.strip()
    obs_conns = datos_obs["connection"].astype(str).str.strip()

    common = comp_conns[comp_conns.isin(obs_conns)].index
    if len(common) < 3:
        return pd.DataFrame(columns=["slot", "slope", "r2", "p95", "n_used"])

    centr_aligned = centr_norm[common]
    comp_idx = common

    slot_to_obs_idx = {}
    for slot in SLOT_COLUMNS:
        if slot in datos_obs.columns:
            slot_to_obs_idx[slot] = obs_conns[obs_conns.isin(comp_conns)].index

    results = []
    for slot in SLOT_COLUMNS:
        if slot not in datos_obs.columns:
            results.append({"slot": slot, "slope": np.nan, "r2": np.nan,
                            "p95": np.nan, "n_used": 0})
            continue

        obs_idx = slot_to_obs_idx[slot]
        traffic_vals = datos_obs.loc[obs_idx, slot].values.astype(float)

        mask = ~np.isnan(traffic_vals)
        x = centr_aligned[obs_idx[mask]]
        y = traffic_vals[mask]

        if len(x) < 3:
            results.append({"slot": slot, "slope": 0.0, "r2": 0.0,
                            "p95": np.percentile(y, 95) if len(y) > 0 else 0.0,
                            "n_used": len(x)})
            continue

        x_med, y_med = calculate_median_positions(x.tolist(), y.tolist(), n_boxes)

        if len(x_med) < 3:
            results.append({"slot": slot, "slope": 0.0, "r2": 0.0,
                            "p95": np.percentile(y, 95),
                            "n_used": len(x)})
            continue

        slope, _, r_val, _, _ = scipy.stats.linregress(x_med, y_med)
        results.append({
            "slot": slot,
            "slope": slope,
            "r2": r_val ** 2,
            "p95": np.percentile(y, 95),
            "n_used": len(x),
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    # Test rápido
    datos_comp = pd.read_csv(centralidad_path("N505"))
    datos_obs = pd.read_csv(
        "data/processed/combinaciones/traffic_mean_N505_r1s6.csv"
    )

    slopes, per95, r2s = correlate_stepwise(datos_comp, datos_obs, "DiCC")
    print(f"Slopes: mean={np.mean(slopes):.4f}, std={np.std(slopes):.4f}")
    print(f"P95: mean={np.mean(per95):.4f}")
    print(f"R²: mean={np.mean(r2s):.4f}")