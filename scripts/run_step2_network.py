#!/usr/bin/env python3
"""
Paso 2: Construcción manual de red (GUI Pygame).
Lanza NetworkCreator.py para dibujar nodos y conexiones.
"""

import sys
from src.manual_network.NetworkCreator import create_initial_menu

if __name__ == "__main__":
    print("=== Paso 2: Creación de Red Manual ===")
    print("Controles: N=nodo, L=enlace, Ctrl+S=guardar, Ctrl+Z=deshacer")
    print("Guarda como 'PuntaArenas' (N505) y 'PuntaArenasDetallado' (N1207)")
    create_initial_menu()