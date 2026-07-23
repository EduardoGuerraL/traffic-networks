import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math

class ImageProcessor:
    def __init__(self, path_dir_screenshots):
        self.path_dir_screenshots = path_dir_screenshots

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def create_mask(self, image, color_list):
        mask = np.zeros((image.shape[0], image.shape[1]), dtype=bool)
        for color in color_list:
            mask |= np.all(image == color, axis=-1)
        return mask.astype(np.uint8)
    
    def mostrar_imagen_limpia(self, path_imagen):
        # Leer la imagen desde el archivo
        image = cv2.imread(path_imagen)
        if image is None:
            raise ValueError(f"No se pudo cargar la imagen desde la ruta: {path_imagen}")

        # Convertir la imagen a espacio de color HSV y RGB
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Definir rangos de colores en HSV
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        lower_orange = np.array([10, 100, 100])
        upper_orange = np.array([25, 255, 255])

        # Definir colores rojo y rojo oscuro en formato hexadecimal
        red_colors = [
            '#f23c32', '#f3493f', '#f56159', '#f4554c', '#f66e66',
            '#f77a73', '#f88680', '#f9928d', '#faaba6'
        ]
        dark_red_colors = [
            '#811f1f', '#892d2d', '#994949', '#913b3b',
            '#b17373', '#c18f8f', '#d1abab'
        ]

        # Convertir los colores hexadecimales a RGB
        red_colors_rgb = np.array([self.hex_to_rgb(color) for color in red_colors])
        dark_red_colors_rgb = np.array([self.hex_to_rgb(color) for color in dark_red_colors])

        # Crear máscaras para cada grupo de colores
        mask_green = cv2.inRange(hsv_image, lower_green, upper_green)
        mask_orange = cv2.inRange(hsv_image, lower_orange, upper_orange)
        mask_red = self.create_mask(rgb_image, red_colors_rgb)
        mask_dark_red = self.create_mask(rgb_image, dark_red_colors_rgb)

        # Crear imagen en color (3 canales)
        color_image = np.zeros((hsv_image.shape[0], hsv_image.shape[1], 3), dtype=np.uint8)

        # Asignar colores específicos a cada máscara
        color_image[mask_green > 0] = (104, 214, 99)  # Gris oscuro (RGB)
        color_image[mask_orange > 0] = (77, 151, 255)  # Un color gris específico (RGB)
        color_image[mask_red > 0] = (0, 0, 255)  # Rojo claro (#f23c32 en RGB)
        color_image[mask_dark_red > 0] = (0, 0, 139)  # Rojo oscuro (#892d2d en RGB)

        # Crear una máscara para los píxeles negros (0, 0, 0)
        mask_black = np.all(color_image == (0, 0, 0), axis=-1)
        # Reemplazar los píxeles negros con (255, 255, 255)
        color_image[mask_black] = (255, 255, 255)
        
        # Mostrar la imagen resultante
        cv2.imshow('Imagen en colores', color_image)
        cv2.waitKey(0)
           
    def mostrar_imagen_desde_txt(self, direccion_archivo_txt):
            """
            Lee un archivo de texto con valores de 0.25, 0.50, 0.75, 1,
            los convierte a una imagen en escala de grises y muestra la imagen.

            :param direccion_archivo_txt: La dirección del archivo de texto que contiene los valores de los píxeles.
            """
            # Leer el archivo de texto
            matriz_pixeles = np.loadtxt(direccion_archivo_txt)
            
            # Verificar que los valores sean válidos
            valores_validos = {0, 0.25, 0.50, 0.75, 1.00}
            if not set(np.unique(matriz_pixeles)).issubset(valores_validos):
                raise ValueError("El archivo de texto contiene valores que no están en la escala esperada (0.25, 0.50, 0.75, 1.00).")

            # Mostrar la imagen
            plt.imshow(matriz_pixeles, cmap='gray', vmin=0, vmax=1)
            plt.colorbar(label='Intensidad')
            plt.title('Imagen en Escala de Grises')
            plt.axis('off')  # Opcional: Ocultar los ejes
            plt.show()  

    def Image2GrayMatrix(self, image):
        # Convertir la imagen a espacio de color HSV y RGB
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Definir rangos de colores en HSV
        # Verde
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])


        lower_orange = np.array([10, 100, 100])
        upper_orange = np.array([25, 255, 255])

        red_colors = [
            '#f23c32', '#f3493f', '#f56159', '#f4554c', '#f66e66',
            '#f77a73', '#f88680', '#f9928d', '#faaba6'
        ]

        dark_red_colors = [
            '#811f1f', '#892d2d', '#994949', '#913b3b',
            '#b17373', '#c18f8f', '#d1abab'
        ]

        # Convertir los colores hexadecimales a RGB
        red_colors_rgb = np.array([self.hex_to_rgb(color) for color in red_colors])
        dark_red_colors_rgb = np.array([self.hex_to_rgb(color) for color in dark_red_colors])

        # Crear máscaras para cada grupo de colores
        mask_green = cv2.inRange(hsv_image, lower_green, upper_green)
        mask_orange = cv2.inRange(hsv_image, lower_orange, upper_orange)
        mask_red = self.create_mask(rgb_image, red_colors_rgb)
        mask_dark_red = self.create_mask(rgb_image, dark_red_colors_rgb)

        # Crear imagen en escala de grises
        gray_image = np.zeros((hsv_image.shape[0], hsv_image.shape[1]), dtype=np.uint8)

        # Asignar valores de gris específicos
        gray_image[mask_green > 0] = 64
        gray_image[mask_orange > 0] = 128
        gray_image[mask_red > 0] = 191
        gray_image[mask_dark_red> 0] = 255

        return gray_image

    def getAllDataInTxtFiles(self, directorio, path_to_save):
        total_images = len([f for f in os.listdir(directorio) if f.endswith(".png")])
        for indice, filename in enumerate(os.listdir(directorio)):
            if filename.endswith(".png"):
                path = os.path.join(directorio, filename)
                imagen = cv2.imread(path)
                if imagen is None:
                    print(f"Error al cargar la imagen {filename}")
                    continue
                grayMatrix = self.Image2GrayMatrix(imagen)
                nombre_txt = os.path.splitext(filename)[0] + ".txt"
                np.savetxt(os.path.join(path_to_save, nombre_txt), grayMatrix)
                print(f"Avance: {indice + 1}/{total_images}")

    def Images2GrayImages(self, directorio_destino):
        
        directorio_origen = self.path_dir_screenshots
        if not os.path.exists(directorio_destino):
            os.makedirs(directorio_destino)
        
        total_images = len(os.listdir(directorio_origen))
        for indice, filename in enumerate(os.listdir(directorio_origen)):
            if filename.endswith(".png"):
                path = os.path.join(directorio_origen, filename)
                imagen = cv2.imread(path)
                if imagen is None:
                    print(f"Error al cargar la imagen {filename}")
                    continue
                grayMatrix = self.Image2GrayMatrix(imagen)

                nombre_png = os.path.splitext(filename)[0] + ".png"

                cv2.imwrite(os.path.join(directorio_destino, nombre_png), grayMatrix)
                print(f"Avance: {indice + 1}/{total_images}")
    
    def GrayMatrix2StreetData(self, path_network, steps, radio, path_to_save):
                    
        def coordenadas_intermedias(coord1, coord2, steps):
            coordenadas_intermedias = []
            coord1[0] = round(coord1[0])
            coord1[1] = round(coord1[1])
            coord2[0] = round(coord2[0])
            coord2[1] = round(coord2[1])

            step_x = (coord2[0] - coord1[0]) / (steps + 1)
            step_y = (coord2[1] - coord1[1]) / (steps + 1)

            for i in range(0, steps + 1):
                intermedio_x = int(coord1[0] + i * step_x)
                intermedio_y = int(coord1[1] + i * step_y)
                coordenadas_intermedias.append((intermedio_x, intermedio_y))
            
            coordenadas_intermedias.append((int(coord2[0]), int(coord2[1])))                               
            return coordenadas_intermedias

        def obtener_datos(matriz, posiciones):
            datos = []
            for posicion in posiciones:
                fila, columna = posicion
                for i in range(-radio, radio+1):
                    for j in range(-radio, radio+1):
                        dato = matriz[fila+i][columna+j]
                        if dato != 0:
                            datos.append(dato)
                if not datos:
                    datos.append(0)
            return datos

        def get_largo_camino(coord1, coord2):
            x1, y1 = coord1
            x2, y2 =  coord2
            distancia = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return distancia

        # Importando los datos de la red.

        image_no_traffic = plt.imread(self.path_dir_screenshots + "/2023-03-29_07-30.png") #Imagen temp/screenTest/2023-03-29_07-30.png
        path_dir_screenshots = str(self.path_dir_screenshots)

        position_of_vertices = eval(open(str(path_network)+"/Posiciones.dat", "r").readline())
        position_of_vertices = {} #Posiciones

        for i, tupla in enumerate(position_of_vertices):
            position_of_vertices[i] = list([tupla[0]*image_no_traffic.shape[1], tupla[1]*image_no_traffic.shape[0]])
        conections = eval(open(str(path_network)+"/Conexiones.dat", "r").readline())
        #self.lanes = eval(open(str(path_network)+"/Carriles.dat", "r").readline())
        
        # Abriendo cada una de las imagenes.
        directorio_origen = self.path_dir_screenshots
        total_images = len(os.listdir(directorio_origen))
        for indice, filename in enumerate(os.listdir(directorio_origen)):
            if filename.endswith(".png"):
                path = os.path.join(directorio_origen, filename)
                imagen = cv2.imread(path)
                if imagen is None:
                    print(f"Error al cargar la imagen {filename}")
                    continue
                grayMatrix = self.Image2GrayMatrix(imagen)
                print(grayMatrix)

                # AQUI se deben obtener los datos para las calles.




                print(f"Avance: {indice + 1}/{total_images}")

    
# Uso del código
processor = ImageProcessor("data/Images/screenshots")
#processor.Images2GrayImages("data/Images/screenshots_cleaned")
path_imagen = 'data/Images/screenshots/2023-03-29_07-45.png'
processor.mostrar_imagen_limpia(path_imagen)