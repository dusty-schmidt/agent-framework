#!/usr/bin/env python3
"""
Simplified environment setup for development.

Just loads .env file and sets up basic paths. Perfect for development
and will work seamlessly with Docker deployment.
"""

import os
import sys
from pathlib import Path

def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_file = Path(__file__).parent / '.env'
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Only set if not already in environment (Docker takes precedence)
                    if key not in os.environ:
                        os.environ[key] = value
        print(f"✅ Loaded .env file")
    else:
        print(f"ℹ️  No .env file found (this is fine for Docker deployment)")

def setup_simple_env():
    """Simple environment setup for development and Docker."""
    # Load .env file first
    load_env_file()
    
    # Add project root to Python path
    project_root = Path(__file__).parent.absolute()
    project_root_str = str(project_root)
    
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    
    # Set basic environment variables
    os.environ.setdefault('AGENTIC_FRAMEWORK_ROOT', project_root_str)
    os.environ.setdefault('DEBUG', 'true')
    os.environ.setdefault('LOG_LEVEL', 'INFO')
    os.environ.setdefault('DEFAULT_MODEL', 'openai/gpt-oss-20b')
    
    return project_root

def get_api_key():
    """Get OpenRouter API key from environment."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY not found. "
            "Create a .env file with your API key or set the environment variable."
        )
    return api_key

def get_model_name():
    """Get the model name to use."""
    return os.getenv('DEFAULT_MODEL', 'openai/gpt-oss-20b')

def is_debug():
    """Check if debug mode is enabled."""
    return os.getenv('DEBUG', 'false').lower() in ('true', '1', 'yes')

def get_log_level():
    """Get the log level."""
    return os.getenv('LOG_LEVEL', 'INFO')

if __name__ == "__main__":
    # Test the simple environment setup
    print("🚀 Simple Environment Setup Test")
    print("=" * 40)
    
    try:
        root = setup_simple_env()
        print(f"Project root: {root}")
        print(f"Model: {get_model_name()}")
        print(f"Debug mode: {is_debug()}")
        print(f"Log level: {get_log_level()}")
        
        # Test API key
        try:
            api_key = get_api_key()
            print(f"API key: {'✅ Found' if api_key else '❌ Missing'}")
        except ValueError as e:
            print(f"API key: ❌ {e}")
        
        print("\n✅ Simple environment setup complete!")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)
