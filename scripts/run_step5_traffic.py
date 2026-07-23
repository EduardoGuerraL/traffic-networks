#!/usr/bin/env python3
"""
Paso 5: Extracción de tráfico desde imágenes.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analysis.extract_traffic import run_step5

if __name__ == "__main__":
    run_step5()