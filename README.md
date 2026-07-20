# Traffic Network Analysis of Punta Arenas (2023)

> Predicting vehicular traffic intensity from the complex street-network topology of Punta Arenas, Chile, using Google Maps traffic imagery and complex-network metrics.

## Research Question

**Can complex-network metrics (centrality, connectivity, structure) predict the
vehicular traffic intensity observed on the streets of a city?**

This repository implements the full pipeline described in:

> E. Guerra, *How the traffic congestion is induced by the complex street network of the city*, SSRN. https://ssrn.com/abstract=XXXXXXXX

*(full link to be added)*

The study combines two complementary representations of the urban road network
with traffic data extracted directly from Google Maps images, and tests whether
the computational/structural properties of the network are correlated with, and
potentially predictive of, real traffic conditions.

---

## Overview

The project follows a five-stage pipeline:

1. **Capture** Google Maps traffic imagery for Punta Arenas over multiple time instants.
2. **Digitize** the road network manually into two graph models.
3. **Extract** a per-street traffic value (mean / max) from each image.
4. **Compute** network metrics (centrality, adjacency, random-walk dynamics).
5. **Visualize & correlate** network metrics against measured traffic intensity.

All stages are reproducible from the scripts in `src/` plus helper notebooks in
`notebooks/`.

---

## The Two Network Models

The road network is represented at two levels of detail:

| Model        | Nodes | Description                                                                 |
|--------------|-------|-----------------------------------------------------------------------------|
| **N505** (SimpleNet)  | 505   | Only intersections are nodes. Straight links between intersections.         |
| **N1207** (ComplexNet)| 1207  | Intersections **plus** intermediate nodes, capturing curved / non-straight streets. |

The richer N1207 model is required to obtain meaningful data for streets that
are not straight lines, while N505 provides the simpler intersection-only view.

---

## Methodology / Pipeline

### 1. Capture traffic images — `src/capture/`
Downloads Google Maps traffic screenshots for a bounding box of Punta Arenas
using Selenium (`screenshot_taker.py`, `map_generator.py`).

```bash
python -m src.capture.screenshot_taker   # adjust config in src/capture/config.py
```

### 2. Manual network digitization — `src/manual_network/NetworkCreator.py`
An interactive Pygame tool to draw nodes (intersections) and links (streets)
directly over a reference image. Outputs the `.dat` files:
`Posiciones.dat`, `Conexiones.dat`, `Carriles.dat`.

```bash
python -m src.manual_network.NetworkCreator
```
- Use **N** to create nodes, **L** to create links, **Ctrl+S** to save, **Ctrl+Z** to undo.
- Two networks are produced: `PuntaArenas` (N505) and `PuntaArenasDetallado` (N1207).

### 3. Traffic extraction — `src/image_analysis/GetDataFromImages.py`
Converts each traffic image into a numeric matrix (green/orange/red/dark-red →
traffic levels 64/128/191/255) and samples it along each street. For every
street it returns the **mean** and **max** traffic value, configurable by:

- `steps` — number of intermediate sample points between street endpoints.
- `radio` — sampling radius (in pixels) around each point.

```bash
python -m src.image_analysis.GetDataFromImages
# → data/processed/traffic_mean.csv, data/processed/traffic_max.csv
```

### 4. Batch combinations — `generar_combinaciones.py`
Runs the extraction for both networks across all combinations of
`radio ∈ {0,1,2,3}` and `steps ∈ {2,5,9}` (labelled `r*s*`, e.g. `r1s6`).
Already-computed combinations are skipped.

```bash
python generar_combinaciones.py
# → data/processed/combinaciones/traffic_{mean,max}_{N505,N1207}_r*s*.csv
# (estimated 3–5 h depending on hardware)
```

### 5. Network metrics — `src/network/GetDataFromNetwork.py`
Builds directed/undirected `networkx` graphs (nodes-as-intersections and
nodes-as-streets) and computes:

