# Filename: test_health_endpoints.py
# Location: tests/test_health_endpoints.py

"""
Test suite for health check endpoints
"""

import pytest
import httpx
import asyncio
from typing import Dict, Any

class TestHealthEndpoints:
    """Test class for health check endpoints"""
    
    BASE_URL = "http://localhost:8001"
    
    @pytest.mark.asyncio
    async def test_basic_health_check(self):
        """Test basic API health endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/api/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "timestamp" in data
            assert data["service"] == "Agentic Framework API"
    
    @pytest.mark.asyncio
    async def test_google_health_check(self):
        """Test Google AI Studio health endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/api/health/llm/google")
            assert response.status_code == 200
            data = response.json()
            assert data["provider"] == "google"
            assert data["model_used"] == "gemini-2.0-flash-lite"
            assert "response_time_ms" in data
    
    @pytest.mark.asyncio
    async def test_groq_health_check(self):
        """Test GROQ health endpoint"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/api/health/llm/groq")
            assert response.status_code == 200
            data = response.json()
            assert data["provider"] == "groq"
            assert data["model_used"] == "llama3-8b-8192"
    
    @pytest.mark.asyncio
    async def test_comprehensive_health_check(self):
        """Test comprehensive health check for all providers"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}/api/health/llm")
            assert response.status_code == 200
            data = response.json()
            assert "overall_status" in data
            assert "providers" in data
            assert "summary" in data
            assert data["summary"]["total_providers"] >= 2
    
    @pytest.mark.asyncio
    async def test_invalid_provider(self):
        """Test health check with invalid provider"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.BASE_URL}/api/health/llm/invalid")
            assert response.status_code == 404
            data = response.json()
            assert "not found" in data["detail"].lower()

if __name__ == "__main__":
    # Simple test runner for development
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    
    async def run_tests():
        test_instance = TestHealthEndpoints()
        print("🧪 Running health endpoint tests...")
        
        try:
            await test_instance.test_basic_health_check()
            print("✅ Basic health check passed")
            
            await test_instance.test_google_health_check()
            print("✅ Google health check passed")
            
            await test_instance.test_groq_health_check()
            print("✅ GROQ health check passed")
            
            await test_instance.test_comprehensive_health_check()
            print("✅ Comprehensive health check passed")
            
            await test_instance.test_invalid_provider()
            print("✅ Invalid provider test passed")
            
            print("🎉 All tests passed!")
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return False
        
        return True
    
    if __name__ == "__main__":
        asyncio.run(run_tests())
