#!/usr/bin/env python3
"""
Pipeline principal - orquesta pasos 2→9.
Uso: python scripts/run_pipeline.py [--from-step N] [--to-step N] [--only-step N]
"""

from __future__ import annotations
import sys
import subprocess
from pathlib import Path


STEPS = {
    2: ("run_step2_network", [], "Red manual (GUI)"),
    4: ("run_step4_centrality", [], "Centralidad (BC/CC/DC Dir/NoDir)"),
    5: ("run_step5_traffic", [], "Extracción tráfico imágenes"),
    6: ("run_step6_combinations", [], "Generar 48 combinaciones R×S"),
    7: ("run_step7_correlate", [], "Correlación comp vs obs (slope, R², P95)"),
    8: ("run_step8_threshold", [], "Barrido umbral → max R²"),
    9: ("run_step9_sweep", [], "Barrido completo → ranking CSV"),
}


def run_step(step_num: int, args: list) -> bool:
    """Ejecuta un script de paso."""
    if step_num not in STEPS:
        print(f"❌ Paso {step_num} no definido")
        return False
    
    script_name, _, desc = STEPS[step_num]
    script_path = Path(__file__).parent / f"{script_name}.py"
    
    if not script_path.exists():
        print(f"❌ No existe: {script_path}")
        return False
    
    cmd = [sys.executable, str(script_path)] + args
    print(f"\n{'='*60}")
    print(f"PASO {step_num}: {desc}")
    print(f"Comando: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    result = subprocess.run(cmd)
    return result.returncode == 0


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline Punta Arenas Traffic")
    parser.add_argument("--from-step", type=int, default=2, help="Primer paso a ejecutar")
    parser.add_argument("--to-step", type=int, default=9, help="Último paso a ejecutar")
    parser.add_argument("--only-step", type=int, help="Ejecutar solo este paso")
    parser.add_argument("--list", action="store_true", help="Listar pasos disponibles")
    
    args = parser.parse_args()
    
    if args.list:
        print("Pasos disponibles:")
        for n, (_, _, desc) in STEPS.items():
            print(f"  {n}: {desc}")
        return
    
    if args.only_step:
        steps_to_run = [args.only_step]
    else:
        steps_to_run = list(range(args.from_step, args.to_step + 1))
    
    print(f"Ejecutando pasos: {steps_to_run}")
    
    for step in steps_to_run:
        if not run_step(step, []):
            print(f"\n❌ Pipeline falló en paso {step}")
            sys.exit(1)
    
    print("\n✅ Pipeline completado exitosamente")


if __name__ == "__main__":
    main()