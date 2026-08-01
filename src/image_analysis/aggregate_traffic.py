"""
Paso 5b: Agregación temporal de tráfico.
Agrupa los datos de tráfico por slots de 15 minutos y calcula estadísticas
por calle: media, desviación estándar, mediana, IQR y conteo de observaciones.

Genera 5 CSVs por combinación:
    traffic_stats_{stat}_{red}_r{radio}s{steps}.csv
"""

from __future__ import annotations

import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict

import numpy as np
import pandas as pd

from src.utils.paths import (
    get_config,
    combinaciones_path,
    traffic_stats_dir,
    iter_redes,
    iter_radios,
    iter_steps,
)

# 96 slots de 15 minutos: 00-00, 00-15, 00-30, ..., 23-45
STANDARD_SLOTS = [f"{h:02d}-{m:02d}" for h in range(24) for m in (0, 15, 30, 45)]

META_COLUMNS = {"connection", "lanes", "length"}


# ------------------------------------------------------------------
# Funciones de utilidad
# ------------------------------------------------------------------

def round_to_15min(h: int, m: int) -> tuple[int, int]:
    """Redondea una hora al slot de 15 min más cercano."""
    if m < 8:
        return h, 0
    elif m < 23:
        return h, 15
    elif m < 38:
        return h, 30
    elif m < 53:
        return h, 45
    else:
        return (h + 1) % 24, 0


def _parse_column_name(col_name: str) -> tuple[datetime | None, str | None]:
    """
    Intenta extraer fecha y slot de un nombre de columna tipo '2023-03-29_07-30'.

    Returns:
        (datetime, slot_str) o (None, None) si no es una columna de tiempo.
    """
    parts = col_name.split("_")
    if len(parts) != 2:
        return None, None

    date_str, hm_str = parts
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None, None

    try:
        h_str, m_str = hm_str.split("-")
        h, m = int(h_str), int(m_str)
    except (ValueError, AttributeError):
        return None, None

    rh, rm = round_to_15min(h, m)
    slot = f"{rh:02d}-{rm:02d}"

    return dt, slot


def group_columns_by_slot(
    columns: list[str],
    weekdays_only: bool = True,
) -> dict[str, list[str]]:
    """
    Agrupa columnas de tiempo por slot de 15 minutos.

    Args:
        columns: Lista de nombres de columnas (ej: '2023-03-29_07-30').
        weekdays_only: Si True, excluye fines de semana.

    Returns:
        Dict slot -> lista de nombres de columna originales.
        Ej: {'07-00': ['2023-03-29_07-00', '2023-03-30_07-00', ...], ...}
    """
    slot_to_cols: dict[str, list[str]] = defaultdict(list)

    for col in columns:
        dt, slot = _parse_column_name(col)
        if dt is None:
            continue
        if weekdays_only and dt.weekday() >= 5:
            continue
        slot_to_cols[slot].append(col)

    return dict(slot_to_cols)


# ------------------------------------------------------------------
# Función principal de agregación
# ------------------------------------------------------------------

