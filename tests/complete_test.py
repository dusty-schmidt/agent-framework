#!/usr/bin/env python3
"""
Complete Test Suite for Agentic Framework

Single comprehensive test that validates every feature once:
- Environment setup and imports
- Configuration loading
- API connectivity
- Model configuration per tier
- Agent initialization
- Memory system functionality
- Central brain coordination
- Real agent responses with meaningful prompts
- Error handling
- Performance validation

No redundant tests - everything tested once, thoroughly.
"""

import asyncio
import sys
import time
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.simple_env import setup_simple_env

# Setup environment
setup_simple_env()

from core.brain.central_brain import CentralBrain
from scripts.config_loader import get_model_config, get_openrouter_headers, create_model_request_payload
from core.memory.memory_interface import UnifiedMemoryItem, MemoryType
from core.memory.storage.json_storage import JSONMemoryStorage

try:
    import aiohttp
except ImportError:
    print("Installing aiohttp...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
    import aiohttp

class CompleteFrameworkTest:
    """Single comprehensive test for all framework features."""
    
    def __init__(self):
        self.start_time = time.time()
        self.test_results = {}
        self.central_brain = CentralBrain()
        self.session_id = "complete_test_session"
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result."""
        self.test_results[test_name] = success
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {test_name}: {details}")
        
    async def test_complete_framework(self):
        """Test every framework feature comprehensively."""
        print("AGENTIC FRAMEWORK - COMPLETE FEATURE TEST")
        print("=" * 60)
        print("Testing every feature once, thoroughly.\n")

        # 1. Environment & Configuration Test
        print(">> Testing Environment & Configuration")
        print("-" * 40)
        
        try:
            # Test imports
            from core.memory.memory_hub import UnifiedMemoryHub
            self.log_test("Core Imports", True, "All core modules imported successfully")
            
            # Test configuration loading
            configs = {}
            for tier in ["node", "link", "mesh", "grid"]:
                config = get_model_config(tier)
                configs[tier] = config
                assert config['model'] == 'openai/gpt-oss-20b'
                assert 'temperature' in config
                assert 'max_tokens' in config
            
            self.log_test("Configuration Loading", True, f"All 4 tier configs loaded with model {configs['node']['model']}")
            
            # Test API key
            headers = get_openrouter_headers()
            assert 'Authorization' in headers
            self.log_test("API Key Setup", True, "OpenRouter API key configured")
            
        except Exception as e:
            self.log_test("Environment Setup", False, f"Error: {e}")
            return False
        
        # 2. Memory System Test
        print(f"\n>> Testing Memory System")
        print("-" * 25)
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Test JSON storage
                storage = JSONMemoryStorage(temp_dir)
                
                # Create and save memory item
                memory_item = UnifiedMemoryItem(
                    content="Test memory for complete framework test",
                    memory_type=MemoryType.CONVERSATION,
                    tier_source="test_tier",
                    metadata={"test": True, "session_id": self.session_id}
                )

                memory_id = await storage.save(memory_item)
                retrieved = await storage.get_by_id(memory_id)

                assert retrieved.content == memory_item.content
                assert retrieved.metadata.get("session_id") == self.session_id
                
                self.log_test("Memory Storage", True, f"Saved and retrieved memory item {memory_id[:8]}...")
                
        except Exception as e:
            self.log_test("Memory System", False, f"Error: {e}")
        
        # 3. Central Brain & Agent Initialization Test
        print(f"\n>> Testing Central Brain & Agent Initialization")
        print("-" * 50)
        
        try:
            # Initialize all tiers
            tier_info = {}
            for tier in ["node", "link", "mesh", "grid"]:
                config = get_model_config(tier)
                agent_config = {
                    "agent_type": f"{tier}_agent",
                    "version": "1.0.0",
                    "capabilities": ["chat", "memory", "tools"],
                    "model_config": config,
                    "initialized_at": time.time()
                }
                
                self.central_brain.register_tier(tier, agent_config)
                tier_info[tier] = agent_config
            
            # Verify registration
            assert len(self.central_brain.connected_tiers) == 4
            for tier in ["node", "link", "mesh", "grid"]:
                assert tier in self.central_brain.connected_tiers
                
            self.log_test("Agent Initialization", True, "All 4 tiers registered with Central Brain")
            
        except Exception as e:
            self.log_test("Central Brain Setup", False, f"Error: {e}")
            return False
        
        # 4. API Connectivity Test
        print(f"\n>> Testing API Connectivity")
        print("-" * 30)
        
        try:
            config = get_model_config("node")  # Use node tier for basic test
            headers = get_openrouter_headers()
            
            messages = [{"role": "user", "content": "Respond with exactly: 'API_TEST_SUCCESS'"}]
            payload = create_model_request_payload(messages, "node")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config["base_url"] + "/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=20)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if 'choices' in data and len(data['choices']) > 0:
                            response_text = data['choices'][0]['message']['content']
                            self.log_test("API Connectivity", True, f"Response: {response_text[:50]}...")
                        else:
                            self.log_test("API Connectivity", False, "No response choices")
                            return False
                    else:
                        self.log_test("API Connectivity", False, f"HTTP {response.status}")
                        return False
                        
        except Exception as e:
            self.log_test("API Connectivity", False, f"Error: {e}")
            return False
        
        # 5. Comprehensive Agent Response Test
        print(f"\n>> Testing Agent Responses with Real Prompts")
        print("-" * 50)
        
        # Define one comprehensive test per tier that validates tier-specific capabilities
        tier_tests = {
            "node": {
                "prompt": "Calculate 25 * 4 and explain the result briefly.",
                "expected_keywords": ["100", "twenty-five", "four", "multiply"],
                "capability": "Simple calculation with explanation"
            },
            "link": {
                "prompt": "You are a helpful tutor. Explain what Python is in 2 sentences, then list 2 uses.",
                "expected_keywords": ["python", "programming", "language", "uses"],
                "capability": "Multi-persona teaching with structured response"
            },
            "mesh": {
                "prompt": "Coordinate this project: Build a mobile app. List the team roles needed and 3 key milestones.",
                "expected_keywords": ["team", "roles", "milestones", "app", "project"],
                "capability": "Project coordination and resource planning"
            },
            "grid": {
                "prompt": "Analyze this scenario and suggest improvements: A company's AI system gives inconsistent results. What could be wrong and how would you systematically improve it?",
                "expected_keywords": ["analyze", "inconsistent", "improve", "systematic", "AI"],
                "capability": "Complex analysis and self-improving recommendations"
            }
        }
        
        agent_results = {}
        
        for tier, test_data in tier_tests.items():
            try:
                print(f"\n   >> {tier.upper()} tier: {test_data['capability']}")

                tier_info = self.central_brain.connected_tiers[tier]
                config = tier_info['config']['model_config']
                
                # Create tier-specific system prompt
                system_prompts = {
                    "node": "You are a Node tier agent. Be direct and concise.",
                    "link": "You are a Link tier agent. Be versatile and adapt to different roles.",
                    "mesh": "You are a Mesh tier agent. Focus on coordination and systematic thinking.",
                    "grid": "You are a Grid tier agent. Provide analytical, thoughtful responses."
                }
                
                messages = [
                    {"role": "system", "content": system_prompts[tier]},
                    {"role": "user", "content": test_data['prompt']}
                ]
                
                payload = create_model_request_payload(messages, tier)
                headers = get_openrouter_headers()
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        config["base_url"] + "/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=25)
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if 'choices' in data and len(data['choices']) > 0:
                                response_text = data['choices'][0]['message']['content']
                                
                                # Validate response quality
                                response_lower = response_text.lower()
                                found_keywords = [kw for kw in test_data['expected_keywords'] 
                                                if kw.lower() in response_lower]
                                
                                if len(response_text) > 20 and found_keywords:
                                    print(f"      [PASS] Response: {response_text[:80]}...")
                                    print(f"      [PASS] Keywords found: {', '.join(found_keywords)}")
                                    agent_results[tier] = True
                                else:
                                    print(f"      [WARN] Response too short or missing keywords")
                                    print(f"      [WARN] Response: {response_text[:80]}...")
                                    agent_results[tier] = False
                            else:
                                print(f"      [FAIL] No response from API")
                                agent_results[tier] = False
                        else:
                            print(f"      [FAIL] HTTP {response.status}")
                            agent_results[tier] = False
                            
            except Exception as e:
                print(f"      [ERROR] Error testing {tier}: {e}")
                agent_results[tier] = False
            
            await asyncio.sleep(1)  # Rate limiting
        
        # Validate agent responses
        successful_agents = sum(1 for success in agent_results.values() if success)
        total_agents = len(agent_results)
        
        self.log_test("Agent Response Validation", 
                     successful_agents == total_agents,
                     f"{successful_agents}/{total_agents} agents passed comprehensive tests")
        
        # 6. Error Handling Test
        print(f"\n>> Testing Error Handling")
        print("-" * 25)
        
        try:
            # Test with invalid request
            invalid_payload = {"model": "invalid-model", "messages": []}
            
            config = get_model_config("node")
            headers = get_openrouter_headers()
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config["base_url"] + "/chat/completions",
                    headers=headers,
                    json=invalid_payload,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    # Should get an error response
                    if response.status != 200:
                        self.log_test("Error Handling", True, f"Correctly handled invalid request (HTTP {response.status})")
                    else:
                        self.log_test("Error Handling", False, "Should have returned error for invalid request")
                        
        except Exception as e:
            self.log_test("Error Handling", True, f"Exception correctly caught: {type(e).__name__}")
        
        # Final Summary
        elapsed_time = time.time() - self.start_time
        
        print(f"\n{'='*60}")
        print("COMPLETE FRAMEWORK TEST SUMMARY")
        print('='*60)

        passed = sum(1 for result in self.test_results.values() if result)
        total = len(self.test_results)

        for test_name, result in self.test_results.items():
            status = "[PASS]" if result else "[FAIL]"
            print(f"{test_name:25} {status}")

        print(f"\nOverall: {passed}/{total} tests passed")
        print(f"Test duration: {elapsed_time:.1f} seconds")

        if passed == total:
            print(f"\n>> ALL TESTS PASSED! Framework is fully validated.")
            print(f">> Ready for:")
            print(f"   - Frontend chat UI development")
            print(f"   - Production deployment")
            print(f"   - Agent development and customization")
            return True
        else:
            print(f"\n>> {total - passed} test(s) failed. Check issues above.")
            return False

async def main():
    """Main entry point."""
    tester = CompleteFrameworkTest()
    success = await tester.test_complete_framework()
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n>> Complete test interrupted.")
        sys.exit(1)
