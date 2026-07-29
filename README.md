# Traffic Network Analysis of Punta Arenas (2023)

> Predicting vehicular traffic intensity from the complex street-network topology of Punta Arenas, Chile, using Google Maps traffic imagery and complex-network metrics.

## Research Question

**Can complex-network metrics (centrality, connectivity, structure) predict the
vehicular traffic intensity observed on the streets of a city?**

This repository implements the full pipeline described in:

> E. Guerra, *How the traffic congestion is induced by the complex street network of the city*, SSRN. https://ssrn.com/abstract=XXXXXXXX

---

## Overview

The project follows a five-stage pipeline:

1. **Capture** Google Maps traffic imagery for Punta Arenas over multiple time instants.
2. **Digitize** the road network manually into two graph models.
3. **Extract** a per-street traffic value (mean / max) from each image.
4. **Compute** network metrics (centrality, adjacency, random-walk dynamics).
5. **Correlate** network metrics against measured traffic intensity.

---

## The Two Network Models

| Model | Nodes | Description |
|-------|-------|-------------|
| **N505** (SimpleNet) | 505 | Only intersections are nodes. Straight links between intersections. |
| **N1207** (ComplexNet) | 1207 | Intersections **plus** intermediate nodes, capturing curved / non-straight streets. |

---

## Pipeline

### 1. Capture traffic images — `src/capture/`

Downloads Google Maps traffic screenshots using Selenium.

```bash
python -m src.capture.screenshot_taker
```

### 2. Manual network digitization — `src/manual_network/NetworkCreator.py`

Interactive Pygame tool to draw nodes and links over a reference image.

```bash
python -m src.manual_network.NetworkCreator
```

Outputs: `data/network/dat_files/{PuntaArenas,PuntaArenasDetallado}/`

### 3. Build and serialize network — `src/network/build_all_networks.py`

Reads `.dat` files, builds networkx graphs, computes centrality metrics, and serializes everything to `network_graphs.pkl`.

```bash
python -m src.network.build_all_networks
```

Outputs: `data/network/serialized/{N505,N1207}/`

### 4. Extract traffic from images — `src/image_analysis/extract_traffic.py`

Converts each traffic image into a numeric matrix (green/orange/red/dark-red → 64/128/191/255) and samples it along each street.

**Parameters:**
- `steps` — intermediate sample points between street endpoints (2, 5, 9)
- `radio` — sampling radius in pixels (0, 1, 2, 3)
- `weekdays_only` — filter to exclude weekends

```python
from src.image_analysis.extract_traffic import run_step5
run_step5(red='N505', radio=1, steps=5, weekdays_only=True)
```

### 5. Batch combinations — `generar_combinaciones.py`

Runs extraction for both networks across all 24 combinations (2 redes × 4 radios × 3 steps).

```bash
python generar_combinaciones.py
```

Outputs: `data/processed/combinaciones/traffic_{mean,max}_N{505,1207}_r{0-3}s{3,6,10}.csv`

**Note:** Each combination takes ~15-20 min. Full batch: ~6-8 hours.

### 6. Compute centrality — `src/network/compute_centrality.py`

Computes 6 centrality metrics on the streets graph:
- BC, DiBC (Betweenness)
- CC, DiCC (Closeness)
- DC, DiDC (Degree)

```bash
python -m src.network.compute_centrality
```

Outputs: `data/network/serialized/{N505,N1207}/centrality/indices_centralidad.csv`

### 7. Correlate traffic with centrality — `src/analysis/correlate.py`

```python
from src.analysis.correlate import correlate_with_aggregated
df = correlate_with_aggregated('N505', radio=1, steps=5, traffic_type='mean')
```

---

## Repository Structure

