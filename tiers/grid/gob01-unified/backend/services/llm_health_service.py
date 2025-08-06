# Filename: llm_health_service.py
# Location: backend/services/llm_health_service.py

import os
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

import httpx
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv(".env")

logger = logging.getLogger(__name__)

class ProviderStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class HealthCheckResult:
    provider: str
    status: ProviderStatus
    response_time_ms: Optional[float]
    error_message: Optional[str]
    model_used: str
    timestamp: datetime

class LLMHealthService:
    """Service for checking health of various LLM providers"""
    
    def __init__(self):
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_AI_STUDIO_API_KEY')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_api_key = os.getenv('OPEN_AI_API_KEY')
        
    async def check_openrouter_health(self) -> HealthCheckResult:
        """Check OpenRouter API health"""
        start_time = datetime.now()
        
        if not self.openrouter_api_key:
            return HealthCheckResult(
                provider="openrouter",
                status=ProviderStatus.UNHEALTHY,
                response_time_ms=None,
                error_message="API key not configured",
                model_used="N/A",
                timestamp=start_time
            )
        
        try:
            # Test with a simple model
            llm = ChatOpenAI(
                model="meta-llama/llama-3.2-3b-instruct:free",
                openai_api_key=self.openrouter_api_key,
                openai_api_base="https://openrouter.ai/api/v1",
                temperature=0.1,
                max_tokens=10
            )
            
            # Simple test message
            messages = [HumanMessage(content="Hello")]
            response = await llm.agenerate([messages])
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000
            
            return HealthCheckResult(
                provider="openrouter",
                status=ProviderStatus.HEALTHY,
                response_time_ms=response_time,
                error_message=None,
                model_used="meta-llama/llama-3.2-3b-instruct:free",
                timestamp=start_time
            )
            
        except Exception as e:
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000
            
            return HealthCheckResult(
                provider="openrouter",
                status=ProviderStatus.UNHEALTHY,
                response_time_ms=response_time,
                error_message=str(e),
                model_used="meta-llama/llama-3.2-3b-instruct:free",
                timestamp=start_time
            )
    
    async def check_google_health(self) -> HealthCheckResult:
        """Check Google AI Studio health"""
        start_time = datetime.now()
        
        if not self.google_api_key:
            return HealthCheckResult(
                provider="google",
                status=ProviderStatus.UNHEALTHY,
                response_time_ms=None,
                error_message="API key not configured",
                model_used="N/A",
                timestamp=start_time
            )
        
        try:
            # Test with Gemini model
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite",
                google_api_key=self.google_api_key,
                temperature=0.1,
                max_output_tokens=10,
                convert_system_message_to_human=True
            )
            
            # Simple test message
            messages = [HumanMessage(content="Hello")]
            response = await llm.agenerate([messages])
            
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000
            
            return HealthCheckResult(
                provider="google",
                status=ProviderStatus.HEALTHY,
                response_time_ms=response_time,
                error_message=None,
                model_used="gemini-2.0-flash-lite",
                timestamp=start_time
            )
            
        except Exception as e:
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000
            
            return HealthCheckResult(
                provider="google",
                status=ProviderStatus.UNHEALTHY,
                response_time_ms=response_time,
                error_message=str(e),
                model_used="gemini-2.0-flash-lite",
                timestamp=start_time
            )

    async def check_groq_health(self) -> HealthCheckResult:
        """Check GROQ API health"""
        start_time = datetime.now()

        if not self.groq_api_key:
            return HealthCheckResult(
                provider="groq",
                status=ProviderStatus.UNHEALTHY,
                response_time_ms=None,
                error_message="API key not configured",
                model_used="N/A",
                timestamp=start_time
            )

        try:
            # Test with a fast GROQ model
            llm = ChatGroq(
                model="llama3-8b-8192",
                groq_api_key=self.groq_api_key,
                temperature=0.1,
                max_tokens=10
            )

            # Simple test message
            messages = [HumanMessage(content="Hello")]
            response = await llm.agenerate([messages])

            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000

            return HealthCheckResult(
                provider="groq",
                status=ProviderStatus.HEALTHY,
                response_time_ms=response_time,
                error_message=None,
                model_used="llama3-8b-8192",
                timestamp=start_time
            )

        except Exception as e:
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000

            return HealthCheckResult(
                provider="groq",
                status=ProviderStatus.UNHEALTHY,
                response_time_ms=response_time,
                error_message=str(e),
                model_used="llama3-8b-8192",
                timestamp=start_time
            )

    async def check_anthropic_health(self) -> HealthCheckResult:
        """Check Anthropic API health"""
        start_time = datetime.now()

        if not self.anthropic_api_key:
            return HealthCheckResult(
                provider="anthropic",
                status=ProviderStatus.UNHEALTHY,
                response_time_ms=None,
                error_message="API key not configured",
                model_used="N/A",
                timestamp=start_time
            )

        try:
            # Test with Claude model
            llm = ChatAnthropic(
                model="claude-3-haiku-20240307",
                anthropic_api_key=self.anthropic_api_key,
                temperature=0.1,
                max_tokens=10
            )

            # Simple test message
            messages = [HumanMessage(content="Hello")]
            response = await llm.agenerate([messages])

            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000

            return HealthCheckResult(
                provider="anthropic",
                status=ProviderStatus.HEALTHY,
                response_time_ms=response_time,
                error_message=None,
                model_used="claude-3-haiku-20240307",
                timestamp=start_time
            )

        except Exception as e:
            end_time = datetime.now()
            response_time = (end_time - start_time).total_seconds() * 1000

            return HealthCheckResult(
                provider="anthropic",
                status=ProviderStatus.UNHEALTHY,
                response_time_ms=response_time,
                error_message=str(e),
                model_used="claude-3-haiku-20240307",
                timestamp=start_time
            )

    async def check_all_providers(self) -> List[HealthCheckResult]:
        """Check health of all configured providers"""
        tasks = [
            self.check_openrouter_health(),
            self.check_google_health(),
            self.check_groq_health(),
            self.check_anthropic_health()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions in the gather
        health_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                provider_name = ["openrouter", "google"][i]
                health_results.append(HealthCheckResult(
                    provider=provider_name,
                    status=ProviderStatus.UNHEALTHY,
                    response_time_ms=None,
                    error_message=f"Health check failed: {str(result)}",
                    model_used="N/A",
                    timestamp=datetime.now()
                ))
            else:
                health_results.append(result)
        
        return health_results
    
    def format_health_response(self, results: List[HealthCheckResult]) -> Dict[str, Any]:
        """Format health check results for API response"""
        overall_healthy = all(r.status == ProviderStatus.HEALTHY for r in results)
        
        return {
            "overall_status": "healthy" if overall_healthy else "degraded",
            "timestamp": datetime.now().isoformat(),
            "providers": {
                result.provider: {
                    "status": result.status.value,
                    "response_time_ms": result.response_time_ms,
                    "error_message": result.error_message,
                    "model_used": result.model_used,
                    "last_checked": result.timestamp.isoformat()
                }
                for result in results
            },
            "summary": {
                "total_providers": len(results),
                "healthy_providers": sum(1 for r in results if r.status == ProviderStatus.HEALTHY),
                "unhealthy_providers": sum(1 for r in results if r.status == ProviderStatus.UNHEALTHY)
            }
        }

# Global health service instance
health_service = LLMHealthService()
