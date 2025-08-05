#!/usr/bin/env python3
"""
Super simple test script for the Minimal TUI
"""

import os
import sys
from pathlib import Path

def main():
    """Run the test TUI"""
    print("🎯 Testing Minimal TUI")
    print("=" * 30)
    print()
    print("This will launch a TEST VERSION with demo processes:")
    print("• Each tier runs a simple Python script")
    print("• You'll see colored output in real-time")
    print("• Click LAUNCH to start, KILL to stop")
    print("• Status indicators show green (running) / red (stopped)")
    print()
    print("🚀 Starting in 3 seconds...")
    print()
    
    import time
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    # Change to the correct directory
    root_dir = Path(__file__).parent
    tui_dir = root_dir / "frontend" / "tui"
    
    # Add to Python path
    sys.path.insert(0, str(tui_dir))
    
    try:
        # Import and run the test TUI
        from test_minimal_tui import TestMinimalTUI
        
        app = TestMinimalTUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n✅ Test completed!")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're in the agentic system directory")
        print("And that textual is installed: pip install textual")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