- Degree, closeness and betweenness centrality (BC/CC/DC) for directed & undirected graphs.
- Adjacency matrices (intersections & streets).
- Analytic random-walk probabilities and Ehrenfest-urn dynamics.

```bash
python -m src.network.GetDataFromNetwork
# → data/processed/DataNetwork/centrality_for_models/*.dat, adjacency matrices
```

### 6. Visualization & correlation — `src/visualization/` + `notebooks/`
Plots relating network metrics to traffic intensity, plus slope/percentile
analyses. The notebooks document results for a single configuration each:

| Notebook | Purpose |
|----------|---------|
| `01_CreacionRed.ipynb`        | Network creation walkthrough |
| `02_CapturaDatos.ipynb`       | Data capture walkthrough |
| `03_Procesamiento.ipynb`      | Image → traffic processing |
| `04_FigurasResultados.ipynb`  | Result figures |
| `05_ExploradorFigurasPaper.ipynb` | Paper figure explorer |

---

## Repository Structure

```
FinalVersion/
├── src/
│   ├── capture/            # Google Maps traffic image download (Selenium)
│   ├── manual_network/     # Interactive network digitizer (NetworkCreator.py)
│   ├── image_analysis/     # Traffic value extraction (GetDataFromImages.py)
│   ├── network/            # Network metrics (GetDataFromNetwork.py)
│   ├── visualization/      # Correlation & result plots
│   ├── utils/              # Shared helpers
│   └── run_capture.py
├── notebooks/             # 01–05 walkthrough notebooks + results/figures
├── data/
│   ├── raw/               # Reference images (NOT versioned)
│   ├── network/dat_files/ # Hand-built .dat networks (versioned)
│   └── processed/         # Traffic CSVs, centrality, combinations
├── results/               # Generated figures
├── generar_combinaciones.py
├── requirements.txt
└── README.md
```

---

## Installation

Requires Python 3.9+.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### ⚠️ API key — security note

`src/capture/config.py` currently contains a hard-coded Google Maps API key.
**Do not commit secrets.** Move it to an environment variable and read it from
the configuration instead:

```bash
export GOOGLE_MAPS_API_KEY="your_key_here"
```

Then update `src/capture/config.py` to use `os.environ["GOOGLE_MAPS_API_KEY"]`
before sharing the repository or publishing it.

---

## Data

- **Raw traffic images** (`data/raw/Images/...`): **not included** in the
  repository (too large). Request them separately and place them under
  `data/raw/Images/screenshotsGoogleMaps/screenshots/`.
- **Network `.dat` files** (`data/network/dat_files/`): versioned in the repo.
- **Processed outputs** (`data/processed/`, `results/`): generated by the pipeline.

---

## Usage / Reproduction

Run stages in order; each depends on the previous outputs:

```bash
# 1. Capture images (needs API key + Selenium driver)
python -m src.capture.screenshot_taker

# 2. Digitize network (interactive) → data/network/dat_files/
python -m src.manual_network.NetworkCreator

# 3. Extract traffic for all combinations
python generar_combinaciones.py

# 4. Compute network metrics
python -m src.network.GetDataFromNetwork

# 5. Explore / reproduce figures
jupyter notebook notebooks/04_FigurasResultados.ipynb
```

The notebooks are the recommended entry point for understanding the results of a
single configuration, while the scripts reproduce the full batch of combinations.

---

## Results / Outputs

- Traffic tables: `data/processed/traffic_{mean,max}*.csv`
- Centrality & coordinates: `data/processed/DataNetwork/`
- Adjacency matrices: `data/RepValdi/*_adjacency_matrix.txt`
- Figures: `results/`, `notebooks/results/figures/`

---

## Project Status

Functional end-to-end pipeline. The execution order is flexible: the scripts
regenerate all images and results, and the notebooks document the outcome for a
single network/configuration at a time.

---

## Acknowledgements

Traffic imagery courtesy of Google Maps. Road-network models digitized manually
for Punta Arenas (Chile, 2023).
