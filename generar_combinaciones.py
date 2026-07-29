"""
generar_combinaciones.py
Genera todos los CSVs de tráfico para N505 y N1207 con distintas combinaciones
de radio y steps. Ejecutar desde FinalVersion/ con el .venv activado.

Usa la versión nueva de ImageProcessor (src.image_analysis.extract_traffic)
que lee desde la serialización de la red vial.

Tiempo estimado: ~3-5 horas dependiendo del hardware.
"""

import time

from src.image_analysis.extract_traffic import ImageProcessor, TrafficConfig
from src.utils.paths import combinaciones_path, iter_redes, combinaciones_dir

# ------------------------------------------------------------------
# Configuración
# ------------------------------------------------------------------

COMBINACIONES = [
    (0, 2),   # r0s2
    (0, 5),   # r0s5
    (0, 9),   # r0s9
    (1, 2),   # r1s2  ← paper N1207
    (1, 5),   # r1s5  ← paper N505
    (1, 9),   # r1s9
    (2, 2),   # r2s2
    (2, 5),   # r2s5
    (2, 9),   # r2s9
    (3, 2),   # r3s2
    (3, 5),   # r3s5
    (3, 9),   # r3s9
]

# ------------------------------------------------------------------
# Log
# ------------------------------------------------------------------

LOG_FILE = combinaciones_dir() / 'progreso.log'

def log(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{timestamp}] {msg}"
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')

# ------------------------------------------------------------------
# Calcular total y verificar cuáles ya existen
# ------------------------------------------------------------------

redes = iter_redes()
total = len(redes) * len(COMBINACIONES)
completados = 0
saltados = 0

log(f"=== Inicio: {total} combinaciones a generar ===")
log(f"Usando nueva versión de ImageProcessor (serialización)")

# ------------------------------------------------------------------
# Loop principal
# ------------------------------------------------------------------

for red_nombre in redes:
    log(f"\n--- Red: {red_nombre} ---")

    processor = ImageProcessor(red_nombre)

    for radio, steps in COMBINACIONES:
        s_label = steps + 1  # steps=2 → S=3, steps=5 → S=6, etc.
        nombre = f"r{radio}s{s_label}"

        mean_path = combinaciones_path('mean', red_nombre, radio, steps)
        max_path = combinaciones_path('max', red_nombre, radio, steps)

        # Saltar si ya existe
        if mean_path.exists() and max_path.exists():
            log(f"  [SKIP] {red_nombre} {nombre} — ya existe")
            saltados += 1
            completados += 1
            continue

        log(f"  [START] {red_nombre} {nombre} (radio={radio}, steps={steps}, S={s_label})")
        t0 = time.time()

        try:
            config = TrafficConfig(radio=radio, steps=steps, weekdays_only=True)
            df_mean, df_max = processor.process_combination(config)

            mean_path.parent.mkdir(parents=True, exist_ok=True)
            df_mean.to_csv(mean_path, index=False)
            df_max.to_csv(max_path, index=False)

            elapsed = time.time() - t0
            completados += 1
            log(f"  [OK] {red_nombre} {nombre} — {df_mean.shape} — {elapsed/60:.1f} min")

        except Exception as e:
            log(f"  [ERROR] {red_nombre} {nombre} — {e}")

log(f"\n=== Fin: {completados}/{total} completados ({saltados} saltados) ===")
log(f"Archivos en: {combinaciones_dir()}/")
