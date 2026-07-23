"""
src.analysis - Core analytical pipeline modules.

Modules:
- centrality:     Paso 4 - compute BC/CC/DC (dir/undir) for both networks
- extract_traffic: Paso 5 - extract traffic values from images (with weekday filter)
- combine:        Paso 6 - generate R x S combinations (wraps generar_combinaciones.py)
- correlate:      Paso 7 - computational vs observational correlation per timestep
- threshold:      Paso 8 - sweep thresholds to maximize R²
- sweep:          Paso 9 - full sweep across all combinations → ranking CSV
"""

from .centrality import compute_centrality, save_centrality
from .extract_traffic import extract_traffic, save_traffic
from .combine import generate_combinations
from .correlate import correlate_stepwise, CorrelateResult
from .threshold import find_optimal_threshold, ThresholdResult
from .sweep import run_full_sweep, SweepConfig, SweepRow

__all__ = [
    "compute_centrality",
    "save_centrality",
    "extract_traffic",
    "save_traffic",
    "generate_combinations",
    "correlate_stepwise",
    "CorrelateResult",
    "find_optimal_threshold",
    "ThresholdResult",
    "run_full_sweep",
    "SweepConfig",
    "SweepRow",
]