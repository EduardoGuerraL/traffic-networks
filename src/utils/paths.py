"""
Paths utility - Centralized path resolution from config/pipeline.yaml
Replaces RutasDeArchivos.py with typed, validated paths.
"""

from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple
import yaml


@dataclass(frozen=True)
class RedConfig:
    nombre: str
    nodos: int
    network_data: Path
    radio_optimo: int
    steps_optimo: int
    umbral_optimo: Dict[str, float]


@dataclass(frozen=True)
class PipelineConfig:
    proyecto: str
    redes: Dict[str, RedConfig]
    radios: List[int]
    steps: List[int]
    imagenes_dir: Path
    imagenes_referencia: str
    solo_dias_semana: bool
    topologia_indices: List[str]
    n_boxes_map: Dict[str, int]
    umbrales_n_puntos: int
    umbrales_rango_factor: float
    combinaciones_dir: Path
    traffic_stats_dir: Path
    centralidad_dir: Path
    resultados_dir: Path
    figures_dir: Path
    sweep_csv: Path
    traffic_values: Dict[str, int]
    traffic_max: int


def load_config(config_path: Path | None = None) -> PipelineConfig:
    """Load and parse pipeline.yaml into typed config."""
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "pipeline.yaml"

    with open(config_path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    # Resolve project root
    root = config_path.parent.parent

    # Parse redes
    redes = {}
    for key, val in raw["redes"].items():
        redes[key] = RedConfig(
            nombre=val["nombre"],
            nodos=val["nodos"],
            network_data=root / val["network_data"],
            radio_optimo=val["radio_optimo"],
            steps_optimo=val["steps_optimo"],
            umbral_optimo=val.get("umbral_optimo", {}),
        )

    return PipelineConfig(
        proyecto=raw["proyecto"]["nombre"],
        redes=redes,
        radios=raw["combinaciones"]["radios"],
        steps=raw["combinaciones"]["steps"],
        imagenes_dir=root / raw["imagenes"]["dir"],
        imagenes_referencia=raw["imagenes"]["referencia"],
        solo_dias_semana=raw["imagenes"]["solo_dias_semana"],
        topologia_indices=raw["topologia"]["indices"],
        n_boxes_map=raw["topologia"]["n_boxes_map"],
        umbrales_n_puntos=raw["umbrales"]["n_puntos"],
        umbrales_rango_factor=raw["umbrales"]["rango_factor"],
        combinaciones_dir=root / raw["output"]["combinaciones_dir"],
        traffic_stats_dir=root / raw["output"].get("traffic_stats_dir", "data/processed/traffic_stats"),
        centralidad_dir=root / raw["output"]["centralidad_dir"],
        resultados_dir=root / raw["output"]["resultados_dir"],
        figures_dir=root / raw["output"]["figures_dir"],
        sweep_csv=root / raw["output"]["sweep_csv"],
        traffic_values=raw["traffic_values"],
        traffic_max=raw["traffic_values"]["max_value"],
    )


# Global config instance (loaded once)
_CONFIG: PipelineConfig | None = None


def get_config() -> PipelineConfig:
    """Get singleton config instance."""
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = load_config()
    return _CONFIG


# --- Path builders ---

def network_data_path(red: str) -> Path:
    """Path to network .dat files (Posiciones.dat, Conexiones.dat, Carriles.dat)."""
    return get_config().redes[red].network_data


def combinaciones_path(tipo: str, red: str, radio: int, steps: int) -> Path:
    """
    Path to traffic combination CSV.
    tipo: 'mean' or 'max'
    steps: internal steps (2, 5, 9) -> label S = steps + 1 (3, 6, 10)
    """
    s_label = steps + 1
    cfg = get_config()
    return cfg.combinaciones_dir / f"traffic_{tipo}_{red}_r{radio}s{s_label}.csv"


def centralidad_path(red: str) -> Path:
    """Path to serialized network centrality CSV (indices_centralidad.csv)."""
    root = Path(__file__).parent.parent.parent
    return root / "data" / "network" / "serialized" / red / "centrality" / "indices_centralidad.csv"


def sweep_csv_path() -> Path:
    return get_config().sweep_csv


def figure_path(name: str) -> Path:
    return get_config().figures_dir / name


def results_dir() -> Path:
    return get_config().resultados_dir


def combinaciones_dir() -> Path:
    return get_config().combinaciones_dir


def traffic_stats_dir() -> Path:
    return get_config().traffic_stats_dir


# --- Helper lists for iteration ---

def iter_redes() -> List[str]:
    return list(get_config().redes.keys())


def iter_radios() -> List[int]:
    return get_config().radios


def iter_steps() -> List[int]:
    return get_config().steps


def iter_topologia() -> List[str]:
    return get_config().topologia_indices


def n_boxes_for(index: str) -> int:
    return get_config().n_boxes_map.get(index, 20)


def umbral_optimo_para(red: str, topologia: str) -> float | None:
    """Get optimal threshold from config if defined."""
    return get_config().redes[red].umbral_optimo.get(topologia)


# --- Validation ---

def validate_paths() -> List[str]:
    """Check that critical input paths exist. Returns list of missing paths."""
    cfg = get_config()
    missing = []

    for red_name, red in cfg.redes.items():
        for f in ["Posiciones.dat", "Conexiones.dat", "Carriles.dat"]:
            p = red.network_data / f
            if not p.exists():
                missing.append(str(p))

    if not cfg.imagenes_dir.exists():
        missing.append(str(cfg.imagenes_dir))

    ref = cfg.imagenes_dir / cfg.imagenes_referencia
    if not ref.exists():
        missing.append(str(ref))

    return missing


if __name__ == "__main__":
    # Quick test
    cfg = load_config()
    print(f"Proyecto: {cfg.proyecto}")
    print(f"Redes: {list(cfg.redes.keys())}")
    print(f"Radios: {cfg.radios}")
    print(f"Steps: {cfg.steps}")
    print(f"Topología: {cfg.topologia_indices}")
    print(f"Combinaciones dir: {cfg.combinaciones_dir}")

    # Test path builders
    print(f"\nN505 network_data: {network_data_path('N505')}")
    print(f"N505 r1s5 mean: {combinaciones_path('mean', 'N505', 1, 5)}")
    print(f"N505 centralidad: {centralidad_path('N505')}")
    print(f"N1207 centralidad: {centralidad_path('N1207')}")

    missing = validate_paths()
    if missing:
        print(f"\n⚠️ Missing paths: {missing}")
    else:
        print("\n✅ All critical paths exist")
