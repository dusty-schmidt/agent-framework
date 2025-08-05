#!/usr/bin/env python3
"""
Comprehensive test suite for the Modular AI Backend API
Tests all endpoints and core functionality
"""

import asyncio
import json
import sys
import time
from typing import Dict, Any
import urllib.request
import urllib.parse
import websockets

# Test configuration
BASE_URL = "http://localhost:8080"
WS_URL = "ws://localhost:8080/ws/stream"

class APITester:
    def __init__(self):
        self.test_results = []
        self.memory_items = []
        
    def log(self, message: str, success: bool = True):
        """Log test results"""
        status = "✓" if success else "✗"
        print(f"{status} {message}")
        self.test_results.append({"message": message, "success": success})
        
    def make_request(self, endpoint: str, method: str = "GET", data: Dict[Any, Any] = None, headers: Dict[str, str] = None) -> Dict[Any, Any]:
        """Make HTTP request to API"""
        url = f"{BASE_URL}{endpoint}"
        
        if headers is None:
            headers = {"Content-Type": "application/json"}
            
        if data:
            data_bytes = json.dumps(data).encode('utf-8')
        else:
            data_bytes = None
            
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req) as response:
                return {
                    "status": response.status,
                    "data": json.loads(response.read().decode('utf-8'))
                }
        except urllib.error.HTTPError as e:
            return {
                "status": e.code,
                "data": json.loads(e.read().decode('utf-8')) if e.read() else {}
            }
        except Exception as e:
            return {"status": 0, "error": str(e)}
    
    def test_health_endpoint(self):
        """Test /health endpoint"""
        self.log("Testing health endpoint...")
        response = self.make_request("/health")
        
        if response["status"] == 200:
            data = response["data"]
            if "status" in data and data["status"] == "ok":
                self.log("Health endpoint returns OK status")
                if "audit" in data:
                    self.log("Health endpoint includes audit information")
                else:
                    self.log("Health endpoint missing audit information", False)
            else:
                self.log("Health endpoint invalid response format", False)
        else:
            self.log(f"Health endpoint failed with status {response['status']}", False)
    
    def test_memory_endpoints(self):
        """Test memory save and query endpoints"""
        self.log("Testing memory endpoints...")
        
        # Test memory save
        test_memory = {
            "type": "test_memory",
            "content": {"message": "Test memory item", "value": 42},
            "tags": ["test", "api"],
            "metadata": {"created_by": "test_suite"}
        }
        
        response = self.make_request("/memory/save", "POST", test_memory)
        if response["status"] == 200:
            memory_item = response["data"]
            if "id" in memory_item:
                self.memory_items.append(memory_item["id"])
                self.log("Memory save successful")
                
                # Verify saved data
                if (memory_item["type"] == test_memory["type"] and 
                    memory_item["content"] == test_memory["content"]):
                    self.log("Memory save data integrity verified")
                else:
                    self.log("Memory save data integrity failed", False)
            else:
                self.log("Memory save missing ID in response", False)
        else:
            self.log(f"Memory save failed with status {response['status']}", False)
        
        # Test memory query by type
        response = self.make_request("/memory/query?type=test_memory")
        if response["status"] == 200:
            data = response["data"]
            if "items" in data and len(data["items"]) > 0:
                self.log("Memory query by type successful")
                
                # Verify query result
                found_item = data["items"][0]
                if found_item["content"]["message"] == "Test memory item":
                    self.log("Memory query data integrity verified")
                else:
                    self.log("Memory query data integrity failed", False)
            else:
                self.log("Memory query returned no items", False)
        else:
            self.log(f"Memory query failed with status {response['status']}", False)
        
        # Test memory query by tag
        response = self.make_request("/memory/query?tag=test")
        if response["status"] == 200:
            data = response["data"]
            if "items" in data and len(data["items"]) > 0:
                self.log("Memory query by tag successful")
            else:
                self.log("Memory query by tag returned no items", False)
        else:
            self.log(f"Memory query by tag failed with status {response['status']}", False)
    
    def test_behavior_endpoints(self):
        """Test behavior adjustment endpoints"""
        self.log("Testing behavior endpoints...")
        
        # Test behavior adjustment
        test_rules = ["Be helpful and informative", "Respond concisely", "Verify data accuracy"]
        behavior_data = {"rules": test_rules, "scope": "test_scope"}
        
        response = self.make_request("/behavior/adjust", "POST", behavior_data)
        if response["status"] == 200:
            data = response["data"]
            if data.get("ok") and data.get("scope") == "test_scope":
                self.log("Behavior adjustment successful")
                
                # Verify rules were saved
                if set(data.get("rules", [])) >= set(test_rules):
                    self.log("Behavior rules saved correctly")
                else:
                    self.log("Behavior rules not saved correctly", False)
            else:
                self.log("Behavior adjustment invalid response", False)
        else:
            self.log(f"Behavior adjustment failed with status {response['status']}", False)
        
        # Test behavior retrieval
        response = self.make_request("/behavior?scope=test_scope")
        if response["status"] == 200:
            data = response["data"]
            if data.get("scope") == "test_scope" and "rules" in data:
                self.log("Behavior retrieval successful")
                
                # Verify retrieved rules
                if set(data["rules"]) >= set(test_rules):
                    self.log("Behavior retrieval data integrity verified")
                else:
                    self.log("Behavior retrieval data integrity failed", False)
            else:
                self.log("Behavior retrieval invalid response", False)
        else:
            self.log(f"Behavior retrieval failed with status {response['status']}", False)
    
    def test_agent_run_endpoint(self):
        """Test agent run endpoint"""
        self.log("Testing agent run endpoint...")
        
        agent_request = {
            "instruction": "Test agent execution",
            "tools": ["test_tool"],
            "timeout_ms": 5000
        }
        
        response = self.make_request("/agents/run", "POST", agent_request)
        if response["status"] == 200:
            data = response["data"]
            if "run_id" in data and "status" in data:
                self.log("Agent run endpoint successful")
                
                if data["status"] == "started":
                    self.log("Agent run status correct")
                else:
                    self.log(f"Agent run unexpected status: {data['status']}", False)
            else:
                self.log("Agent run missing required fields", False)
        else:
            self.log(f"Agent run failed with status {response['status']}", False)
    
    async def test_websocket_functionality(self):
        """Test WebSocket connection and events"""
        self.log("Testing WebSocket functionality...")
        
        try:
            async with websockets.connect(WS_URL) as websocket:
                self.log("WebSocket connection established")
                
                # Trigger an agent run to generate events
                agent_request = {"instruction": "WebSocket test run"}
                response = self.make_request("/agents/run", "POST", agent_request)
                
                if response["status"] == 200:
                    run_id = response["data"]["run_id"]
                    self.log("Agent run triggered for WebSocket test")
                    
                    # Collect WebSocket messages
                    messages = []
                    try:
                        for _ in range(3):  # Expect 3 messages from the mock agent
                            message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                            messages.append(json.loads(message))
                        
                        self.log(f"Received {len(messages)} WebSocket messages")
                        
                        # Verify message structure
                        for i, msg in enumerate(messages):
                            required_fields = ["id", "ts", "type", "source", "correlation_id", "seq", "payload"]
                            if all(field in msg for field in required_fields):
                                self.log(f"WebSocket message {i+1} structure valid")
                                
                                # Verify payload contains run_id
                                if msg["payload"].get("run_id") == run_id:
                                    self.log(f"WebSocket message {i+1} run_id matches")
                                else:
                                    self.log(f"WebSocket message {i+1} run_id mismatch", False)
                            else:
                                self.log(f"WebSocket message {i+1} structure invalid", False)
                    
                    except asyncio.TimeoutError:
                        self.log("WebSocket message timeout", False)
                else:
                    self.log("Failed to trigger agent run for WebSocket test", False)
                    
        except Exception as e:
            self.log(f"WebSocket test failed: {str(e)}", False)
    
    def test_error_handling(self):
        """Test error handling for invalid requests"""
        self.log("Testing error handling...")
        
        # Test invalid endpoint
        response = self.make_request("/invalid/endpoint")
        if response["status"] == 404:
            self.log("404 error handling works")
        else:
            self.log(f"Expected 404, got {response['status']}", False)
        
        # Test invalid JSON for memory save
        try:
            req = urllib.request.Request(f"{BASE_URL}/memory/save", 
                                       data=b"invalid json", 
                                       headers={"Content-Type": "application/json"}, 
                                       method="POST")
            with urllib.request.urlopen(req) as response:
                self.log("Invalid JSON should have failed", False)
        except urllib.error.HTTPError as e:
            if e.code in [400, 422]:  # Bad request or validation error
                self.log("Invalid JSON error handling works")
            else:
                self.log(f"Unexpected error code for invalid JSON: {e.code}", False)
        except Exception as e:
            self.log(f"Unexpected error for invalid JSON: {str(e)}", False)
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Modular AI Backend API Test Suite")
        print("=" * 50)
        
        # Run synchronous tests
        self.test_health_endpoint()
        self.test_memory_endpoints()
        self.test_behavior_endpoints()
        self.test_agent_run_endpoint()
        self.test_error_handling()
        
        # Run asynchronous WebSocket test
        await self.test_websocket_functionality()
        
        # Print summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ Failed tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['message']}")
        
        return failed_tests == 0

async def main():
    """Main test runner"""
    tester = APITester()
    
    # Check if server is running
    try:
        response = tester.make_request("/health")
        if response["status"] != 200:
            print("❌ Server is not running or not responding. Please start the server first.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Cannot connect to server: {str(e)}")
        print("Please make sure the server is running on http://localhost:8080")
        sys.exit(1)
    
    # Run tests
    success = await tester.run_all_tests()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
