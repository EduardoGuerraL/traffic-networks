"""
Paso 5: Extracción de tráfico de imágenes.
Procesa imágenes de Google Maps y genera CSVs por calle × instante.
"""

from __future__ import annotations
from pathlib import Path
import os
import math
import numpy as np
import cv2
import pandas as pd
from statistics import mean
from dataclasses import dataclass

from src.utils.paths import (
    get_config,
    combinaciones_path,
    iter_redes,
    iter_radios,
    iter_steps,
    network_data_path,
)
from src.utils.basics import obtener_nombres_con_H_M_sinFDS


# Colores de tráfico de Google Maps (en RGB)
RED_COLORS = [
    '#f23c32', '#f3493f', '#f56159', '#f4554c', '#f66e66',
    '#f77a73', '#f88680', '#f9928d', '#faaba6'
]
DARK_RED_COLORS = [
    '#811f1f', '#892d2d', '#994949', '#913b3b',
    '#b17373', '#c18f8f', '#d1abab'
]

# Valores numéricos asignados a cada nivel de tráfico
TRAFFIC_VALUES = {
    'green':    64,
    'orange':  128,
    'red':     191,
    'dark_red': 255,
    'no_data':   0,
}


@dataclass
class TrafficConfig:
    radio: int
    steps: int
    weekdays_only: bool = True


