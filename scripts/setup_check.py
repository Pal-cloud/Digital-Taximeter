#!/usr/bin/env python3
"""
Digital Taximeter - Setup and Installation Helper

This module provides utilities for setting up the Digital Taximeter
application and verifying the installation.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    min_version = (3, 6)
    current_version = sys.version_info[:2]
    
    if current_version < min_version:
        print(f"❌ Python {min_version[0]}.{min_version[1]}+ required")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        return False
    
    print(f"✅ Python {current_version[0]}.{current_version[1]} - Compatible")
    return True

def check_dependencies():
    """Check if optional dependencies are available."""
    optional_deps = ['colorama', 'rich', 'pytest']
    available = []
    missing = []
    
    for dep in optional_deps:
        try:
            __import__(dep)
            available.append(dep)
        except ImportError:
            missing.append(dep)
    
    if available:
        print(f"✅ Available dependencies: {', '.join(available)}")
    
    if missing:
        print(f"ℹ️  Optional dependencies not installed: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt to install them")
    
    return len(missing) == 0

def setup_logs_directory():
    """Ensure logs directory exists."""
    logs_dir = Path("logs")
    
    if not logs_dir.exists():
        logs_dir.mkdir()
        print(f"✅ Created logs directory: {logs_dir}")
    else:
        print(f"✅ Logs directory exists: {logs_dir}")
    
    return True

def verify_installation():
    """Verify that all core files are present."""
    required_files = [
        "main.py",
        "taximeter.ipynb", 
        "README.md",
        "requirements.txt"
    ]
    
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All core files present")
    return True

def run_tests():
    """Run the test suite if available."""
    tests_dir = Path("tests")
    
    if not tests_dir.exists():
        print("ℹ️  No tests directory found")
        return False
    
    print("🧪 Running tests...")
    try:
        result = subprocess.run([sys.executable, "-m", "unittest", "discover", "tests", "-v"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def main():
    """Main setup function."""
    print("🚕 Digital Taximeter - Setup and Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("File Verification", verify_installation),
        ("Logs Directory", setup_logs_directory),
        ("Dependencies", check_dependencies),
        ("Tests", run_tests)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} failed: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("Run 'python main.py' or 'python run_taximeter.py' to start")
    else:
        print("⚠️  Setup completed with some issues")
        print("Check the messages above and fix any problems")

if __name__ == "__main__":
    main()
