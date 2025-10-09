import os
import time
from datetime import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

def take_screenshot(output_dir, url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(800, 740)

    driver.get(url)
    time.sleep(40)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    screenshot_path = os.path.join(output_dir, f'{timestamp}.png')
    driver.save_screenshot(screenshot_path)
    print(f'Captura de pantalla guardada en: {screenshot_path}')
    driver.quit()

def screenshots_in_time(direccion_guardar_imagenes):

    url = "file:////home/chuleo/Investigation/Transporte/FinalVersion/src/GoogleScreenshot/query_with_traffic.html"
    output_dir = direccion_guardar_imagenes

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        print('Iniciando programa...')
        take_screenshot(direccion_guardar_imagenes, url)
        while True:
            current_minutes = datetime.now().minute
            if current_minutes % 15 == 0:
                take_screenshot(direccion_guardar_imagenes, url)
                time.sleep(60)  # Dormir durante un minuto antes de verificar de nuevo
            else:
                time.sleep(5)  # Verificar cada 5 segundos si es múltiplo de 15
    except KeyboardInterrupt:
        print('Programa finalizado por el usuario.')

def take_clean_screenshot(direccion_guardar_imagenes):
    url = "file:////home/chuleo/Investigation/Transporte/FinalVersion/src/GoogleScreenshot/query_clean.html"
    output_dir = direccion_guardar_imagenes

    take_screenshot(output_dir, url)


if __name__ == '__main__':
    take_clean_screenshot("probando")