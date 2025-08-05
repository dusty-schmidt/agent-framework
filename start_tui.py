#!/usr/bin/env python3
"""
Main launcher for the Agentic System TUI Manager
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the TUI manager"""
    print("🚀 Starting Agentic System TUI Manager...")
    print("=========================================")
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Add frontend/tui to Python path
    tui_path = script_dir / "frontend" / "tui"
    if str(tui_path) not in sys.path:
        sys.path.insert(0, str(tui_path))
    
    # Check if TUI files exist
    if not (tui_path / "unified_tui.py").exists():
        print("❌ TUI files not found in frontend/tui/!")
        sys.exit(1)
    
    # Check dependencies
    try:
        import textual
        import rich
        print("✅ Dependencies available")
    except ImportError:
        print("📦 Installing TUI dependencies...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "-r", str(tui_path / "requirements_tui.txt")
            ])
            print("✅ Dependencies installed!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            sys.exit(1)
    
    # Launch the TUI
    print("🎨 Launching TUI Manager...")
    print("   Use Ctrl+C to exit")
    print("   Use Tab to navigate between tabs")
    print("   Click buttons to control tiers")
    print("")
    
    try:
        # Change to TUI directory for proper imports
        os.chdir(tui_path)
        from minimal_tui import main as tui_main
        tui_main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error running TUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
