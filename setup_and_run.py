#!/usr/bin/env python3
"""
Setup and Run Script for Mood Tracker Dashboard

This script:
1. Converts your Markdown journal files to CSV format
2. Launches the dashboard with your personal data
3. Ensures everything is set up correctly
"""

import subprocess
import sys
import os

def main():
    """
    Main function to set up and run the dashboard
    """
    print("🧠 Mood Tracker Dashboard - Setup & Run")
    print("=" * 50)
    
    # Step 1: Convert journal files
    print("\n🔄 Step 1: Converting your journal files...")
    try:
        result = subprocess.run([sys.executable, 'convert_journal.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Journal conversion completed successfully!")
            print(result.stdout)
        else:
            print("❌ Journal conversion failed:")
            print(result.stderr)
            return
            
    except Exception as e:
        print(f"❌ Error running conversion: {e}")
        return
    
    # Step 2: Launch dashboard
    print("\n🚀 Step 2: Launching dashboard...")
    print("The dashboard will open in your browser.")
    print("Press Ctrl+C to stop the server.")
    print()
    
    try:
        subprocess.run([sys.executable, 'run_dashboard.py'])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped.")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")

if __name__ == "__main__":
    main() 