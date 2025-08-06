import json
import os

def load_config(path="config.json"):
    """Load configuration from JSON file and environment variables."""
    try:
        with open(path, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{path}' not found")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file: {e}")
    
    # Get API key from environment variable
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is required. "
            "Set it with: export GEMINI_API_KEY='your-api-key-here'"
        )
    
    config["api_key"] = api_key
    return config
