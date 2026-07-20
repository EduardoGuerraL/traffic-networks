# run_capture.py

import os
import time
from datetime import datetime

from capture.config import CONFIG
from capture.map_generator import generate_map_html
from capture.screenshot_taker import take_screenshot

def main():
    print("[INFO] Generating map HTML...")
    generate_map_html(
        api_key=CONFIG["API_KEY"],
        coords=CONFIG["COORDS"],
        zoom=CONFIG["ZOOM"],
        include_traffic=CONFIG["INCLUDE_TRAFFIC"],
        output_file=CONFIG["OUTPUT_HTML"]
    )

    os.makedirs(CONFIG["OUTPUT_DIR"], exist_ok=True)
    print(f"[INFO] Capturing screenshots every {CONFIG['PERIOD_MINUTES']} minute(s). Press Ctrl+C to stop.")

    try:
        while True:
            now = datetime.now()
            if now.minute % CONFIG["PERIOD_MINUTES"] == 0:
                take_screenshot(CONFIG["OUTPUT_DIR"], CONFIG["OUTPUT_HTML"])
                time.sleep(60)
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Stopped.")

if __name__ == "__main__":
    main()
