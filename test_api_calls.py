#!/usr/bin/env python3
"""
Test script to validate actual API calls to OpenRouter.

This script tests:
1. API key configuration
2. Model availability
3. Actual API responses
4. Different tier configurations
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Setup environment
from setup_environment import setup_project_environment
setup_project_environment()

from model_config import (
    get_model_config, 
    get_openrouter_headers, 
    create_model_request_payload,
    TIER_MODEL_CONFIGS
)

try:
    import aiohttp
except ImportError:
    print("❌ aiohttp not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
    import aiohttp

async def test_api_connection():
    """Test basic API connection to OpenRouter."""
    print("🔌 Testing API connection...")
    
    try:
        headers = get_openrouter_headers()
        
        async with aiohttp.ClientSession() as session:
            # Test with a simple request to get models
            async with session.get(
                "https://openrouter.ai/api/v1/models",
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    models = data.get('data', [])
                    
                    # Check if our target model is available
                    target_model = "openai/gpt-oss-20b"
                    available_models = [model['id'] for model in models]
                    
                    if target_model in available_models:
                        print(f"   ✅ API connection successful")
                        print(f"   ✅ Target model '{target_model}' is available")
                        return True
                    else:
                        print(f"   ⚠️  API connection successful but '{target_model}' not found")
                        print(f"   Available models: {len(available_models)} total")
                        # Show first few available models
                        for model in available_models[:5]:
                            if "openai" in model or "gpt" in model:
                                print(f"      - {model}")
                        return False
                else:
                    print(f"   ❌ API connection failed: HTTP {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"   ❌ API connection test failed: {e}")
        return False

async def test_simple_completion():
    """Test a simple completion request."""
    print("\n💬 Testing simple completion...")
    
    try:
        headers = get_openrouter_headers()
        config = get_model_config("default")
        
        # Simple test message
        messages = [
            {"role": "user", "content": "Say 'Hello from the Agentic Framework!' and nothing else."}
        ]
        
        payload = create_model_request_payload(messages, "default")
        
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
                        print(f"   ✅ Completion successful")
                        print(f"   Response: {response_text}")
                        
                        # Check if response contains expected text
                        if "Hello from the Agentic Framework" in response_text:
                            print(f"   ✅ Response validation passed")
                            return True
                        else:
                            print(f"   ⚠️  Response validation failed - unexpected content")
                            return False
                    else:
                        print(f"   ❌ No choices in response")
                        return False
                else:
                    print(f"   ❌ Completion failed: HTTP {response.status}")
                    error_text = await response.text()
                    print(f"   Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"   ❌ Simple completion test failed: {e}")
        return False

async def test_tier_specific_calls():
    """Test API calls with tier-specific configurations."""
    print("\n🏗️ Testing tier-specific configurations...")
    
    results = {}
    
    for tier_name in ["node", "link", "mesh", "grid"]:
        print(f"\n   Testing {tier_name} tier...")
        
        try:
            headers = get_openrouter_headers()
            config = get_model_config(tier_name)
            
            # Tier-specific test message
            messages = [
                {
                    "role": "user", 
                    "content": f"You are a {tier_name} tier agent. Respond with exactly: 'I am {tier_name} tier ready!'"
                }
            ]
            
            payload = create_model_request_payload(messages, tier_name)
            
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
                            print(f"     ✅ {tier_name} tier response: {response_text}")
                            results[tier_name] = True
                        else:
                            print(f"     ❌ {tier_name} tier: No response")
                            results[tier_name] = False
                    else:
                        print(f"     ❌ {tier_name} tier failed: HTTP {response.status}")
                        results[tier_name] = False
                        
        except Exception as e:
            print(f"     ❌ {tier_name} tier test failed: {e}")
            results[tier_name] = False
    
    # Summary
    successful_tiers = sum(1 for success in results.values() if success)
    print(f"\n   Tier test results: {successful_tiers}/{len(results)} tiers successful")
    
    return successful_tiers == len(results)

async def test_conversation_flow():
    """Test a multi-turn conversation to validate context handling."""
    print("\n💭 Testing conversation flow...")
    
    try:
        headers = get_openrouter_headers()
        config = get_model_config("default")
        
        # Multi-turn conversation
        messages = [
            {"role": "user", "content": "My name is Alice. Remember this."},
            {"role": "assistant", "content": "Hello Alice! I'll remember your name."},
            {"role": "user", "content": "What is my name?"}
        ]
        
        payload = create_model_request_payload(messages, "default")
        
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
                        print(f"   ✅ Conversation response: {response_text}")
                        
                        # Check if the model remembered the name
                        if "Alice" in response_text:
                            print(f"   ✅ Context retention validated")
                            return True
                        else:
                            print(f"   ⚠️  Context retention failed - name not remembered")
                            return False
                    else:
                        print(f"   ❌ No response in conversation test")
                        return False
                else:
                    print(f"   ❌ Conversation test failed: HTTP {response.status}")
                    return False
                    
    except Exception as e:
        print(f"   ❌ Conversation flow test failed: {e}")
        return False

async def test_error_handling():
    """Test error handling with invalid requests."""
    print("\n🚨 Testing error handling...")
    
    try:
        headers = get_openrouter_headers()
        config = get_model_config("default")
        
        # Invalid request (empty messages)
        payload = {
            "model": config["model"],
            "messages": [],  # Invalid: empty messages
            "max_tokens": config["max_tokens"],
            "temperature": config["temperature"]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                config["base_url"] + "/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    print(f"   ✅ Error handling working - got expected error: HTTP {response.status}")
                    return True
                else:
                    print(f"   ⚠️  Expected error but got success")
                    return False
                    
    except Exception as e:
        print(f"   ✅ Error handling working - caught exception: {type(e).__name__}")
        return True

async def main():
    """Run all API tests."""
    print("🚀 Agentic Framework API Validation Test")
    print("=" * 50)
    
    # Check for API key first
    try:
        get_openrouter_headers()
        print("✅ OPENROUTER_API_KEY found")
    except ValueError as e:
        print(f"❌ {e}")
        print("\nTo fix this:")
        print("1. Get an API key from https://openrouter.ai/keys")
        print("2. Set it as an environment variable:")
        print("   export OPENROUTER_API_KEY='your-api-key-here'")
        return False
    
    # Test results
    results = []
    
    # Run tests
    results.append(("API Connection", await test_api_connection()))
    results.append(("Simple Completion", await test_simple_completion()))
    results.append(("Tier Configurations", await test_tier_specific_calls()))
    results.append(("Conversation Flow", await test_conversation_flow()))
    results.append(("Error Handling", await test_error_handling()))
    
    # Summary
    print("\n📊 API Test Results:")
    print("-" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} API tests passed")
    
    if passed == len(results):
        print("\n🎉 All API tests passed! OpenRouter integration is working correctly.")
        print(f"🤖 Model '{get_model_config()['model']}' is ready for use across all tiers.")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} API test(s) failed.")
        print("Please check your API key and network connection.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
