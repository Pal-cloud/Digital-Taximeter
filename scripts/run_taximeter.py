#!/usr/bin/env python3
"""
Digital Taximeter - Standalone CLI Runner

This script provides a simple command line interface to run
the Digital Taximeter with additional options.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for the CLI runner."""
    print("🚕 Digital Taximeter - Starting...")
    
    try:
        # Import and run the main taximeter function
        from main import taximeter
        taximeter()
    except KeyboardInterrupt:
        print("\n👋 Taximeter interrupted by user. Goodbye!")
    except ImportError as e:
        print(f"❌ Error importing main module: {e}")
        print("Make sure main.py is in the same directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