class ImageProcessor:
    """Procesa imágenes de tráfico y extrae valores por calle."""
    
    def __init__(self, red: str):
        self.red = red
        cfg = get_config()
        
        # Directorio de screenshots
        self.screenshots_dir = cfg.imagenes_dir
        
        # Imagen de referencia para dimensiones
        ref_path = self.screenshots_dir / cfg.imagenes_referencia
        ref_image = cv2.imread(str(ref_path))
        if ref_image is None:
            raise FileNotFoundError(f"Referencia no encontrada: {ref_path}")
        self.img_h, self.img_w = ref_image.shape[:2]
        
        # Cargar red vial
        net_dir = network_data_path(red)
        raw_positions = eval(open(net_dir / "Posiciones.dat").readline())
        self.position_of_vertices = {
            i: [t[0] * self.img_w, t[1] * self.img_h]
            for i, t in enumerate(raw_positions)
        }
        self.connections = eval(open(net_dir / "Conexiones.dat").readline())
        self.lanes = eval(open(net_dir / "Carriles.dat").readline())
        
        # Pre-computar colores
        self._red_rgb = np.array([self._hex_to_rgb(c) for c in RED_COLORS])
        self._dark_red_rgb = np.array([self._hex_to_rgb(c) for c in DARK_RED_COLORS])
        
        # Cache de coordenadas intermedias
        self._coords_cache: dict[int, list] = {}
        
        # Columnas de tiempo (nombres de archivos PNG)
        png_files = sorted([f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')])
        self.all_time_columns = [os.path.splitext(f)[0] for f in png_files]
        
        if cfg.solo_dias_semana:
            self.time_columns = obtener_nombres_con_H_M_sinFDS(self.all_time_columns)
        else:
            self.time_columns = self.all_time_columns
        
        print(f"  {red}: {len(self.connections)} calles, {len(self.time_columns)} instantes")
    
    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        h = hex_color.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    def _get_intermediate_coords(self, steps: int) -> list:
        """Cache coordenadas intermedias para dado steps."""
        if steps not in self._coords_cache:
            self._coords_cache[steps] = [
                self._intermediate_coords(
                    list(self.position_of_vertices[c[0]]),
                    list(self.position_of_vertices[c[1]]),
                    steps
                )
                for c in self.connections
            ]
        return self._coords_cache[steps]
    
    @staticmethod
    def _intermediate_coords(coord1: list, coord2: list, steps: int) -> list:
        """Puntos intermedios entre dos coordenadas (en píxeles)."""
        c1 = [round(coord1[0]), round(coord1[1])]
        c2 = [round(coord2[0]), round(coord2[1])]
        dx = (c2[0] - c1[0]) / (steps + 1)
        dy = (c2[1] - c1[1]) / (steps + 1)
        points = [
            (int(c1[0] + i * dx), int(c1[1] + i * dy))
            for i in range(steps + 1)
        ]
        points.append((c2[0], c2[1]))
        return points
    
    def _image_to_traffic_matrix(self, image: np.ndarray) -> np.ndarray:
        """Convierte imagen BGR a matriz de valores de tráfico (0-255)."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        mask_green = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
        mask_orange = cv2.inRange(hsv, np.array([10, 100, 100]), np.array([25, 255, 255]))
        mask_red = self._color_mask(rgb, self._red_rgb)
        mask_dark_red = self._color_mask(rgb, self._dark_red_rgb)
        
        matrix = np.zeros(image.shape[:2], dtype=np.uint8)
        matrix[mask_green > 0] = TRAFFIC_VALUES['green']
        matrix[mask_orange > 0] = TRAFFIC_VALUES['orange']
        matrix[mask_red > 0] = TRAFFIC_VALUES['red']
        matrix[mask_dark_red > 0] = TRAFFIC_VALUES['dark_red']
        return matrix
    
    @staticmethod
    def _color_mask(rgb_image: np.ndarray, color_list: np.ndarray) -> np.ndarray:
        mask = np.zeros(rgb_image.shape[:2], dtype=bool)
        for color in color_list:
            mask |= np.all(rgb_image == color, axis=-1)
        return mask.astype(np.uint8)
    
    def _sample_matrix(self, matrix: np.ndarray, coords: list, radio: int) -> list:
        """Extrae valores de la matriz en coordenadas dadas (con radio)."""
        h, w = matrix.shape
        values = []
        for (col, row) in coords:
            for di in range(-radio, radio + 1):
                for dj in range(-radio, radio + 1):
                    r, c = row + di, col + dj
                    if 0 <= r < h and 0 <= c < w:
                        v = matrix[r, c]
                        if v != 0:
                            values.append(int(v))
        return values if values else [0]
    
    def _street_length(self, connection: tuple) -> float:
        x1, y1 = self.position_of_vertices[connection[0]]
        x2, y2 = self.position_of_vertices[connection[1]]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def process_combination(self, config: TrafficConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Procesa todas las imágenes para una configuración y devuelve (df_mean, df_max)."""
        steps = config.steps
        radio = config.radio
        
        # Base DataFrame con info de calles
        base = pd.DataFrame({
            'connection': self.connections,
            'lanes': self.lanes,
            'length': [self._street_length(c) for c in self.connections],
        })
        
        # Coordenadas intermedias por calle
        coords_per_street = self._get_intermediate_coords(steps)
        
        cols_mean = {}
        cols_max = {}
        
        png_files = sorted([f for f in os.listdir(self.screenshots_dir) if f.endswith('.png')])
        
        for filename in png_files:
            key = os.path.splitext(filename)[0]
            if key not in self.time_columns:
                continue
            
            path = os.path.join(self.screenshots_dir, filename)
            image = cv2.imread(path)
            if image is None:
                continue
            
            traffic_matrix = self._image_to_traffic_matrix(image)
            
            street_means = []
            street_maxes = []
            for coords in coords_per_street:
                values = self._sample_matrix(traffic_matrix, coords, radio)
                street_means.append(mean(values))
                street_maxes.append(max(values))
            
            cols_mean[key] = street_means
            cols_max[key] = street_maxes
        
        df_mean = pd.concat([base, pd.DataFrame(cols_mean)], axis=1)
        df_max = pd.concat([base, pd.DataFrame(cols_max)], axis=1)
        return df_mean, df_max
    
    def save_combination(self, config: TrafficConfig) -> tuple[Path, Path]:
        """Procesa y guarda CSVs para una combinación."""
        df_mean, df_max = self.process_combination(config)
        
        mean_path = combinaciones_path('mean', self.red, config.radio, config.steps)
        max_path = combinaciones_path('max', self.red, config.radio, config.steps)
        
        mean_path.parent.mkdir(parents=True, exist_ok=True)
        df_mean.to_csv(mean_path, index=False)
        df_max.to_csv(max_path, index=False)
        
        return mean_path, max_path


def run_step5(
    red: str | None = None,
    radio: int | None = None,
    steps: int | None = None,
    weekdays_only: bool = True,
    force: bool = False
):
    """
    Entry point para Paso 5.
    
    Args:
        red: 'N505' o 'N1207' (None = ambas)
        radio: 0-3 (None = todos)
        steps: 2, 5, 9 (None = todos)
        weekdays_only: filtrar solo días laborables
        force: re-procesar aunque exista
    """
    redes = [red] if red else iter_redes()
    radios = [radio] if radio is not None else iter_radios()
    steps_list = [steps] if steps is not None else iter_steps()
    
    for r in redes:
        print(f"\n=== Red: {r} ===")
        processor = ImageProcessor(r)
        
        for rad in radios:
            for st in steps_list:
                config = TrafficConfig(radio=rad, steps=st, weekdays_only=weekdays_only)
                
                mean_path = combinaciones_path('mean', r, rad, st)
                max_path = combinaciones_path('max', r, rad, st)
                
                if not force and mean_path.exists() and max_path.exists():
                    print(f"  [SKIP] r{rad}s{st+1} ya existe")
                    continue
                
                print(f"  [PROCESS] r{rad}s{st+1}...", end=" ", flush=True)
                try:
                    processor.save_combination(config)
                    print("OK")
                except Exception as e:
                    print(f"ERROR: {e}")


if __name__ == "__main__":
    run_step5()