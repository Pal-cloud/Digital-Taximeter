"""
Utility functions for Digital Taximeter UI and formatting
"""
import os
import sys
from config.settings import COLORS_AVAILABLE, Fore, Style

def print_colored(message, color=None, style=None, end='\n'):
    """Print with colors if available, otherwise plain text."""
    # Default to yellow color if no color specified
    if color is None:
        color = 'yellow'
    
    try:
        if COLORS_AVAILABLE and color and Fore:
            color_code = getattr(Fore, color.upper(), '')
            style_code = getattr(Style, style.upper(), '') if style and Style else ''
            reset = Style.RESET_ALL if Style else ''
            print(f"{style_code}{color_code}{message}{reset}", end=end)
        else:
            print(message, end=end)
    except (TypeError, UnicodeEncodeError):
        # Fallback for terminals with encoding issues
        try:
            print(message, end=end)
        except UnicodeEncodeError:
            # Last resort: strip emojis and unicode chars
            import re
            clean_message = re.sub(r'[^\x00-\x7F]+', '?', message)
            print(clean_message, end=end)

def clear_screen():
    """Clear the terminal screen in a cross-platform way."""
    os.system('cls' if os.name == 'nt' else 'clear')

def format_currency(amount):
    """Format currency amount to 2 decimal places."""
    return f"€{amount:.2f}"

def format_time(seconds):
    """Format time in seconds to a readable format."""
    return f"{seconds:.1f}s"
