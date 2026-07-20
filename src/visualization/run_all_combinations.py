"""
Runner: genera visualizaciones para todas las combinaciones de red × radio × steps.

Uso:
    python src/visualization/run_all_combinations.py

Salida: PNGs en results/combinaciones/{red}_r{radio}s{steps}/
"""

import os
import sys
import pandas as pd
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from functions.RutasDeArchivos import Datos_computacionales, datos_combinaciones, REDES, RADIOS, STEPS
from src.visualization.Hours_vs_Slope_TrafficScale import run_hours_vs_slope

# Flag para elegir qué visualizaciones generar.
# Solo se genera la figura de Hours_vs_Slope (la más lenta de preparar, pero la
# que entrega la curva de pendientes vs tiempo del día con la barra de tráfico).
GENERAR_SOLO_HOURS_VS_SLOPE = True

# Mapeo red → índice en Datos_computacionales
COMP_INDEX = {"N505": 0, "N1207": 1}

# Topology indices disponibles en los datos computacionales
TOPOLOGY_INDICES = ["DiBC", "BC", "DiCC", "CC", "DiDC", "DC"]

# Modelo óptimo por red (topology_index, threshold)
OPTIMAL_MODELS = {
    "N505": {"topology_index": "DiCC", "threshold": 0.329},
    "N1207": {"topology_index": "DiCC", "threshold": 0.368},
}

# Thresholds para ThreeSlopes (BC, CC, DC)
THREE_SLOPES_THRESHOLDS = {
    "N505": [0.25, 0.332, 0.319],
    "N1207": [0.38, 0.328, 0.305],
}


def run_all():
    total = len(REDES) * len(RADIOS) * len(STEPS)
    count = 0
    start_time = time.time()

    for red in REDES:
        datos_comp = pd.read_csv(Datos_computacionales[COMP_INDEX[red]])

        for radio in RADIOS:
            for steps in STEPS:
                count += 1
                obs_path = datos_combinaciones[red]["mean"][(radio, steps)]
                out_dir = f"results/combinaciones/{red}_r{radio}s{steps}"

                print(f"\n[{count}/{total}] {red} radio={radio} steps={steps}")
                print(f"  Obs: {obs_path}")

                if not os.path.exists(obs_path):
                    print(f"  SKIP: archivo no encontrado")
                    continue

                datos_obs = pd.read_csv(obs_path)
                os.makedirs(out_dir, exist_ok=True)

                # 1. Hours_vs_Slope (SIEMPRE se genera)
                print("  -> Hours_vs_Slope_TrafficScale")
                run_hours_vs_slope(
                    datos_comp, datos_obs, red,
                    output_path=os.path.join(out_dir, f"Hours_vs_Slope_{red}_r{radio}s{steps}.png")
                )

                if not GENERAR_SOLO_HOURS_VS_SLOPE:
                    # 2. MedianSlopesVsPer95 (modelo óptimo de la red)
                    model = OPTIMAL_MODELS[red]
                    print(f"  -> MedianSlopesVsPer95 ({model['topology_index']})")
                    run_median_slopes_vs_per95(
                        datos_comp, datos_obs, red,
                        topology_index=model['topology_index'],
                        threshold=model['threshold'],
                        output_path=os.path.join(out_dir, f"MedianSlopesVsPer95_{red}_r{radio}s{steps}.png")
                    )

                    # 3. MedianSlopesVsR2
                    print(f"  -> MedianSlopesVsR2 (CC, DiCC)")
                    run_median_slopes_vs_r2(
                        datos_comp, datos_obs, red,
                        topology_names=['CC', 'DiCC'],
                        output_path=os.path.join(out_dir, f"MedianSlopesVsR2_{red}_r{radio}s{steps}.png")
                    )

                    # 4. ThreeSlopesVsPer95
                    print(f"  -> ThreeSlopesVsPer95 (BC, CC, DC)")
                    run_three_slopes_vs_per95(
                        datos_comp, datos_obs, red,
                        topology_indices=["BC", "CC", "DC"],
                        thresholds=THREE_SLOPES_THRESHOLDS[red],
                        output_path=os.path.join(out_dir, f"ThreeSlopesVsPer95_{red}_r{radio}s{steps}.png")
                    )

                    # 5. TrafficIntensityVsNetwork (DC)
                    print(f"  -> TrafficIntensityVsNetworkValuePlot (DC)")
                    run_traffic_vs_network(
                        datos_comp, datos_obs, red,
                        topology_name='DC',
                        output_dir=os.path.join(out_dir, f"TrafficVsNetwork_{red}_r{radio}s{steps}")
                    )

    elapsed = time.time() - start_time
    print(f"\n{'='*50}")
    if GENERAR_SOLO_HOURS_VS_SLOPE:
        print(f"Modo: SOLO Hours_vs_Slope")
    print(f"Completado: {count} combinaciones en {elapsed/60:.1f} min")
    print(f"Resultados en: results/combinaciones/")


if __name__ == "__main__":
    run_all()
