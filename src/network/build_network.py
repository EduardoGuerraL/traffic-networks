"""
NetworkBuilder: Construye grafos de red desde archivos .dat y los serializa.

Uso:
    builder = NetworkBuilder("data/network/dat_files/PuntaArenas", "data/raw/...")
    builder.build()
    builder.save("data/network/serialized/N505")
"""

from __future__ import annotations

import json
import math
import os
import pickle
from pathlib import Path
from typing import Any

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


class NetworkBuilder:
    """
    Construye los 4 grafos de una red vial (DG/UG × inter/streets)
    a partir de los archivos generados por NetworkCreator.

    Archivos esperados en network_data_dir:
        - Posiciones.dat   → posiciones fraccionales de intersecciones
        - Conexiones.dat   → pares de intersecciones conectadas
        - Carriles.dat     → número de carriles por enlace
    """

    DAT_FILE_NAMES = {
        "positions": "Posiciones.dat",
        "connections": "Conexiones.dat",
        "lanes": "Carriles.dat",
    }

    def __init__(self, network_data_dir: str | Path, image_path: str | Path):
        """
        Args:
            network_data_dir: Directorio con Posiciones.dat, Conexiones.dat, Carriles.dat.
            image_path: Ruta a la imagen de referencia (para dimensiones y visualización).
        """
        self.network_data_dir = Path(network_data_dir)
        self.image_path = Path(image_path)

        # Resultados (se llenan con build())
        self._fraction_pos_intersections: list[tuple[float, float]] | None = None
        self._inter_conections: list[tuple[int, int]] | None = None
        self._street_lanes: list[int] | None = None
        self._pos_intersections: dict[int, list[int]] | None = None
        self._conection_btw_streets: list[tuple[int, int]] | None = None
        self._streets_coordinates: dict[int, tuple[list[int], list[int]]] | None = None
        self._image_shape: tuple[int, ...] | None = None

        self._DG_inter: nx.DiGraph | None = None
        self._UG_inter: nx.Graph | None = None
        self._DG_streets: nx.DiGraph | None = None
        self._UG_streets: nx.Graph | None = None

        self._built = False

    # ------------------------------------------------------------------
    # Propiedades de solo lectura (solo disponibles después de build())
    # ------------------------------------------------------------------

    @property
    def DG_inter(self) -> nx.DiGraph:
        self._ensure_built()
        return self._DG_inter

    @property
    def UG_inter(self) -> nx.Graph:
        self._ensure_built()
        return self._UG_inter

    @property
    def DG_streets(self) -> nx.DiGraph:
        self._ensure_built()
        return self._DG_streets

    @property
    def UG_streets(self) -> nx.Graph:
        self._ensure_built()
        return self._UG_streets

    @property
    def pos_intersections(self) -> dict[int, list[int]]:
        self._ensure_built()
        return self._pos_intersections

    @property
    def inter_conections(self) -> list[tuple[int, int]]:
        self._ensure_built()
        return self._inter_conections

    @property
    def street_lanes(self) -> list[int]:
        self._ensure_built()
        return self._street_lanes

    @property
    def streets_coordinates(self) -> dict[int, tuple[list[int], list[int]]]:
        self._ensure_built()
        return self._streets_coordinates

    @property
    def image_shape(self) -> tuple[int, ...]:
        self._ensure_built()
        return self._image_shape

    @property
    def num_streets(self) -> int:
        """Número de calles (= nodos en la representación streets-as-nodes)."""
        self._ensure_built()
        return len(self._DG_streets.nodes())

    @property
    def num_intersections(self) -> int:
        """Número de intersecciones (= nodos en la representación intersections-as-nodes)."""
        self._ensure_built()
        return len(self._DG_inter.nodes())

    # ------------------------------------------------------------------
    # Construcción
    # ------------------------------------------------------------------

    def build(self) -> NetworkBuilder:
        """
        Ejecuta el proceso completo de construcción de la red:
        1. Lee archivos .dat
        2. Redimensiona posiciones a coordenadas de imagen
        3. Calcula conexiones entre calles
        4. Calcula coordenadas de calles
        5. Crea los 4 grafos NetworkX

        Returns:
            self (para chaining: builder.build().save(...))
        """
        self._load_dat_files()
        self._compute_pixel_positions()
        self._compute_street_connections()
        self._compute_street_coordinates()
        self._build_graphs()
        self._built = True
        return self

    def _ensure_built(self):
        if not self._built:
            raise RuntimeError(
                "Network not built yet. Call builder.build() before accessing results."
            )

    def _load_dat_files(self):
        """Lee los 3 archivos .dat generados por NetworkCreator."""
        positions_path = self.network_data_dir / self.DAT_FILE_NAMES["positions"]
        connections_path = self.network_data_dir / self.DAT_FILE_NAMES["connections"]
        lanes_path = self.network_data_dir / self.DAT_FILE_NAMES["lanes"]

        for p in [positions_path, connections_path, lanes_path]:
            if not p.exists():
                raise FileNotFoundError(f"Expected dat file not found: {p}")

        self._fraction_pos_intersections = eval(
            open(positions_path, "r").readline()
        )
        self._inter_conections = eval(
            open(connections_path, "r").readline()
        )
        self._street_lanes = eval(
            open(lanes_path, "r").readline()
        )

    def _compute_pixel_positions(self):
        """Convierte posiciones fraccionales (0-1) a coordenadas de píxel de imagen."""
        img = plt.imread(str(self.image_path))
        self._image_shape = img.shape

        img_h, img_w = img.shape[0], img.shape[1]
        self._pos_intersections = {}
        for i, frac_tuple in enumerate(self._fraction_pos_intersections):
            self._pos_intersections[i] = [
                int(frac_tuple[0] * img_w),
                int(frac_tuple[1] * img_h),
            ]

    def _compute_street_connections(self):
        """
        Calcula las conexiones entre calles usando la representación
        'streets-as-nodes': dos calles están conectadas si el endpoint
        de una coincide con el startpoint de otra.
        """
        streets = dict(enumerate(self._inter_conections))
        connections = []
        for i in range(len(streets)):
            for j in range(len(streets)):
                if streets[i][1] == streets[j][0] and j != i:
                    connections.append((i, j))
        self._conection_btw_streets = connections

    def _compute_street_coordinates(self):
        """Calcula las coordenadas de pixel para cada calle (par de intersecciones)."""
        streets = dict(enumerate(self._inter_conections))
        self._streets_coordinates = {}
        for street_id, (inter_i, inter_f) in streets.items():
            self._streets_coordinates[street_id] = (
                self._pos_intersections[inter_i],
                self._pos_intersections[inter_f],
            )

    def _build_graphs(self):
        """Construye los 4 grafos NetworkX."""
        self._DG_inter = nx.DiGraph(self._inter_conections)
        self._UG_inter = nx.Graph(self._inter_conections)
        self._DG_streets = nx.DiGraph(self._conection_btw_streets)
        self._UG_streets = nx.Graph(self._conection_btw_streets)

    # ------------------------------------------------------------------
    # Serialización
    # ------------------------------------------------------------------

    def save(self, output_dir: str | Path) -> tuple[Path, Path]:
        """
        Serializa los grafos y metadatos en el directorio de salida.

        Crea:
            - network_graphs.pkl: los 4 grafos NetworkX (pickle)
            - network_metadata.json: posiciones, conexiones, carriles,
              coordenadas de calles, dimensiones de imagen

        Args:
            output_dir: Directorio donde se guardan los archivos.

        Returns:
            Tupla (ruta_grafos_pkl, ruta_metadata_json)
        """
        self._ensure_built()
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # --- Serializar grafos con pickle ---
        graphs_path = output_dir / "network_graphs.pkl"
        graphs_data = {
            "DG_inter": self._DG_inter,
            "UG_inter": self._UG_inter,
            "DG_streets": self._DG_streets,
            "UG_streets": self._UG_streets,
        }
        with open(graphs_path, "wb") as f:
            pickle.dump(graphs_data, f, protocol=pickle.HIGHEST_PROTOCOL)

        # --- Serializar metadatos con JSON ---
        metadata_path = output_dir / "network_metadata.json"
        metadata = {
            "source_files": {
                "positions": str(self.network_data_dir / self.DAT_FILE_NAMES["positions"]),
                "connections": str(self.network_data_dir / self.DAT_FILE_NAMES["connections"]),
                "lanes": str(self.network_data_dir / self.DAT_FILE_NAMES["lanes"]),
            },
            "image_path": str(self.image_path),
            "image_shape": list(self._image_shape),
            "num_intersections": self.num_intersections,
            "num_streets": self.num_streets,
            "inter_conections": [list(c) for c in self._inter_conections],
            "street_lanes": list(self._street_lanes),
            "fraction_pos_intersections": [list(p) for p in self._fraction_pos_intersections],
            "pos_intersections": {str(k): v for k, v in self._pos_intersections.items()},
            "streets_coordinates": {
                str(k): [list(v[0]), list(v[1])]
                for k, v in self._streets_coordinates.items()
            },
        }
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return graphs_path, metadata_path
