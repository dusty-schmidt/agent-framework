#!/usr/bin/env python3
"""
Standardized environment setup for the Agentic Framework.

This script ensures consistent Python path setup and environment handling
across all tiers and components.
"""

import sys
import os
from pathlib import Path

def setup_project_environment():
    """
    Set up the project environment with standardized paths.
    
    This should be called at the beginning of any script that needs
    to import from the agentic framework modules.
    """
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    
    # Add project root to Python path if not already there
    project_root_str = str(project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    
    # Set environment variables for consistent behavior
    os.environ['AGENTIC_FRAMEWORK_ROOT'] = project_root_str
    os.environ['PYTHONPATH'] = f"{project_root_str}:{os.environ.get('PYTHONPATH', '')}"
    
    print(f"✅ Agentic Framework environment initialized")
    print(f"   Project root: {project_root}")
    print(f"   Python path updated")
    
    return project_root

def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.absolute()

def get_tier_path(tier_name: str):
    """Get the path to a specific tier."""
    return get_project_root() / tier_name

def get_data_path(component: str = ""):
    """Get the path to data storage."""
    data_path = get_project_root() / "data"
    if component:
        data_path = data_path / component
    data_path.mkdir(parents=True, exist_ok=True)
    return data_path

def get_logs_path():
    """Get the path to logs directory."""
    logs_path = get_project_root() / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)
    return logs_path

def get_config_path():
    """Get the path to configuration files."""
    return get_project_root() / "central_nervous_system" / "config"

if __name__ == "__main__":
    # Test the environment setup
    root = setup_project_environment()
    
    print("\n📁 Project structure:")
    print(f"   Root: {root}")
    print(f"   Data: {get_data_path()}")
    print(f"   Logs: {get_logs_path()}")
    print(f"   Config: {get_config_path()}")
    
    # Test imports
    try:
        print("\n🧪 Testing imports...")
        from unified_memory.memory_interface import UnifiedMemoryItem
        print("   ✅ unified_memory imports working")
    except ImportError as e:
        print(f"   ❌ unified_memory import failed: {e}")
    
    print("\n🎯 Environment setup complete!")
