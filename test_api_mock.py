#!/usr/bin/env python3
"""
Mock API test to validate framework functionality without requiring actual API calls.

This script simulates OpenRouter API responses to test:
1. Request payload generation
2. Response handling
3. Tier-specific configurations
4. Error handling
"""

import asyncio
import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

# Setup environment
from setup_environment import setup_project_environment
setup_project_environment()

from model_config import (
    get_model_config, 
    create_model_request_payload,
    validate_model_name,
    TIER_MODEL_CONFIGS
)

class MockOpenRouterAPI:
    """Mock OpenRouter API for testing."""
    
    def __init__(self):
        self.call_count = 0
        self.last_request = None
    
    async def mock_chat_completion(self, payload):
        """Mock chat completion response."""
        self.call_count += 1
        self.last_request = payload
        
        # Simulate different responses based on input
        messages = payload.get('messages', [])
        if not messages:
            # Simulate error for empty messages
            return {
                "error": {
                    "message": "Messages array cannot be empty",
                    "type": "invalid_request_error"
                }
            }, 400
        
        last_message = messages[-1].get('content', '')
        
        # Generate appropriate mock response
        if "Hello from the Agentic Framework" in last_message:
            response_text = "Hello from the Agentic Framework!"
        elif "tier agent" in last_message:
            # Extract tier name from message
            for tier in ["node", "link", "mesh", "grid"]:
                if tier in last_message:
                    response_text = f"I am {tier} tier ready!"
                    break
            else:
                response_text = "I am a tier agent ready!"
        elif "My name is Alice" in last_message:
            response_text = "Hello Alice! I'll remember your name."
        elif "What is my name" in last_message:
            response_text = "Your name is Alice."
        else:
            response_text = f"Mock response to: {last_message[:50]}..."
        
        return {
            "id": f"chatcmpl-mock-{self.call_count}",
            "object": "chat.completion",
            "created": 1234567890,
            "model": payload.get('model', 'openai/gpt-oss-20b'),
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": response_text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        }, 200

def test_model_configuration():
    """Test model configuration generation."""
    print("🤖 Testing model configuration...")
    
    # Test default config
    default_config = get_model_config()
    assert default_config['model'] == 'openai/gpt-oss-20b'
    assert default_config['provider'] == 'openrouter'
    print("   ✅ Default configuration correct")
    
    # Test tier-specific configs
    for tier in ["node", "link", "mesh", "grid"]:
        config = get_model_config(tier)
        assert config['model'] == 'openai/gpt-oss-20b'
        assert 'temperature' in config
        assert 'max_tokens' in config
        print(f"   ✅ {tier} tier configuration correct")
    
    # Test model name validation
    assert validate_model_name('openai/gpt-oss-20b') == True
    assert validate_model_name('invalid-model') == False
    print("   ✅ Model name validation working")
    
    return True

def test_request_payload_generation():
    """Test API request payload generation."""
    print("\n📦 Testing request payload generation...")
    
    messages = [
        {"role": "user", "content": "Test message"}
    ]
    
    # Test default payload
    payload = create_model_request_payload(messages)
    assert payload['model'] == 'openai/gpt-oss-20b'
    assert payload['messages'] == messages
    assert 'max_tokens' in payload
    assert 'temperature' in payload
    print("   ✅ Default payload generation correct")
    
    # Test tier-specific payloads
    for tier in ["node", "link", "mesh", "grid"]:
        tier_payload = create_model_request_payload(messages, tier)
        tier_config = get_model_config(tier)
        
        assert tier_payload['model'] == tier_config['model']
        assert tier_payload['temperature'] == tier_config['temperature']
        assert tier_payload['max_tokens'] == tier_config['max_tokens']
        print(f"   ✅ {tier} tier payload correct")
    
    # Test payload overrides
    override_payload = create_model_request_payload(
        messages, 
        "default", 
        {"temperature": 0.9, "max_tokens": 500}
    )
    assert override_payload['temperature'] == 0.9
    assert override_payload['max_tokens'] == 500
    print("   ✅ Payload overrides working")
    
    return True

async def test_mock_api_responses():
    """Test mock API responses."""
    print("\n🎭 Testing mock API responses...")
    
    mock_api = MockOpenRouterAPI()
    
    # Test simple completion
    payload = create_model_request_payload([
        {"role": "user", "content": "Say 'Hello from the Agentic Framework!' and nothing else."}
    ])
    
    response, status = await mock_api.mock_chat_completion(payload)
    assert status == 200
    assert 'choices' in response
    assert "Hello from the Agentic Framework" in response['choices'][0]['message']['content']
    print("   ✅ Simple completion mock working")
    
    # Test tier-specific responses
    for tier in ["node", "link", "mesh", "grid"]:
        tier_payload = create_model_request_payload([
            {"role": "user", "content": f"You are a {tier} tier agent. Respond with exactly: 'I am {tier} tier ready!'"}
        ], tier)
        
        response, status = await mock_api.mock_chat_completion(tier_payload)
        assert status == 200
        assert f"I am {tier} tier ready!" in response['choices'][0]['message']['content']
        print(f"   ✅ {tier} tier mock response correct")
    
    # Test conversation flow
    conversation_payload = create_model_request_payload([
        {"role": "user", "content": "My name is Alice. Remember this."},
        {"role": "assistant", "content": "Hello Alice! I'll remember your name."},
        {"role": "user", "content": "What is my name?"}
    ])
    
    response, status = await mock_api.mock_chat_completion(conversation_payload)
    assert status == 200
    assert "Alice" in response['choices'][0]['message']['content']
    print("   ✅ Conversation flow mock working")
    
    # Test error handling
    error_payload = create_model_request_payload([])  # Empty messages
    response, status = await mock_api.mock_chat_completion(error_payload)
    assert status == 400
    assert 'error' in response
    print("   ✅ Error handling mock working")
    
    print(f"   📊 Total API calls made: {mock_api.call_count}")
    
    return True

async def test_integration_simulation():
    """Test integration with central nervous system components."""
    print("\n🧠 Testing integration simulation...")
    
    try:
        from central_nervous_system.core.central_brain import CentralBrain
        
        # Initialize central brain
        brain = CentralBrain()
        
        # Register test tiers
        for tier in ["node", "link", "mesh", "grid"]:
            brain.register_tier(tier, {
                "agent_type": "test",
                "version": "1.0.0",
                "capabilities": ["chat", "memory"],
                "model_config": get_model_config(tier)
            })
        
        # Verify tier registration
        assert len(brain.connected_tiers) == 4
        print("   ✅ All tiers registered with Central Brain")
        
        # Test model config retrieval for each tier
        for tier in brain.connected_tiers:
            tier_info = brain.connected_tiers[tier]
            assert 'model_config' in tier_info['config']
            model_config = tier_info['config']['model_config']
            assert model_config['model'] == 'openai/gpt-oss-20b'
            print(f"   ✅ {tier} tier model config accessible")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Integration simulation failed: {e}")
        return False

async def main():
    """Run all mock tests."""
    print("🚀 Agentic Framework Mock API Test")
    print("=" * 50)
    print("This test validates the framework without requiring actual API calls.")
    print()
    
    # Test results
    results = []
    
    # Run tests
    results.append(("Model Configuration", test_model_configuration()))
    results.append(("Request Payload Generation", test_request_payload_generation()))
    results.append(("Mock API Responses", await test_mock_api_responses()))
    results.append(("Integration Simulation", await test_integration_simulation()))
    
    # Summary
    print("\n📊 Mock Test Results:")
    print("-" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} mock tests passed")
    
    if passed == len(results):
        print("\n🎉 All mock tests passed!")
        print("🤖 Framework is ready for OpenRouter integration.")
        print("📝 To test with real API calls:")
        print("   1. Get API key from https://openrouter.ai/keys")
        print("   2. Set: export OPENROUTER_API_KEY='your-key'")
        print("   3. Run: python test_api_calls.py")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} mock test(s) failed.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
