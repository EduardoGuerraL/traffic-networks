"""
NetworkGraphLoader: Carga grafos de red serializados + metadatos.

Uso:
    loader = NetworkGraphLoader.load("data/network/serialized/N505")
    print(loader.num_streets, loader.DG_streets)
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path

import networkx as nx


class NetworkGraphLoader:
    """
    Carga grafos de red ya serializados por NetworkBuilder.

    Lee:
        - network_graphs.pkl  → 4 grafos NetworkX (DG/UG × inter/streets)
        - network_metadata.json → posiciones, conexiones, carriles, etc.
    """

    GRAPH_FILE = "network_graphs.pkl"
    METADATA_FILE = "network_metadata.json"

    def __init__(
        self,
        DG_inter: nx.DiGraph,
        UG_inter: nx.Graph,
        DG_streets: nx.DiGraph,
        UG_streets: nx.Graph,
        metadata: dict,
    ):
        self._DG_inter = DG_inter
        self._UG_inter = UG_inter
        self._DG_streets = DG_streets
        self._UG_streets = UG_streets
        self._metadata = metadata

    # ------------------------------------------------------------------
    # Fábrica: desde archivo serializado
    # ------------------------------------------------------------------

    @classmethod
    def load(cls, network_dir: str | Path) -> NetworkGraphLoader:
        """
        Carga grafos + metadatos desde un directorio serializado.

        Args:
            network_dir: Directorio con network_graphs.pkl y network_metadata.json.

        Returns:
            Instancia de NetworkGraphLoader lista para usar.
        """
        network_dir = Path(network_dir)
        graphs_path = network_dir / cls.GRAPH_FILE
        metadata_path = network_dir / cls.METADATA_FILE

        if not graphs_path.exists():
            raise FileNotFoundError(f"Grafo serializado no encontrado: {graphs_path}")
        if not metadata_path.exists():
            raise FileNotFoundError(f"Metadata no encontrada: {metadata_path}")

        with open(graphs_path, "rb") as f:
            graphs = pickle.load(f)

        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        return cls(
            DG_inter=graphs["DG_inter"],
            UG_inter=graphs["UG_inter"],
            DG_streets=graphs["DG_streets"],
            UG_streets=graphs["UG_streets"],
            metadata=metadata,
        )

    # ------------------------------------------------------------------
    # Propiedades: grafos
    # ------------------------------------------------------------------

    @property
    def DG_inter(self) -> nx.DiGraph:
        """Intersecciones como nodos, dirigido."""
        return self._DG_inter

    @property
    def UG_inter(self) -> nx.Graph:
        """Intersecciones como nodos, no dirigido."""
        return self._UG_inter

    @property
    def DG_streets(self) -> nx.DiGraph:
        """Calles como nodos, dirigido."""
        return self._DG_streets

    @property
    def UG_streets(self) -> nx.Graph:
        """Calles como nodos, no dirigido."""
        return self._UG_streets

    # ------------------------------------------------------------------
    # Propiedades: metadatos
    # ------------------------------------------------------------------

    @property
    def num_intersections(self) -> int:
        return self._metadata["num_intersections"]

    @property
    def num_streets(self) -> int:
        return self._metadata["num_streets"]

    @property
    def image_shape(self) -> list[int]:
        return self._metadata["image_shape"]

    @property
    def image_path(self) -> str:
        return self._metadata["image_path"]

    @property
    def inter_conections(self) -> list[list[int]]:
        """Conexiones originales entre intersecciones: [[0, 3], [3, 6], ...]."""
        return self._metadata["inter_conections"]

    @property
    def street_lanes(self) -> list[int]:
        """Número de carriles por calle."""
        return self._metadata["street_lanes"]

    @property
    def fraction_pos_intersections(self) -> list[list[float]]:
        """Posiciones fraccionales (0-1) de cada intersección."""
        return self._metadata["fraction_pos_intersections"]

    @property
    def pos_intersections(self) -> dict[int, list[int]]:
        """Posiciones en píxeles de cada intersección: {0: [x, y], ...}."""
        return {int(k): v for k, v in self._metadata["pos_intersections"].items()}

    @property
    def streets_coordinates(self) -> dict[int, tuple[list[int], list[int]]]:
        """Coordenadas de cada calle (par de intersecciones): {0: ([x1,y1],[x2,y2]), ...}."""
        return {
            int(k): (v[0], v[1])
            for k, v in self._metadata["streets_coordinates"].items()
        }

    @property
    def source_files(self) -> dict[str, str]:
        """Rutas a los archivos .dat originales."""
        return self._metadata["source_files"]

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """Retorna un resumen textual de la red cargada."""
        return (
            f"NetworkGraphLoader:\n"
            f"  Intersecciones (nodos): {self.num_intersections}\n"
            f"  Calles (nodos):         {self.num_streets}\n"
            f"  DG_inter aristas:       {self._DG_inter.number_of_edges()}\n"
            f"  DG_streets aristas:     {self._DG_streets.number_of_edges()}\n"
            f"  Imagen:                 {self.image_path} ({self.image_shape})"
        )

    def __repr__(self) -> str:
        return (
            f"NetworkGraphLoader("
            f"intersections={self.num_intersections}, "
            f"streets={self.num_streets})"
        )
