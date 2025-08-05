#!/usr/bin/env python3
"""
Standardized model configuration for the Agentic Framework.

This module provides consistent model configuration across all tiers,
using OpenRouter with the openai/gpt-oss-20b model for testing.
"""

import os
from typing import Dict, Any, Optional
from simple_env import get_api_key, get_model_name

# Standard model configuration (will use .env values)
def get_standard_config():
    return {
        "provider": "openrouter",
        "base_url": "https://openrouter.ai/api/v1",
        "model": get_model_name(),
        "max_tokens": int(os.getenv('DEFAULT_MAX_TOKENS', '1000')),
        "temperature": float(os.getenv('DEFAULT_TEMPERATURE', '0.7')),
        "timeout": int(os.getenv('API_TIMEOUT', '30'))
    }

# Tier-specific model configurations
def get_tier_configs():
    base_config = get_standard_config()
    return {
        "node": {
            **base_config,
            "temperature": 0.6,  # Slightly more focused
            "max_tokens": 800
        },
        "link": {
            **base_config,
            "temperature": 0.7,  # Balanced
            "max_tokens": 1200
        },
        "mesh": {
            **base_config,
            "temperature": 0.5,  # More focused for coordination
            "max_tokens": 1500
        },
        "grid": {
            **base_config,
            "temperature": 0.8,  # More creative for self-improvement
            "max_tokens": 2000
        }
    }

def get_model_config(tier_name: str = "default") -> Dict[str, Any]:
    """
    Get the model configuration for a specific tier.

    Args:
        tier_name: The tier name (node, link, mesh, grid) or "default"

    Returns:
        Dictionary containing model configuration
    """
    tier_configs = get_tier_configs()
    if tier_name in tier_configs:
        return tier_configs[tier_name].copy()
    return get_standard_config().copy()

def get_openrouter_headers() -> Dict[str, str]:
    """
    Get the headers needed for OpenRouter API calls.

    Returns:
        Dictionary containing required headers
    """
    api_key = get_api_key()  # This will handle the error message

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/dusty-schmidt/agent-framework",
        "X-Title": "Agentic Framework"
    }

def validate_model_name(model_name: str) -> bool:
    """
    Validate that a model name follows OpenRouter naming standards.
    
    Args:
        model_name: Model name to validate (should be "provider/model")
        
    Returns:
        True if valid, False otherwise
    """
    if "/" not in model_name:
        return False
    
    parts = model_name.split("/")
    if len(parts) != 2:
        return False
    
    provider, model = parts
    return bool(provider.strip() and model.strip())

def get_available_models() -> Dict[str, str]:
    """
    Get a list of commonly available models on OpenRouter.
    
    Returns:
        Dictionary mapping model names to descriptions
    """
    return {
        "openai/gpt-oss-20b": "OpenAI GPT OSS 20B - Good balance of capability and speed",
        "openai/gpt-3.5-turbo": "OpenAI GPT-3.5 Turbo - Fast and efficient",
        "openai/gpt-4": "OpenAI GPT-4 - High capability",
        "anthropic/claude-3-haiku": "Anthropic Claude 3 Haiku - Fast and efficient",
        "anthropic/claude-3-sonnet": "Anthropic Claude 3 Sonnet - Balanced capability",
        "meta-llama/llama-3.1-8b-instruct": "Meta Llama 3.1 8B - Open source",
        "google/gemini-pro": "Google Gemini Pro - Multimodal capabilities"
    }

def create_model_request_payload(messages: list, tier_name: str = "default", 
                               override_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized request payload for the model API.
    
    Args:
        messages: List of message dictionaries
        tier_name: The tier making the request
        override_config: Optional config overrides
        
    Returns:
        Dictionary containing the API request payload
    """
    config = get_model_config(tier_name)
    
    if override_config:
        config.update(override_config)
    
    return {
        "model": config["model"],
        "messages": messages,
        "max_tokens": config["max_tokens"],
        "temperature": config["temperature"],
        "stream": False  # For simplicity in testing
    }

if __name__ == "__main__":
    # Test the configuration
    print("🤖 Agentic Framework Model Configuration")
    print("=" * 50)
    
    print(f"Standard model: {STANDARD_MODEL_CONFIG['model']}")
    print(f"Provider: {STANDARD_MODEL_CONFIG['provider']}")
    print(f"Base URL: {STANDARD_MODEL_CONFIG['base_url']}")
    
    print("\n📊 Tier-specific configurations:")
    for tier, config in TIER_MODEL_CONFIGS.items():
        print(f"  {tier}: temp={config['temperature']}, tokens={config['max_tokens']}")
    
    print("\n🔍 Available models:")
    for model, desc in get_available_models().items():
        valid = "✅" if validate_model_name(model) else "❌"
        print(f"  {valid} {model}: {desc}")
    
    # Test API key
    try:
        headers = get_openrouter_headers()
        print(f"\n🔑 API key configured: {'✅' if headers else '❌'}")
    except ValueError as e:
        print(f"\n🔑 API key issue: {e}")
    
    print("\n🎯 Configuration ready for testing!")
