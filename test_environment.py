#!/usr/bin/env python3
"""
Test script to verify the standardized environment setup.

This script tests:
1. Environment setup
2. Import resolution
3. Model configuration
4. Basic functionality
"""

import sys
from pathlib import Path

# Setup environment
from setup_environment import setup_project_environment
setup_project_environment()

def test_imports():
    """Test that all imports work correctly."""
    print("🧪 Testing imports...")
    
    try:
        from unified_memory.memory_interface import UnifiedMemoryItem, MemoryType
        print("   ✅ unified_memory imports working")
    except ImportError as e:
        print(f"   ❌ unified_memory import failed: {e}")
        return False
    
    try:
        from central_nervous_system.core.central_brain import CentralBrain
        print("   ✅ central_nervous_system imports working")
    except ImportError as e:
        print(f"   ❌ central_nervous_system import failed: {e}")
        return False
    
    try:
        from model_config import get_model_config, validate_model_name
        print("   ✅ model_config imports working")
    except ImportError as e:
        print(f"   ❌ model_config import failed: {e}")
        return False
    
    return True

def test_model_config():
    """Test model configuration."""
    print("\n🤖 Testing model configuration...")
    
    from model_config import get_model_config, validate_model_name, get_available_models
    
    # Test standard config
    config = get_model_config()
    print(f"   Default model: {config['model']}")
    print(f"   Provider: {config['provider']}")
    
    # Test tier configs
    for tier in ["node", "link", "mesh", "grid"]:
        tier_config = get_model_config(tier)
        print(f"   {tier} tier: {tier_config['model']} (temp={tier_config['temperature']})")
    
    # Test model name validation
    test_models = [
        "openai/gpt-oss-20b",  # Valid
        "anthropic/claude-3-haiku",  # Valid
        "invalid-model",  # Invalid
        "provider/model/extra"  # Invalid
    ]
    
    print("\n   Model name validation:")
    for model in test_models:
        valid = validate_model_name(model)
        status = "✅" if valid else "❌"
        print(f"     {status} {model}")
    
    return True

def test_memory_system():
    """Test basic memory system functionality."""
    print("\n💾 Testing memory system...")
    
    try:
        from unified_memory.memory_interface import UnifiedMemoryItem, MemoryType
        from unified_memory.storage.json_storage import JSONMemoryStorage
        import tempfile
        import asyncio
        
        async def test_memory():
            # Create temporary storage
            with tempfile.TemporaryDirectory() as temp_dir:
                storage = JSONMemoryStorage(temp_dir)
                
                # Create test memory item
                memory_item = UnifiedMemoryItem(
                    content="Test memory item",
                    memory_type=MemoryType.CONVERSATION,
                    tier_source="test_tier",
                    session_id="test_session"
                )
                
                # Save and retrieve
                memory_id = await storage.save(memory_item)
                retrieved = await storage.get_by_id(memory_id)
                
                if retrieved and retrieved.content == "Test memory item":
                    print("   ✅ Memory save/retrieve working")
                    return True
                else:
                    print("   ❌ Memory save/retrieve failed")
                    return False
        
        result = asyncio.run(test_memory())
        return result
        
    except Exception as e:
        print(f"   ❌ Memory system test failed: {e}")
        return False

def test_central_brain():
    """Test basic central brain functionality."""
    print("\n🧠 Testing central brain...")
    
    try:
        from central_nervous_system.core.central_brain import CentralBrain
        
        # Initialize central brain
        brain = CentralBrain()
        
        # Test tier registration
        brain.register_tier("test_tier", {
            "agent_type": "test",
            "version": "1.0.0",
            "capabilities": ["test"]
        })
        
        if "test_tier" in brain.connected_tiers:
            print("   ✅ Tier registration working")
            return True
        else:
            print("   ❌ Tier registration failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Central brain test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Agentic Framework Environment Test")
    print("=" * 50)
    
    # Test results
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Model Config", test_model_config()))
    results.append(("Memory System", test_memory_system()))
    results.append(("Central Brain", test_central_brain()))
    
    # Summary
    print("\n📊 Test Results:")
    print("-" * 30)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:15} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Environment is ready for development.")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} test(s) failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
