#!/usr/bin/env python3
"""
Configuration Validation Script

Validates the project configuration and environment setup.
This script will grow to include more validation checks over time.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.simple_env import setup_simple_env, get_api_key, get_model_name, get_log_level
from scripts.config_loader import get_api_config, get_tier_config

def validate_environment():
    """Validate environment setup."""
    print(">> Validating Environment")
    print("-" * 30)
    
    issues = []
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 11:
        print(f"[PASS] Python version: {python_version.major}.{python_version.minor}")
    else:
        issues.append(f"Python 3.11+ required, found {python_version.major}.{python_version.minor}")

    # Check API key
    try:
        api_key = get_api_key()
        print("[PASS] API key: Found")
    except ValueError as e:
        issues.append(str(e))

    # Check model configuration
    try:
        model = get_model_name()
        print(f"[PASS] Model: {model}")
    except Exception as e:
        issues.append(f"Model configuration error: {e}")

    # Check log level
    try:
        log_level = get_log_level()
        print(f"[PASS] Log level: {log_level}")
    except Exception as e:
        issues.append(f"Log level error: {e}")
    
    return issues

def validate_configuration():
    """Validate configuration files."""
    print("\n>> Validating Configuration")
    print("-" * 30)
    
    issues = []
    
    # Check config.toml exists
    config_file = Path(__file__).parent.parent / "config.toml"
    if config_file.exists():
        print("[PASS] config.toml: Found")
    else:
        issues.append("config.toml not found")
    
    # Check API configuration
    try:
        api_config = get_api_config()
        required_keys = ['provider', 'base_url', 'model', 'temperature']
        for key in required_keys:
            if key in api_config:
                print(f"[PASS] API config '{key}': {api_config[key]}")
            else:
                issues.append(f"Missing API config key: {key}")
    except Exception as e:
        issues.append(f"API configuration error: {e}")
    
    # Check tier configurations
    tiers = ['node', 'link', 'mesh', 'grid']
    for tier in tiers:
        try:
            tier_config = get_tier_config(tier)
            print(f"[PASS] {tier} tier config: OK")
        except Exception as e:
            issues.append(f"{tier} tier configuration error: {e}")
    
    return issues

def validate_directory_structure():
    """Validate project directory structure."""
    print("\n>>  Validating Directory Structure")
    print("-" * 35)
    
    issues = []
    project_root = Path(__file__).parent.parent
    
    required_dirs = [
        'core',
        'core/brain',
        'core/memory', 
        'core/config',
        'core/data',
        'tiers',
        'scripts',
        'tests',
        'docs',
        'docker'
    ]
    
    for dir_path in required_dirs:
        full_path = project_root / dir_path
        if full_path.exists():
            print(f"[PASS] {dir_path}/")
        else:
            issues.append(f"Missing directory: {dir_path}/")
    
    required_files = [
        'config.toml',
        'environment.yml',
        'requirements.txt',
        'README.md'
    ]
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"[PASS] {file_path}")
        else:
            issues.append(f"Missing file: {file_path}")
    
    return issues

def validate_imports():
    """Validate that core imports work."""
    print("\n>>  Validating Imports")
    print("-" * 20)
    
    issues = []
    
    try:
        from core.brain.central_brain import CentralBrain
        print("[PASS] Core brain imports")
    except ImportError as e:
        issues.append(f"Core brain import error: {e}")
    
    try:
        from core.memory.memory_interface import UnifiedMemoryItem
        print("[PASS] Core memory imports")
    except ImportError as e:
        issues.append(f"Core memory import error: {e}")
    
    try:
        import aiohttp
        print("[PASS] aiohttp")
    except ImportError:
        issues.append("aiohttp not installed")
    
    try:
        import toml
        print("[PASS] toml")
    except ImportError:
        issues.append("toml not installed")
    
    return issues

def main():
    """Main validation process."""
    print("AGENTIC FRAMEWORK - CONFIGURATION VALIDATION")
    print("=" * 55)
    
    # Setup environment
    try:
        setup_simple_env()
    except Exception as e:
        print(f"[FAIL] Environment setup failed: {e}")
        sys.exit(1)
    
    # Run all validations
    all_issues = []
    
    all_issues.extend(validate_environment())
    all_issues.extend(validate_configuration())
    all_issues.extend(validate_directory_structure())
    all_issues.extend(validate_imports())
    
    # Summary
    print("\n" + "=" * 55)
    print("VALIDATION SUMMARY")
    print("=" * 55)
    
    if not all_issues:
        print(">>  All validations passed!")
        print("[PASS] Configuration is valid and ready to use")
        return True
    else:
        print(f"[FAIL] Found {len(all_issues)} issue(s):")
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")
        print("\n>>   Please fix these issues before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
