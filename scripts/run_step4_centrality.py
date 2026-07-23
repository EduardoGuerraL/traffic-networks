#!/usr/bin/env python3
"""
Paso 4: Cálculo de centralidad (BC, CC, DC dirigidas/no dirigidas).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analysis.centrality import run_step4

if __name__ == "__main__":
    run_step4()