```
FinalVersion/
├── src/
│   ├── capture/              # Google Maps screenshot download
│   ├── manual_network/       # Interactive network digitizer
│   ├── image_analysis/       # Traffic extraction from images
│   │   ├── extract_traffic.py    # Main extraction module
│   │   └── aggregate_traffic.py  # Post-processing (stats_*)
│   ├── network/              # Network building and centrality
│   │   ├── build_all_networks.py # Build + serialize networks
│   │   ├── compute_centrality.py # Compute centrality metrics
│   │   └── load_network.py       # Load serialized networks
│   ├── analysis/             # Correlation and threshold analysis
│   │   ├── correlate.py      # Traffic-centrality correlation
│   │   ├── threshold.py      # Threshold sweep
│   │   └── sweep.py          # Full parameter sweep
│   ├── visualization/        # Result plots
│   └── utils/                # Shared helpers
│       ├── paths.py          # Centralized path resolution
│       └── basics.py         # Utility functions
├── data/
│   ├── raw/                  # Traffic screenshots (PNG)
│   ├── network/
│   │   ├── dat_files/        # Original .dat network files
│   │   └── serialized/       # Serialized networks + centrality
│   │       ├── N505/
│   │       │   ├── network_graphs.pkl
│   │       │   └── centrality/indices_centralidad.csv
│   │       └── N1207/
│   └── processed/
│       └── combinaciones/    # Traffic CSVs (mean/max + stats_*)
├── results/                  # Generated figures
├── config/pipeline.yaml      # Central configuration
├── generar_combinaciones.py  # Batch traffic extraction
├── requirements.txt
└── README.md
```

---

## Data Files

### Traffic CSVs (`data/processed/combinaciones/`)

| Pattern | Description | Rows | Columns |
|---------|-------------|------|---------|
| `traffic_mean_N*_r*s*.csv` | Mean traffic per street | 505/1207 | 2318 (3 + 2315 instants) |
| `traffic_max_N*_r*s*.csv` | Max traffic per street | 505/1207 | 2318 |
| `traffic_stats_*` | Statistical aggregations | 505/1207 | varies |

**Column naming:** `r{radio}s{steps+1}` (e.g., `r1s6` = radio=1, steps=5, S=6)

### Centrality CSVs (`data/network/serialized/*/centrality/`)

| Column | Description |
|--------|-------------|
| `Nodo` | Node ID |
| `Conections` | Tuple of connected nodes |
| `BC`, `DiBC` | Betweenness centrality (undirected/directed) |
| `CC`, `DiCC` | Closeness centrality (undirected/directed) |
| `DC`, `DiDC` | Degree centrality (undirected/directed) |

---

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .  # For package imports
```

---

## Configuration

All paths and parameters are centralized in `config/pipeline.yaml`:

```yaml
redes:
  N505:
    nodos: 505
    network_data: "data/network/dat_files/PuntaArenas"
  N1207:
    nodos: 1207
    network_data: "data/network/dat_files/PuntaArenasDetallado"

combinaciones:
  radios: [0, 1, 2, 3]
  steps: [2, 5, 9]

imagenes:
  dir: "data/raw"
  referencia: "CleanScreenshot.png"
  solo_dias_semana: true
```

---

## Key Functions

### `src/utils/paths.py`

```python
from src.utils.paths import centralidad_path, combinaciones_path, iter_redes

centralidad_path('N505')  # → .../serialized/N505/centrality/indices_centralidad.csv
combinaciones_path('mean', 'N505', 1, 5)  # → .../combinaciones/traffic_mean_N505_r1s6.csv
iter_redes()  # → ['N505', 'N1207']
```

### `src/analysis/correlate.py`

```python
from src.analysis.correlate import correlate_with_aggregated

# Correlate centrality with aggregated traffic
df = correlate_with_aggregated('N505', radio=1, steps=5, traffic_type='mean')

# Correlate specific centrality metric
df = correlate_stepwise('N505', 'DC', radio=1, steps=5)
```

---

## Project Status

- [x] Network serialization
- [x] Centrality computation (6 metrics × 2 networks)
- [x] Traffic extraction (24 combinations × 2 networks)
- [x] Weekday filtering
- [x] Basic correlation analysis
- [ ] Statistical aggregation (traffic_stats_*)
- [ ] Threshold optimization
- [ ] Full parameter sweep

---

## Acknowledgements

Traffic imagery courtesy of Google Maps. Road-network models digitized manually
for Punta Arenas (Chile, 2023).
