#!/usr/bin/env python3
"""
Node Agent Runner
Run the Node tier agent from the agentic system root directory
"""

import sys
import os
import subprocess

def main():
    """Run the Node agent with proper path setup"""
    
    # Add the node agent directory to Python path
    node_path = os.path.join(os.path.dirname(__file__), 'node', 'node-agent')
    if node_path not in sys.path:
        sys.path.insert(0, node_path)
    
    # Change to node agent directory for relative imports
    original_cwd = os.getcwd()
    os.chdir(node_path)
    
    try:
        # Import and run the agent
        from run_agent import main as run_agent_main
        run_agent_main()
    except ImportError as e:
        print(f"Error importing node agent: {e}")
        print("Make sure you've installed the requirements:")
        print("pip install -r node/node-agent/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error running node agent: {e}")
        sys.exit(1)
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

if __name__ == "__main__":
    main()
