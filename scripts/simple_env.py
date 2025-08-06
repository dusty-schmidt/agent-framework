#!/usr/bin/env python3
"""
Simple environment setup for conda + Docker deployment.

No complex environment management - just basic path setup.
API keys should be in your zsh config or Docker environment.
"""

import os
import sys
from pathlib import Path

def setup_simple_env():
    """Simple environment setup for conda and Docker."""
    # Add project root to Python path
    project_root = Path(__file__).parent.absolute()
    project_root_str = str(project_root)

    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)

    # Set basic environment variables (only if not already set)
    os.environ.setdefault('AGENTIC_FRAMEWORK_ROOT', project_root_str)
    os.environ.setdefault('LOG_LEVEL', 'INFO')

    return project_root

def get_api_key():
    """Get OpenRouter API key from environment (set in zsh config or Docker)."""
    # First try current environment
    api_key = os.getenv('OPENROUTER_API_KEY')

    # If it's the placeholder or missing, try to find the real one
    if not api_key or api_key == 'your_key_here':
        api_key = find_real_api_key()

    if not api_key or api_key == 'your_key_here':
        raise ValueError(
            "OPENROUTER_API_KEY not found. "
            "Add 'export OPENROUTER_API_KEY=your_key' to your ~/.zshrc or set in Docker environment."
        )
    return api_key

def find_real_api_key():
    """Try to find the real API key from shell profiles."""
    import subprocess

    print("🔍 Searching for API key in shell profiles...")

    # Try to get from shell profiles
    shell_commands = [
        'bash -c "source ~/.zshrc 2>/dev/null && echo $OPENROUTER_API_KEY"',
        'bash -c "source ~/.bashrc 2>/dev/null && echo $OPENROUTER_API_KEY"',
        'bash -c "source ~/.bash_profile 2>/dev/null && echo $OPENROUTER_API_KEY"',
        'zsh -c "source ~/.zshrc 2>/dev/null && echo $OPENROUTER_API_KEY"'
    ]

    for cmd in shell_commands:
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                key = result.stdout.strip()
                if key and key != 'your_key_here' and key.startswith('sk-'):
                    print(f"✅ Found API key in shell profile (length: {len(key)})")
                    # Update current environment
                    os.environ['OPENROUTER_API_KEY'] = key
                    return key
        except Exception:
            continue

    print("❌ Could not find valid API key in shell profiles")
    return None

def get_model_name():
    """Get the model name to use."""
    return os.getenv('MODEL_NAME', 'openai/gpt-oss-20b')

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
