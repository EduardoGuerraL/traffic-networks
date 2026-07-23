import os
import math
import numpy as np
import cv2
import pandas as pd
from statistics import mean


class ImageProcessor:
    """
    Procesa imágenes de tráfico de Google Maps y extrae valores por calle.

    Reemplaza el flujo anterior que generaba un HDF5 de ~1.8 GB cargando
    todas las imágenes en memoria. Esta versión procesa una imagen a la vez.
    """

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
        'green':    64,   # Fluido
        'orange':  128,   # Moderado
        'red':     191,   # Lento
        'dark_red': 255,  # Muy lento
        'no_data':   0,   # Sin datos
    }

    def __init__(self, path_dir_screenshots: str, path_dir_network_data: str):
        """
        Args:
            path_dir_screenshots:   Carpeta con las imágenes PNG de Google Maps.
            path_dir_network_data:  Carpeta con Posiciones.dat, Conexiones.dat y Carriles.dat.
        """
        self.path_dir_screenshots = path_dir_screenshots

        # Imagen de referencia (sin tráfico) para obtener dimensiones
        ref_path = os.path.join(path_dir_screenshots, "2023-03-29_07-30.png")
        ref_image = cv2.imread(ref_path)
        if ref_image is None:
            raise FileNotFoundError(f"No se encontró la imagen de referencia: {ref_path}")
        h, w = ref_image.shape[:2]

        # Cargar red vial
        raw_positions = eval(open(os.path.join(path_dir_network_data, "Posiciones.dat")).readline())
        self.position_of_vertices = {
            i: [tupla[0] * w, tupla[1] * h]
            for i, tupla in enumerate(raw_positions)
        }
        self.connections = eval(open(os.path.join(path_dir_network_data, "Conexiones.dat")).readline())
        self.lanes       = eval(open(os.path.join(path_dir_network_data, "Carriles.dat")).readline())

        # Pre-computar colores como arrays numpy (una sola vez)
        self._red_rgb      = np.array([self._hex_to_rgb(c) for c in self.RED_COLORS])
        self._dark_red_rgb = np.array([self._hex_to_rgb(c) for c in self.DARK_RED_COLORS])

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def images_to_dataframe(self, steps: int = 1, radio: int = 0) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Procesa todas las imágenes PNG de la carpeta y devuelve dos DataFrames:
            - df_mean : valor medio de tráfico por calle y por instante.
            - df_max  : valor máximo de tráfico por calle y por instante.

        Cada fila es una calle (conexión), cada columna es un instante de tiempo
        con nombre igual al nombre del archivo PNG sin extensión (e.g. '2023-03-29_07-30').

        Args:
            steps : puntos intermedios a muestrear entre los extremos de cada calle.
            radio : radio (en píxeles) alrededor de cada punto muestreado.

        Returns:
            (df_mean, df_max)
        """
        # Estructura base del DataFrame
        base = pd.DataFrame({
            'connection': self.connections,
            'lanes':      self.lanes,
            'length':     [self._street_length(c) for c in self.connections],
        })

        # Coordenadas intermedias por calle (calculadas una sola vez)
        coords_per_street = [
            self._intermediate_coords(
                list(self.position_of_vertices[c[0]]),
                list(self.position_of_vertices[c[1]]),
                steps
            )
            for c in self.connections
        ]

        cols_mean = {}
        cols_max  = {}

        png_files = sorted([f for f in os.listdir(self.path_dir_screenshots) if f.endswith('.png')])
        total = len(png_files)

        for idx, filename in enumerate(png_files):
            path = os.path.join(self.path_dir_screenshots, filename)
            image = cv2.imread(path)
            if image is None:
                print(f"  [!] No se pudo leer: {filename}")
                continue

            # Imagen → matriz de tráfico (una sola vez por imagen)
            traffic_matrix = self._image_to_traffic_matrix(image)

            street_means = []
            street_maxes = []
            for coords in coords_per_street:
                values = self._sample_matrix(traffic_matrix, coords, radio)
                street_means.append(mean(values))
                street_maxes.append(max(values))

            key = os.path.splitext(filename)[0]  # '2023-03-29_07-30'
            cols_mean[key] = street_means
            cols_max[key]  = street_maxes

            print(f"  Procesando {idx + 1}/{total}: {filename}")

        df_mean = pd.concat([base, pd.DataFrame(cols_mean)], axis=1)
        df_max  = pd.concat([base, pd.DataFrame(cols_max)],  axis=1)
        return df_mean, df_max

    # ------------------------------------------------------------------
    # Métodos internos
    # ------------------------------------------------------------------

    def _image_to_traffic_matrix(self, image: np.ndarray) -> np.ndarray:
        """Convierte una imagen BGR en una matriz de valores de tráfico (0-255)."""
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        mask_green    = cv2.inRange(hsv, np.array([35, 40, 40]),   np.array([85, 255, 255]))
        mask_orange   = cv2.inRange(hsv, np.array([10, 100, 100]), np.array([25, 255, 255]))
        mask_red      = self._color_mask(rgb, self._red_rgb)
        mask_dark_red = self._color_mask(rgb, self._dark_red_rgb)

        matrix = np.zeros(image.shape[:2], dtype=np.uint8)
        matrix[mask_green    > 0] = self.TRAFFIC_VALUES['green']
        matrix[mask_orange   > 0] = self.TRAFFIC_VALUES['orange']
        matrix[mask_red      > 0] = self.TRAFFIC_VALUES['red']
        matrix[mask_dark_red > 0] = self.TRAFFIC_VALUES['dark_red']
        return matrix

    def _sample_matrix(self, matrix: np.ndarray, coords: list, radio: int) -> list:
        """Extrae valores de la matriz en las coordenadas dadas (con radio)."""
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

    @staticmethod
    def _intermediate_coords(coord1: list, coord2: list, steps: int) -> list:
        """Devuelve puntos intermedios entre dos coordenadas (en píxeles)."""
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

    def _street_length(self, connection: tuple) -> float:
        """Distancia en píxeles entre los dos extremos de una calle."""
        x1, y1 = self.position_of_vertices[connection[0]]
        x2, y2 = self.position_of_vertices[connection[1]]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def _color_mask(rgb_image: np.ndarray, color_list: np.ndarray) -> np.ndarray:
        """Máscara booleana: píxeles que coinciden con algún color de la lista."""
        mask = np.zeros(rgb_image.shape[:2], dtype=bool)
        for color in color_list:
            mask |= np.all(rgb_image == color, axis=-1)
        return mask.astype(np.uint8)

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> tuple:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# ----------------------------------------------------------------------
# Uso
# ----------------------------------------------------------------------
if __name__ == '__main__':
    processor = ImageProcessor(
        path_dir_screenshots  = "data/raw/Images/screenshotsGoogleMaps/screenshots",
        path_dir_network_data = "data/DataMakeNetwork/PuntaArenasDetallado",
    )

    df_mean, df_max = processor.images_to_dataframe(steps=1, radio=0)

    os.makedirs("data/processed", exist_ok=True)
    df_mean.to_csv("data/processed/traffic_mean.csv", index=False)
    df_max.to_csv( "data/processed/traffic_max.csv",  index=False)

    print(f"\nListo. Filas (calles): {len(df_mean)}, Columnas (instantes): {len(df_mean.columns) - 3}")
    print("Archivos guardados en data/processed/")