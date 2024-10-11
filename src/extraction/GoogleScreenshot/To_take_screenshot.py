import os
import time
from datetime import datetime
from utils.screenshot_utils import take_screenshot
from utils.map_utils import generate_map_html

def main():
    # Parameters
    api_key = "AIzaSyBGmInnA0XmKh8AoW8SjlCVDEQzAhGyQto" # put you api key for Google Platform
    coords = {
        "southwest": {"lat": -53.182604877545785, "lng": -70.95911023010035},
        "northeast": {"lat": -53.17809805517051, "lng": -70.88282359600152}
    }

    include_traffic = True
    zoom = 15
    output_html = "map.html"
    output_dir = "figures"
    period_for_screenshot = 1 # in minutes

    # Generar HTML
    generate_map_html(api_key, coords, zoom,  include_traffic, output_html)

    # Crear directorio si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        print(f'Starting screenshots every {period_for_screenshot} minutes...')
        while True:
            current_minutes = datetime.now().minute
            if current_minutes % period_for_screenshot == 0:
                take_screenshot(output_dir, f"file://{os.path.abspath(output_html)}")
                time.sleep(5)
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        print('End')

if __name__ == '__main__':
    main()