def aggregate_traffic_csv(
    input_path: Path,
    output_dir: Path,
    weekdays_only: bool = True,
) -> dict[str, Path]:
    """
    Lee un CSV de traffic_mean/max y calcula estadísticas por slot temporal.

    Para cada calle y cada slot de 15 min calcula:
    - mean: promedio de los valores en ese slot
    - std: desviación estándar (Population std, ddof=0)
    - median: mediana
    - iqr: rango intercuartil (Q3 - Q1)
    - count: número de observaciones

    Genera 5 CSVs separados (mean, std, median, iqr, count).

    Args:
        input_path: Ruta al CSV de entrada (traffic_mean o traffic_max).
        output_dir: Directorio donde guardar los CSVs de salida.
        weekdays_only: Si True, solo incluye días laborables.

    Returns:
        Dict nombre_stat -> Path del CSV generado.
    """
    stem = input_path.stem  # ej: traffic_mean_N505_r1s6

    # Extraer info del nombre: traffic_{stat}_{red}_r{radio}s{steps}
    parts = stem.split("_")
    stat_type = parts[1]  # 'mean' o 'max'
    red = parts[2]  # 'N505' o 'N1207'
    radio_steps = "_".join(parts[3:])  # 'r1s6'

    # Leer CSV
    df = pd.read_csv(input_path)

    # Separar metadata vs columnas de tiempo
    time_columns = [c for c in df.columns if c not in META_COLUMNS and c != "CleanScreenshot"]

    # Agrupar columnas por slot
    slot_to_cols = group_columns_by_slot(time_columns, weekdays_only=weekdays_only)

    # Calcular estadísticas por slot
    stats_mean = {}
    stats_std = {}
    stats_median = {}
    stats_iqr = {}
    stats_count = {}

    for slot in STANDARD_SLOTS:
        cols = slot_to_cols.get(slot, [])
        if not cols:
            # Slot sin datos: llenar con NaN
            stats_mean[slot] = np.nan
            stats_std[slot] = np.nan
            stats_median[slot] = np.nan
            stats_iqr[slot] = np.nan
            stats_count[slot] = 0
            continue

        slot_data = df[cols].values  # shape: (n_streets, n_observations)

        stats_mean[slot] = np.mean(slot_data, axis=1)
        stats_std[slot] = np.std(slot_data, axis=1, ddof=0)
        stats_median[slot] = np.median(slot_data, axis=1)

        q75 = np.percentile(slot_data, 75, axis=1)
        q25 = np.percentile(slot_data, 25, axis=1)
        stats_iqr[slot] = q75 - q25

        stats_count[slot] = len(cols)

    # Construir DataFrames y guardar
    output_dir.mkdir(parents=True, exist_ok=True)
    result_paths = {}

    base_name = f"{stat_type}_{red}_{radio_steps}"

    for stat_name, stat_dict in [
        ("mean", stats_mean),
        ("std", stats_std),
        ("median", stats_median),
        ("iqr", stats_iqr),
    ]:
        # DataFrame: filas = calles, columnas = slots
        data = {}
        for slot in STANDARD_SLOTS:
            val = stat_dict[slot]
            # Si es escalar (NaN), expandir a vector
            if np.isscalar(val):
                data[slot] = np.full(len(df), val)
            else:
                data[slot] = val

        df_out = pd.DataFrame(data, columns=STANDARD_SLOTS)

        # Agregar metadata al inicio
        meta_dict = {}
        for mc in ["connection", "lanes", "length"]:
            if mc in df.columns:
                meta_dict[mc] = df[mc].values

        if meta_dict:
            df_meta = pd.DataFrame(meta_dict)
            df_out = pd.concat([df_meta, df_out], axis=1)

        out_path = output_dir / f"traffic_stats_{stat_name}_{base_name}.csv"
        df_out.to_csv(out_path, index=False)
        result_paths[stat_name] = out_path

    # CSV de conteo (una sola fila con los conteos por slot)
    count_data = {"slot": STANDARD_SLOTS, "count": [stats_count[s] for s in STANDARD_SLOTS]}
    df_count = pd.DataFrame(count_data)
    count_path = output_dir / f"traffic_stats_count_{red}.csv"
    df_count.to_csv(count_path, index=False)
    result_paths["count"] = count_path

    return result_paths


# ------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------

def run_aggregation(
    red: str | None = None,
    radio: int | None = None,
    steps: int | None = None,
    force: bool = False,
):
    """
    Ejecuta la agregación temporal para todas las combinaciones.

    Genera un CSV de conteo por red, ya que el conteo es independiente
    de radio/steps.

    Args:
        red: 'N505' o 'N1207' (None = ambas).
        radio: 0-3 (None = todos).
        steps: 2, 5, 9 (None = todos).
        force: re-procesar aunque exista.
    """
    redes = [red] if red else iter_redes()
    radios = [radio] if radio is not None else iter_radios()
    steps_list = [steps] if steps is not None else iter_steps()

    output_base = traffic_stats_dir()

    total = 0
    for r in redes:
        print(f"\n=== Agregación: {r} ===")

        # Generar CSV de conteo una sola vez por red
        count_path = output_base / f"traffic_stats_count_{r}.csv"

        if not force and count_path.exists():
            print(f"  [SKIP] count (ya existe)")
        else:
            # Usar la primera combinación disponible para calcular conteos
            first_input = combinaciones_path("mean", r, radios[0], steps_list[0])
            if first_input.exists():
                print(f"  [PROCESS] count...", end=" ", flush=True)
                try:
                    aggregate_traffic_csv(first_input, output_base)
                    print("OK")
                except Exception as e:
                    print(f"ERROR: {e}")

        # Generar estadísticas (mean/std/median/iqr) por combinación
        for rad in radios:
            for st in steps_list:
                for stat in ["mean", "max"]:
                    input_path = combinaciones_path(stat, r, rad, st)
                    if not input_path.exists():
                        print(f"  SKIP {stat} r{rad}s{st+1}: archivo no encontrado")
                        continue

                    # Verificar si ya existen los CSVs de salida
                    base_name = f"{stat}_{r}_r{rad}s{st+1}"
                    expected_path = output_base / f"traffic_stats_mean_{base_name}.csv"

                    if not force and expected_path.exists():
                        print(f"  [SKIP] {stat} r{rad}s{st+1} (ya existe)")
                        continue

                    total += 1
                    print(f"  [PROCESS] {stat} r{rad}s{st+1}...", end=" ", flush=True)
                    try:
                        aggregate_traffic_csv(
                            input_path, output_base
                        )
                        print("OK")
                    except Exception as e:
                        print(f"ERROR: {e}")

    print(f"\nTotal procesado: {total} combinaciones")


if __name__ == "__main__":
    run_aggregation()
