import matplotlib.pyplot as plt
from PIL import Image

def mostrar_decima_parte(imagen_path):
    # Cargamos la imagen usando PIL
    imagen = Image.open(imagen_path)

    # Obtenemos las dimensiones originales de la imagen
    ancho_original, alto_original = imagen.size

    # Calculamos las nuevas dimensiones reducidas a una décima parte
    ancho_nuevo = ancho_original // 10
    alto_nuevo = alto_original // 10

    # Redimensionamos la imagen a una décima parte
    imagen_redimensionada = imagen.resize((ancho_nuevo, alto_nuevo), Image.ANTIALIAS)

    # Mostramos la imagen original
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(imagen)
    plt.title("Imagen Original")

    # Mostramos la imagen reducida a una décima parte
    plt.subplot(1, 2, 2)
    plt.imshow(imagen_redimensionada)
    plt.title("Imagen Reducida (1/10)")

    plt.show()

# Ruta de la imagen que deseas mostrar
imagen_path = "data/Images/screenshots/2023-03-29_08-00.png" 
mostrar_decima_parte(imagen_path)
