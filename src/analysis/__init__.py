"""
src.analysis - Analytical pipeline modules.

Modules:
- correlate:    Paso 7 - computational vs observational correlation per timestep
- threshold:    Paso 8 - sweep thresholds to maximize R²
- sweep:        Paso 9 - full sweep across all combinations → ranking CSV
"""

from .correlate import correlate_stepwise
from .threshold import find_optimal_threshold
from .sweep import run_full_sweep

__all__ = [
    "correlate_stepwise",
    "find_optimal_threshold",
    "run_full_sweep",
]
