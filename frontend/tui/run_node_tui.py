#!/usr/bin/env python3
"""
Node Agent TUI Runner
Run the Node tier agent with TUI from the agentic system root directory
"""

import sys
import os

def main():
    """Run the Node agent TUI with proper path setup"""

    # Get path to agentic system root and node agent directory
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    node_path = os.path.join(root_dir, 'node', 'node-agent')

    if node_path not in sys.path:
        sys.path.insert(0, node_path)

    # Change to node agent directory for relative imports
    original_cwd = os.getcwd()
    os.chdir(node_path)
    
    try:
        # Check if TUI dependencies are available
        try:
            import textual
            import rich
        except ImportError:
            print("TUI dependencies not found. Installing...")
            print("Run: pip install -r node/node-agent/requirements.txt")
            sys.exit(1)
        
        # Import and run the TUI agent
        from demo_tui import SimpleTUIDemo
        app = SimpleTUIDemo()
        app.run()
    except ImportError as e:
        print(f"Error importing node TUI agent: {e}")
        print("Make sure you've installed the requirements:")
        print("pip install -r node/node-agent/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error running node TUI agent: {e}")
        sys.exit(1)
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

if __name__ == "__main__":
    main()
