# capture/screenshot_taker.py

import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_screenshot(output_dir, html_path):
    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    chrome_options.add_argument("--headless=new")  # evita problemas con Chrome reciente
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")  # modo headless
    chrome_options.add_argument("--no-sandbox")  # importante en muchos linux
    chrome_options.add_argument("--disable-dev-shm-usage")  # evita errores de espacio compartido
    chrome_options.add_argument("--disable-gpu")  # para evitar problemas con GPU
    chrome_options.add_argument("--remote-debugging-port=9222")  # a veces ayuda

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(800, 740)

    driver.get(f"file://{os.path.abspath(html_path)}")
    time.sleep(5)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    filepath = os.path.join(output_dir, f"{timestamp}.png")
    driver.save_screenshot(filepath)
    print(f"[✔] Saved: {filepath}")

    driver.quit()
