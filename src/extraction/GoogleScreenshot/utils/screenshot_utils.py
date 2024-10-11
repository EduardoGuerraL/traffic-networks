import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_screenshot(output_dir, url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(800, 740)

    driver.get(url)
    time.sleep(5)  # Esperar a que la página se cargue completamente

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
    screenshot_path = os.path.join(output_dir, f'{timestamp}.png')
    driver.save_screenshot(screenshot_path)
    print(f'Screenshot save in: {screenshot_path}')
    driver.quit()