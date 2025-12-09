#!/usr/bin/env python3
"""
Digital Taximeter - Professional taxi fare calculation system
Entry point for the restructured application

Run with: python main.py
"""

if __name__ == "__main__":
    try:
        import sys
        import os
        
        # Add src directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(current_dir, 'src')
        sys.path.insert(0, src_dir)
        sys.path.insert(0, current_dir)
        
        from taximeter_app import main
        print("🚀 Starting Digital Taximeter")
        main()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📦 Make sure dependencies are installed:")
        print("   pip install -r requirements.txt")
        print("\n🔧 If the problem persists, check the project structure.")
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
