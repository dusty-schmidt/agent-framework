"""
Developer Agent - Specialized for software development tasks
"""

import logging
import asyncio
from typing import Dict, List
from core.base_agent import BaseAgent, AgentRequest, AgentResponse, AgentCapability
from agents.simple_gemini_bot import GeminiProvider

logger = logging.getLogger('DeveloperAgent')

class DeveloperAgent(BaseAgent):
    """
    Specialized agent for software development tasks including:
    - Code generation and review
    - Architecture planning
    - Debugging assistance
    - Technology recommendations
    """
    
    def __init__(self, gemini_provider: GeminiProvider):
        capabilities = [
            AgentCapability(
                name="Code Generation",
                description="Generate code in various programming languages",
                keywords=["code", "write", "create", "program", "function", "class", "script"],
                confidence_threshold=0.8
            ),
            AgentCapability(
                name="Code Review",
                description="Review and improve existing code",
                keywords=["review", "improve", "optimize", "refactor", "debug", "fix"],
                confidence_threshold=0.8
            ),
            AgentCapability(
                name="Architecture Design",
                description="Design software architecture and system design",
                keywords=["architecture", "design", "system", "structure", "pattern", "framework"],
                confidence_threshold=0.7
            ),
            AgentCapability(
                name="Technology Consultation",
                description="Recommend technologies and best practices",
                keywords=["technology", "framework", "library", "tool", "recommend", "best practice"],
                confidence_threshold=0.7
            ),
            AgentCapability(
                name="Debugging Support",
                description="Help debug and troubleshoot code issues",
                keywords=["debug", "error", "bug", "issue", "troubleshoot", "fix", "problem"],
                confidence_threshold=0.8
            )
        ]
        
        system_prompt = """You are a Senior Software Developer Agent with expertise across multiple programming languages and technologies.

Your specializations include:
- Code generation with best practices and proper documentation
- Code review focusing on performance, security, and maintainability
- Software architecture design following established patterns
- Technology recommendations based on project requirements
- Debugging and troubleshooting complex issues

Guidelines:
- Always provide working, tested code examples
- Include comments and documentation
- Consider security, performance, and maintainability
- Suggest appropriate design patterns when relevant
- Provide step-by-step explanations for complex concepts
- Include error handling and edge cases
- Recommend testing strategies

Be precise, professional, and focus on delivering production-ready solutions."""
        
        super().__init__(
            agent_id="developer",
            name="Developer Agent",
            capabilities=capabilities,
            system_prompt=system_prompt,
            memory_namespace="developer"
        )
        
        self.gemini_provider = gemini_provider
        
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process software development related requests"""
        
        try:
            # Build hierarchical prompt with development context
            full_prompt = self.get_hierarchical_prompt(request)
            
            # Get response from Gemini with developer-focused context
            response_content = await self.gemini_provider.chat(full_prompt, [])
            
            # Determine confidence based on request type
            confidence = self._calculate_confidence(request)
            
            # Update metrics
            self.update_metrics(success=True, confidence=confidence)
            
            return AgentResponse(
                request_id=request.id,
                content=response_content,
                agent_id=self.agent_id,
                confidence=confidence,
                reasoning=f"Processed development request using specialized knowledge",
                metadata={
                    'task_type': self._classify_dev_task(request.user_input),
                    'estimated_complexity': self._estimate_complexity(request.user_input)
                }
            )
            
        except Exception as e:
            self.logger.error(f"Developer agent processing failed: {e}")
            self.update_metrics(success=False, confidence=0.1)
            
            return AgentResponse(
                request_id=request.id,
                content=f"I encountered an error processing your development request: {str(e)}",
                agent_id=self.agent_id,
                confidence=0.1,
                reasoning=f"Error during processing: {str(e)}",
                success=False
            )
    
    def _calculate_confidence(self, request: AgentRequest) -> float:
        """Calculate confidence based on request characteristics"""
        base_confidence = self.can_handle(request)
        
        # Boost confidence for specific development keywords
        high_confidence_keywords = [
            'python', 'javascript', 'typescript', 'java', 'cpp', 'c++',
            'react', 'node', 'django', 'flask', 'api', 'database',
            'algorithm', 'data structure', 'object-oriented'
        ]
        
        user_input_lower = request.user_input.lower()
        keyword_matches = sum(1 for keyword in high_confidence_keywords 
                             if keyword in user_input_lower)
        
        # Increase confidence based on keyword matches
        confidence_boost = min(keyword_matches * 0.1, 0.3)
        
        return min(base_confidence + confidence_boost, 1.0)
    
    def _classify_dev_task(self, user_input: str) -> str:
        """Classify the type of development task"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['write', 'create', 'generate', 'build']):
            return "code_generation"
        elif any(word in user_input_lower for word in ['review', 'improve', 'optimize']):
            return "code_review"
        elif any(word in user_input_lower for word in ['debug', 'fix', 'error', 'bug']):
            return "debugging"
        elif any(word in user_input_lower for word in ['architecture', 'design', 'structure']):
            return "architecture"
        elif any(word in user_input_lower for word in ['recommend', 'choose', 'select']):
            return "consultation"
        else:
            return "general_development"
    
    def _estimate_complexity(self, user_input: str) -> str:
        """Estimate the complexity of the development task"""
        complexity_indicators = {
            'simple': ['hello world', 'basic', 'simple', 'quick', 'small'],
            'medium': ['function', 'class', 'module', 'component', 'feature'],
            'complex': ['system', 'architecture', 'framework', 'full application', 'enterprise']
        }
        
        user_input_lower = user_input.lower()
        
        for complexity, indicators in complexity_indicators.items():
            if any(indicator in user_input_lower for indicator in indicators):
                return complexity
        
        # Default to medium complexity
        return "medium"
    
    async def handle_consultation_request(self, agents: List[BaseAgent], request: AgentRequest) -> AgentResponse:
        """
        Handle complex development requests by consulting with multiple specialized agents.
        This implements the "consult" feature for challenging tasks.
        """
        
        consultation_agents = []
        
        # Determine which specialized agents to consult based on request
        user_input_lower = request.user_input.lower()
        
        if any(word in user_input_lower for word in ['microservice', 'distributed', 'scalable']):
            # Would consult microservices agent if it existed
            consultation_agents.append("microservices_agent")
        
        if any(word in user_input_lower for word in ['web', 'frontend', 'react', 'vue', 'angular']):
            # Would consult web development agent if it existed
            consultation_agents.append("web_development_agent")
        
        if any(word in user_input_lower for word in ['architecture', 'design pattern', 'system design']):
            # Would consult architecture agent if it existed
            consultation_agents.append("architecture_agent")
        
        # For now, return a comprehensive response acknowledging the consultation approach
        consultation_response = f"""
I've analyzed your complex development request and would normally consult with specialized agents:
{', '.join(consultation_agents) if consultation_agents else 'relevant specialists'}

For this request: "{request.user_input}"

I'll provide a comprehensive response drawing from multiple development perspectives:

{await self._generate_comprehensive_response(request)}
        """
        
        return AgentResponse(
            request_id=request.id,
            content=consultation_response.strip(),
            agent_id=self.agent_id,
            confidence=0.85,
            reasoning="Provided comprehensive multi-perspective development guidance",
            metadata={
                'consultation_type': 'multi_agent',
                'consulted_specialties': consultation_agents
            }
        )
    
    async def _generate_comprehensive_response(self, request: AgentRequest) -> str:
        """Generate a comprehensive response for complex development requests"""
        
        # This would normally coordinate with multiple agents
        # For now, we'll provide a structured response covering multiple angles
        
        perspectives = {
            'Architecture': "Consider scalability, maintainability, and performance requirements",
            'Implementation': "Focus on code quality, testing, and documentation", 
            'DevOps': "Plan for deployment, monitoring, and maintenance",
            'Security': "Implement proper authentication, authorization, and data protection"
        }
        
        response_parts = []
        for perspective, guidance in perspectives.items():
            response_parts.append(f"**{perspective} Perspective:** {guidance}")
        
        full_prompt = f"""
        {self.get_hierarchical_prompt(request)}
        
        Please provide a comprehensive response covering these perspectives:
        {chr(10).join(response_parts)}
        """
        
        return await self.gemini_provider.chat(full_prompt, [])
