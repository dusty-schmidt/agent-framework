#!/usr/bin/env python3
"""
Demo script to show the minimal TUI in action
"""

import os
import sys
from pathlib import Path

def main():
    """Run the minimal TUI demo"""
    print("🎯 Minimal TUI Demo")
    print("==================")
    print()
    print("This TUI provides:")
    print("• Simple tier panels: NODE | LINK | MESH | GRID")
    print("• Each panel has: NAME | LAUNCH | KILL | STATUS")
    print("• Right side: Color-coded logs panel")
    print("• Clean, functional design matching your mockup")
    print()
    print("Controls:")
    print("• Click LAUNCH to start a tier")
    print("• Click KILL to stop a tier")
    print("• Status indicator shows ● (green=running, red=stopped)")
    print("• Logs show color-coded output from all tiers")
    print("• Press Ctrl+C to exit")
    print()
    
    # Change to the correct directory
    root_dir = Path(__file__).parent
    os.chdir(root_dir)
    
    try:
        print("🚀 Starting Minimal TUI...")
        print("   (This will run for 10 seconds as a demo)")
        print()
        
        # Import and run the minimal TUI
        from frontend.tui.minimal_tui import MinimalTUI
        
        app = MinimalTUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n✅ Demo completed!")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you're in the agentic system directory")

if __name__ == "__main__":
    main()
