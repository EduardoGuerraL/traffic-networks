from PIL import Image
import imageio
import os


def extract_time(filename):
    # Extraer la hora del nombre de archivo en formato "scatter_CC_hour = 18:0.png"
    time_str = filename.split('=')[-1].split('.png')[0].strip()
    hour, minute = map(int, time_str.split(':'))
    return hour, minute

def create_gif(image_folder, output_gif, duration=0.5):
    # Lista todos los archivos en la carpeta de imágenes y ordenalos cronológicamente
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')], key=extract_time)

    images = []
    for filename in image_files:
        file_path = os.path.join(image_folder, filename)
        img = Image.open(file_path)
        images.append(img)

    # Guarda las imágenes como GIF
    imageio.mimsave(output_gif, images, duration=duration)

if __name__ == "__main__":
    # Ruta de la carpeta con las imágenes (asegúrate de tener imágenes en la carpeta)
    input_folder = "data/Images/resultados/EHR_detallado_calles"

    # Ruta de salida del archivo GIF
    output_gif_path = "ruta_del_archivo.gif"

    # Duración en segundos para cada frame del GIF (0.5 segundos por defecto)
    frame_duration = 0.5

    create_gif(input_folder, output_gif_path, duration=frame_duration)