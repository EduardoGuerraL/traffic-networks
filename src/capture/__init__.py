# capture/__init__.py

from .screenshot_taker import take_screenshot
from .map_generator import generate_map_html
from .config import CONFIG

__all__ = ['take_screenshot', 'generate_map_html', 'CONFIG']
