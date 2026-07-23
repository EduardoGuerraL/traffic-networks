import requests
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

API_KEY = ""
CENTER = "53.349805,-6.26031"  # Ejemplo: Dublín
ZOOM = 15
SIZE = "640x640"
TRAFFIC_LAYER = "traffic"  # Para tráfico real en Google Static Maps, se usa "style=feature:traffic|visibility:on" pero en Static Maps no es oficial

def get_traffic_map_image(center, zoom, size, api_key, output_path):
    # Google Static Maps no soporta oficialmente capa de tráfico, pero podemos intentar con tráfico visible en JS + captura, o con tráfico en JS + Selenium
    # Aquí solo descarga mapa estático sin tráfico porque tráfico no es oficial en Static Maps
    url = f"https://maps.googleapis.com/maps/api/staticmap?center={center}&zoom={zoom}&size={size}&key={api_key}"
    print(f"[INFO] Downloading map image from: {url}")
    r = requests.get(url)
    if r.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(r.content)
        print(f"[INFO] Image saved to {output_path}")
    else:
        print(f"[ERROR] Failed to get map image. Status code: {r.status_code}")

# Si quieres el tráfico visible con Selenium y Google Maps JS, se hace así:

def capture_traffic_with_selenium(lat, lon, zoom, output_path, wait_time=5):
    # Configuración de Selenium
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=800,600")
    
    driver = webdriver.Chrome(options=options)

    # URL con tráfico activado en Google Maps JavaScript
    url = f"https://www.google.com/maps/@{lat},{lon},{zoom}z/data=!5m1!1e1"  # !1e1 activa capa de tráfico

    print(f"[INFO] Loading URL: {url}")
    driver.get(url)
    
    time.sleep(wait_time)  # Esperar que cargue
    
    # Tomar screenshot
    driver.save_screenshot(output_path)
    print(f"[INFO] Screenshot saved to {output_path}")
    
    driver.quit()

import requests

def get_city_bbox(city_name):
    url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    data = response.json()
    if not data:
        raise ValueError("City not found.")
    bbox = data[0]['boundingbox']  # [south, north, west, east]
    return list(map(float, bbox))


import numpy as np

def generate_grid(bbox, steps_lat=3, steps_lon=3):
    south, north, west, east = bbox
    lats = np.linspace(south, north, steps_lat)
    lons = np.linspace(west, east, steps_lon)
    grid_centers = [(lat, lon) for lat in lats for lon in lons]
    return grid_centers

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from datetime import datetime

def capture_tile(lat, lon, zoom, output_dir):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1280,720")
    driver = webdriver.Chrome(options=options)

    url = f"https://www.google.com/maps/@{lat},{lon},{zoom}z/data=!5m1!1e1"
    driver.get(url)
    time.sleep(5)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/traffic_{lat}_{lon}_{timestamp}.png"
    driver.save_screenshot(filename)
    print(f"[INFO] Saved {filename}")
    
    driver.quit()
def capture_full_city(city_name, zoom=13, grid_size=(3, 3), output_dir="city_traffic"):
    os.makedirs(output_dir, exist_ok=True)
    bbox = get_city_bbox(city_name)
    grid = generate_grid(bbox, steps_lat=grid_size[0], steps_lon=grid_size[1])
    for lat, lon in grid:
        capture_tile(lat, lon, zoom, output_dir)

if __name__ == "__main__":
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    capture_full_city("Santiago, Chile", zoom=13, grid_size=(4, 4))
