"""
Configuration settings for Digital Taximeter
"""
import os
import logging

# Fare rates (EUR per second)
FARE_RATES = {
    'stopped': 0.02,  # €0.02 per second when stopped
    'moving': 0.05,   # €0.05 per second when moving
}

# Logging configuration
LOG_DIR = 'logs'
LOG_FILE = 'taximeter.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_LEVEL = logging.INFO

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Terminal colors availability
try:
    from colorama import init, Fore, Back, Style
    import colorama
    colorama.init()  # For Windows compatibility
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    Fore = Back = Style = None

def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE), encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
