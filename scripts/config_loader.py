#!/usr/bin/env python3
"""
Simple configuration loader for the Agentic Framework.

Loads configuration from config.toml and provides clean access to settings.
"""

import os
import toml
from typing import Dict, Any
from pathlib import Path
from .simple_env import get_api_key

# Load configuration
CONFIG_FILE = Path(__file__).parent.parent / "config.toml"

def load_config() -> Dict[str, Any]:
    """Load configuration from config.toml"""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")
    
    with open(CONFIG_FILE, 'r') as f:
        return toml.load(f)

# Global config instance
_config = load_config()

def get_api_config() -> Dict[str, Any]:
    """Get API configuration with environment overrides."""
    api_config = _config['api'].copy()
    
    # Override with environment variables if set
    if os.getenv('MODEL_NAME'):
        api_config['model'] = os.getenv('MODEL_NAME')
    if os.getenv('DEFAULT_TEMPERATURE'):
        api_config['temperature'] = float(os.getenv('DEFAULT_TEMPERATURE'))
    if os.getenv('API_TIMEOUT'):
        api_config['timeout'] = int(os.getenv('API_TIMEOUT'))
    
    return api_config

def get_tier_config(tier_name: str) -> Dict[str, Any]:
    """Get configuration for a specific tier."""
    api_config = get_api_config()
    
    # Get tier-specific overrides
    tier_config = _config.get('tiers', {}).get(tier_name, {})
    
    # Merge with API config
    return {**api_config, **tier_config}

def get_openrouter_headers() -> Dict[str, str]:
    """Get headers for OpenRouter API calls."""
    # Try config file first, then environment
    config = load_config()
    api_key = config.get('api', {}).get('api_key')

    if not api_key or api_key == "PUT_YOUR_OPENROUTER_API_KEY_HERE":
        # Fallback to environment variable
        api_key = get_api_key()

    if not api_key or api_key == "PUT_YOUR_OPENROUTER_API_KEY_HERE":
        raise ValueError("OPENROUTER_API_KEY not found in config.toml or environment")

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/dusty-schmidt/agentic-framework",
        "X-Title": "Agentic Framework"
    }

def create_model_request_payload(messages: list, tier_name: str = "node") -> Dict[str, Any]:
    """Create a request payload for the model API."""
    config = get_tier_config(tier_name)
    
    return {
        "model": config["model"],
        "messages": messages,
        "temperature": config["temperature"],
        "max_tokens": config.get("max_tokens", 1000),
        "stream": False
    }

def get_system_config() -> Dict[str, Any]:
    """Get system configuration."""
    return _config.get('system', {})

# Backward compatibility functions
def get_model_config(tier_name: str = "node") -> Dict[str, Any]:
    """Backward compatibility function."""
    return get_tier_config(tier_name)

def get_tier_configs() -> Dict[str, Dict[str, Any]]:
    """Get all tier configurations."""
    return {
        tier: get_tier_config(tier) 
        for tier in ['node', 'link', 'mesh', 'grid']
    }
