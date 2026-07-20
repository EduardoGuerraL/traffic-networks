"""
generar_combinaciones.py
Genera todos los CSVs de tráfico para N505 y N1207 con distintas combinaciones
de radio y steps. Ejecutar desde FinalVersion/ con el .venv activado.

Tiempo estimado: ~3-5 horas dependiendo del hardware.
"""

import sys
import os
import time

sys.path.insert(0, 'src/image_analysis')
from GetDataFromImages import ImageProcessor

# ------------------------------------------------------------------
# Configuración
# ------------------------------------------------------------------

REDES = {
    'N505': {
        'screenshots':  'data/raw/Images/screenshotsGoogleMaps/screenshots',
        'network_data': 'data/network/dat_files/PuntaArenas',
    },
    'N1207': {
        'screenshots':  'data/raw/Images/screenshotsGoogleMaps/screenshots',
        'network_data': 'data/network/dat_files/PuntaArenasDetallado',
    },
}

COMBINACIONES = [
    (0, 2),   # r0s3
    (0, 5),   # r0s6
    (0, 9),   # r0s10
    (1, 2),   # r1s3  ← paper N1207
    (1, 5),   # r1s6  ← paper N505
    (1, 9),   # r1s10
    (2, 2),   # r2s3
    (2, 5),   # r2s6
    (2, 9),   # r2s10
    (3, 2),   # r3s3
    (3, 5),   # r3s6
    (3, 9),   # r3s10
]

OUTPUT_DIR = 'data/processed/combinaciones'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------
# Log
# ------------------------------------------------------------------

LOG_FILE = os.path.join(OUTPUT_DIR, 'progreso.log')

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

# ------------------------------------------------------------------
# Calcular total y verificar cuáles ya existen
# ------------------------------------------------------------------

total = len(REDES) * len(COMBINACIONES)
completados = 0
saltados = 0

log(f"=== Inicio: {total} combinaciones a generar ===")
log(f"Resultados en: {OUTPUT_DIR}/")

# ------------------------------------------------------------------
# Loop principal
# ------------------------------------------------------------------

for red_nombre, red_config in REDES.items():
    log(f"\n--- Red: {red_nombre} ---")

    processor = ImageProcessor(
        path_dir_screenshots  = red_config['screenshots'],
        path_dir_network_data = red_config['network_data'],
    )

    for radio, steps in COMBINACIONES:
        s_label = steps + 1  # steps=2 → S=3, steps=5 → S=6, etc.
        nombre = f"r{radio}s{s_label}"

        path_mean = os.path.join(OUTPUT_DIR, f"traffic_mean_{red_nombre}_{nombre}.csv")
        path_max  = os.path.join(OUTPUT_DIR, f"traffic_max_{red_nombre}_{nombre}.csv")

        # Saltar si ya existe
        if os.path.exists(path_mean) and os.path.exists(path_max):
            log(f"  [SKIP] {red_nombre} {nombre} — ya existe")
            saltados += 1
            completados += 1
            continue

        log(f"  [START] {red_nombre} {nombre} (radio={radio}, steps={steps}, S={s_label})")
        t0 = time.time()

        try:
            df_mean, df_max = processor.images_to_dataframe(steps=steps, radio=radio)
            df_mean.to_csv(path_mean, index=False)
            df_max.to_csv(path_max,   index=False)

            elapsed = time.time() - t0
            completados += 1
            log(f"  [OK] {red_nombre} {nombre} — {df_mean.shape} — {elapsed/60:.1f} min")

        except Exception as e:
            log(f"  [ERROR] {red_nombre} {nombre} — {e}")

log(f"\n=== Fin: {completados}/{total} completados ({saltados} saltados) ===")
log(f"Archivos en: {OUTPUT_DIR}/")
