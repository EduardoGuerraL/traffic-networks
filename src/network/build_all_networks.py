"""
Script de migración: construye ambas redes (N505, N1207) y las serializa.

Ejecutar desde la raíz del proyecto:
    python -m src.network.build_all_networks
"""

from __future__ import annotations

import sys
from pathlib import Path

# Asegurar que la raíz del proyecto esté en sys.path
_project_root = str(Path(__file__).resolve().parent.parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from src.network.build_network import NetworkBuilder
from src.network.load_network import NetworkGraphLoader
from src.utils.paths import get_config


def build_and_save(red_key: str) -> None:
    """
    Construye una red, la serializa y verifica que se puede cargar.

    Args:
        red_key: Clave de la red en pipeline.yaml ('N505' o 'N1207').
    """
    cfg = get_config()
    red = cfg.redes[red_key]

    print(f"\n{'='*60}")
    print(f"  Construyendo red: {red.nombre} ({red.nodos} nodos esperados)")
    print(f"{'='*60}")

    # Directorio de datos originales
    dat_dir = red.network_data
    print(f"  Fuente .dat:     {dat_dir}")

    # Directorio de imagen de referencia
    img_path = cfg.imagenes_dir / cfg.imagenes_referencia
    print(f"  Imagen ref:      {img_path}")

    # Directorio de salida serializado
    output_dir = Path(_project_root) / "data" / "network" / "serialized" / red_key
    print(f"  Serializar en:   {output_dir}")

    # --- Construir ---
    print(f"\n  [1/3] Construyendo grafos...")
    builder = NetworkBuilder(str(dat_dir), str(img_path))
    builder.build()

    print(f"    DG_inter:  {builder.DG_inter.number_of_nodes()} nodos, {builder.DG_inter.number_of_edges()} aristas")
    print(f"    UG_inter:  {builder.UG_inter.number_of_nodes()} nodos, {builder.UG_inter.number_of_edges()} aristas")
    print(f"    DG_streets: {builder.DG_streets.number_of_nodes()} nodos, {builder.DG_streets.number_of_edges()} aristas")
    print(f"    UG_streets: {builder.UG_streets.number_of_nodes()} nodos, {builder.UG_streets.number_of_edges()} aristas")

    # --- Serializar ---
    print(f"\n  [2/3] Serializando...")
    pkl_path, json_path = builder.save(str(output_dir))
    print(f"    Grafos:    {pkl_path}")
    print(f"    Metadata:  {json_path}")

    # --- Verificar carga ---
    print(f"\n  [3/3] Verificando carga...")
    loader = NetworkGraphLoader.load(str(output_dir))
    assert loader.num_streets == builder.num_streets, (
        f"Verification failed: {loader.num_streets} != {builder.num_streets}"
    )
    assert loader.num_intersections == builder.num_intersections, (
        f"Verification failed: {loader.num_intersections} != {builder.num_intersections}"
    )
    print(f"    OK - {loader}")

    print(f"\n  Red {red_key} serializada exitosamente en {output_dir}")


def main() -> None:
    """Construye y serializa todas las redes definidas en pipeline.yaml."""
    cfg = get_config()

    print("=" * 60)
    print("  SERIALIZACIÓN DE REDES VIALES")
    print("=" * 60)

    for red_key in cfg.redes:
        build_and_save(red_key)

    print("\n" + "=" * 60)
    print("  TODAS LAS REDES PROCESADAS")
    print("=" * 60)


if __name__ == "__main__":
    main()
