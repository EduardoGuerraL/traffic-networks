#!/usr/bin/env python3
"""
Paso 6: Generar todas las combinaciones R×S (48 CSVs).
Llama a generar_combinaciones.py existente.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import generar_combinaciones

if __name__ == "__main__":
    print("=== Paso 6: Generando combinaciones R×S ===")
    # generar_combinaciones.py ya tiene su main