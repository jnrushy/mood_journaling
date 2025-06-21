#!/usr/bin/env python3
"""
Quick launcher for the Mood Tracker Dashboard.

This script sets up the environment and launches the Streamlit dashboard.
It includes error checking and helpful messages for common issues.
"""

import sys
import os
import subprocess
import importlib.util

def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        'streamlit',
        'textblob', 
        'pandas',
        'plotly',
        'matplotlib',
        'wordcloud'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install them with:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_data_file():
    """Check if the sample data file exists."""
    data_file = 'data/journal_entries.csv'
    
    if not os.path.exists(data_file):
        print(f"❌ Sample data file not found: {data_file}")
        print("\n💡 The sample data file is already created with example entries.")
        print("   You can replace it with your own journal data from Notion.")
        return False
    
    print("✅ Sample data file found!")
    return True

def main():
    """Main function to launch the dashboard."""
    print("🧠 Mood Tracker Dashboard Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check data file
    if not check_data_file():
        return
    
    print("\n🚀 Launching dashboard...")
    print("   The dashboard will open in your web browser.")
    print("   Press Ctrl+C to stop the server.")
    print()
    
    try:
        # Launch Streamlit dashboard
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 
            'app/dashboard.py',
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped.")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        print("\n💡 Try running manually:")
        print("   streamlit run app/dashboard.py")

if __name__ == "__main__":
    main() 