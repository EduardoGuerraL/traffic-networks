"""
src.analysis - Core analytical pipeline modules.

Modules:
- compute_centrality: Paso 4 - compute BC/CC/DC (dir/undir) for both networks
- extract_traffic:    Paso 5 - extract traffic values from images (with weekday filter)
- correlate:          Paso 7 - computational vs observational correlation per timestep
- threshold:          Paso 8 - sweep thresholds to maximize R²
- sweep:              Paso 9 - full sweep across all combinations → ranking CSV
"""

from .compute_centrality import compute_centrality, save_centrality
from .correlate import correlate_stepwise
from .threshold import find_optimal_threshold
from .sweep import run_full_sweep

__all__ = [
    "compute_centrality",
    "save_centrality",
    "correlate_stepwise",
    "find_optimal_threshold",
    "run_full_sweep",
]
