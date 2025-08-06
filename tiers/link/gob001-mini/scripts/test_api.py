#!/usr/bin/env python3
# Filename: test_api.py
# Location: scripts/test_api.py

"""
Development script for testing API endpoints manually
Keep all test scripts organized here during development
"""

import asyncio
import httpx
import json
from datetime import datetime

class APITester:
    """Manual API testing utility"""
    
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
    
    async def test_chat_endpoint(self, message: str, session_id: str = "dev-test"):
        """Test chat endpoint with a message"""
        print(f"🔄 Testing chat: '{message}'")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json={"message": message, "sessionId": session_id}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Agent: {data['agent_used']}")
                    print(f"✅ Confidence: {data['confidence']:.2f}")
                    print(f"✅ Using fallback: {data['using_fallback']}")
                    print(f"✅ Reply: {data['reply'][:100]}...")
                    return data
                else:
                    print(f"❌ Error: {response.status_code} - {response.text}")
                    return None
                    
            except Exception as e:
                print(f"❌ Exception: {e}")
                return None
    
    async def test_health_endpoints(self):
        """Test all health endpoints"""
        print("🏥 Testing health endpoints...")
        
        endpoints = [
            "/api/health",
            "/api/health/llm/google", 
            "/api/health/llm/groq",
            "/api/health/llm"
        ]
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            for endpoint in endpoints:
                try:
                    print(f"🔄 Testing {endpoint}")
                    response = await client.get(f"{self.base_url}{endpoint}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        if "provider" in data:
                            print(f"✅ {data['provider']}: {data['status']}")
                        elif "overall_status" in data:
                            print(f"✅ Overall: {data['overall_status']}")
                        else:
                            print(f"✅ Status: {data.get('status', 'OK')}")
                    else:
                        print(f"❌ {endpoint}: {response.status_code}")
                        
                except Exception as e:
                    print(f"❌ {endpoint}: {e}")
    
    async def test_agent_routing(self):
        """Test different types of messages to verify agent routing"""
        print("🤖 Testing agent routing...")
        
        test_messages = [
            ("Hello, how are you?", "general"),
            ("Write a Python function to sort a list", "coding"),
            ("Explain quantum physics", "general"),
            ("Debug this JavaScript code: console.log('test')", "coding"),
            ("What's the weather like?", "general")
        ]
        
        for message, expected_type in test_messages:
            print(f"\n📝 Testing: {message}")
            result = await self.test_chat_endpoint(message)
            if result:
                agent = result.get('agent_used', 'unknown')
                confidence = result.get('confidence', 0)
                print(f"🎯 Expected: {expected_type}, Got: {agent}, Confidence: {confidence:.2f}")

async def main():
    """Main testing function"""
    print("🚀 Starting API Testing Session")
    print("=" * 50)
    
    tester = APITester()
    
    # Test health endpoints first
    await tester.test_health_endpoints()
    print("\n" + "=" * 50)
    
    # Test basic chat
    await tester.test_chat_endpoint("Hello! Can you help me with a simple test?")
    print("\n" + "=" * 50)
    
    # Test agent routing
    await tester.test_agent_routing()
    print("\n" + "=" * 50)
    
    print("✅ Testing session complete!")

if __name__ == "__main__":
    asyncio.run(main())
