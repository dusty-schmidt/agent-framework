#!/usr/bin/env python3
"""
Simple test script for development.

Just loads .env and tests basic functionality. Perfect for development workflow.
"""

import asyncio
import sys
from pathlib import Path

# Simple environment setup
from simple_env import setup_simple_env, get_api_key, get_model_name, is_debug
setup_simple_env()

from model_config import get_model_config, create_model_request_payload, get_openrouter_headers

try:
    import aiohttp
except ImportError:
    print("Installing aiohttp...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
    import aiohttp

async def quick_api_test():
    """Quick test to verify API is working."""
    print("🧪 Quick API Test")
    print("-" * 20)
    
    try:
        # Test configuration
        config = get_model_config()
        print(f"Model: {config['model']}")
        print(f"Temperature: {config['temperature']}")
        
        # Test API key
        headers = get_openrouter_headers()
        print("✅ API key loaded")
        
        # Simple API call
        messages = [{"role": "user", "content": "Say 'API test successful!' and nothing else."}]
        payload = create_model_request_payload(messages)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                config["base_url"] + "/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        response_text = data['choices'][0]['message']['content']
                        print(f"✅ API Response: {response_text}")
                        return True
                    else:
                        print("❌ No response from API")
                        return False
                else:
                    error_text = await response.text()
                    print(f"❌ API Error ({response.status}): {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_imports():
    """Test that imports work."""
    print("\n📦 Import Test")
    print("-" * 15)
    
    try:
        from central_nervous_system.core.central_brain import CentralBrain
        print("✅ Central Brain import")
        
        from unified_memory.memory_interface import UnifiedMemoryItem
        print("✅ Memory interface import")
        
        # Quick functionality test
        brain = CentralBrain()
        brain.register_tier("test", {"capabilities": ["test"]})
        print("✅ Central Brain basic functionality")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

async def main():
    """Run simple tests."""
    print("🚀 Agentic Framework - Simple Development Test")
    print("=" * 50)
    
    # Check environment
    print(f"Model: {get_model_name()}")
    print(f"Debug: {is_debug()}")
    
    # Test imports first
    imports_ok = test_imports()
    
    # Test API if imports work
    api_ok = False
    if imports_ok:
        try:
            get_api_key()  # This will raise if no API key
            api_ok = await quick_api_test()
        except ValueError as e:
            print(f"\n🔑 API Key Issue: {e}")
            print("Create a .env file with OPENROUTER_API_KEY=your-key-here")
    
    # Summary
    print(f"\n📊 Results:")
    print(f"Imports: {'✅' if imports_ok else '❌'}")
    print(f"API:     {'✅' if api_ok else '❌'}")
    
    if imports_ok and api_ok:
        print("\n🎉 Everything working! Ready for development.")
        return True
    elif imports_ok:
        print("\n⚠️  Framework ready, just need API key for live testing.")
        return True
    else:
        print("\n❌ Issues found. Check the errors above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
