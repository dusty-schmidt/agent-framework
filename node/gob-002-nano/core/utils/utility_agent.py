"""
Utility Agent - LangChain-like flow for information processing and summarization.
Handles successful prompt/response summarization and embedding into memory.
"""

import logging
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

from core.base_agent import BaseAgent, AgentRequest, AgentResponse, AgentCapability
from tools.embed_memory import VectorMemory

logger = logging.getLogger('UtilityAgent')

@dataclass
class InteractionSummary:
    """Structured summary of successful interactions"""
    timestamp: str
    user_intent: str
    agent_response: str
    success_indicators: List[str]
    key_concepts: List[str]
    confidence: float
    response_quality: float

class UtilityAgent(BaseAgent):
    """
    Utility Agent for managing information flow throughout the system.
    - Summarizes successful interactions
    - Embeds summaries into memory for future reference
    - Manages context flow between agents
    - Provides relevance scoring for memory retrieval
    """
    
    def __init__(self, memory: VectorMemory):
        capabilities = [
            AgentCapability(
                name="Information Summarization",
                description="Summarize and process successful interactions",
                keywords=["summarize", "process", "embed", "memory"],
                confidence_threshold=0.9
            ),
            AgentCapability(
                name="Context Management", 
                description="Manage context flow between agents",
                keywords=["context", "flow", "information", "relevant"],
                confidence_threshold=0.8
            )
        ]
        
        system_prompt = """You are a Utility Agent responsible for information flow management.
        Your primary functions:
        1. Analyze successful interactions and create meaningful summaries
        2. Extract key concepts and relationships from conversations
        3. Determine relevance of past experiences to current requests
        4. Maintain high-quality memory embeddings for future reference
        
        Be precise, analytical, and focus on extracting actionable insights."""
        
        super().__init__(
            agent_id="utility",
            name="Utility Agent",
            capabilities=capabilities,
            system_prompt=system_prompt,
            memory_namespace="utility"
        )
        
        self.memory = memory
        self.interaction_history = []
        
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Process utility requests like summarization and context management"""
        
        user_input_lower = request.user_input.lower()
        
        if "summarize" in user_input_lower:
            return await self._handle_summarization(request)
        elif "context" in user_input_lower or "relevant" in user_input_lower:
            return await self._handle_context_retrieval(request)
        else:
            return await self._generic_utility_response(request)
    
    async def _handle_summarization(self, request: AgentRequest) -> AgentResponse:
        """Handle summarization requests"""
        try:
            # Extract interaction data from request context
            interaction_data = request.context.get('interaction_data', {})
            
            summary = await self.create_interaction_summary(
                user_input=interaction_data.get('user_input', ''),
                agent_response=interaction_data.get('agent_response', ''),
                success_metrics=interaction_data.get('success_metrics', {})
            )
            
            # Store summary in memory
            await self.store_summary(summary)
            
            return AgentResponse(
                request_id=request.id,
                content=f"Successfully summarized and stored interaction. Key concepts: {', '.join(summary.key_concepts)}",
                agent_id=self.agent_id,
                confidence=0.95,
                reasoning="Processed interaction data and created structured summary"
            )
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return AgentResponse(
                request_id=request.id,
                content="Failed to process summarization request",
                agent_id=self.agent_id,
                confidence=0.1,
                reasoning=f"Error during summarization: {str(e)}",
                success=False
            )
    
    async def _handle_context_retrieval(self, request: AgentRequest) -> AgentResponse:
        """Handle context retrieval requests"""
        try:
            query = request.context.get('query', request.user_input)
            
            # Retrieve relevant context from memory
            relevant_memories = self.memory.semantic_search(query, top_k=5)
            
            # Format context for use by other agents
            context_summary = await self.format_context_for_agents(relevant_memories, query)
            
            return AgentResponse(
                request_id=request.id,
                content=context_summary,
                agent_id=self.agent_id,
                confidence=0.9,
                reasoning=f"Retrieved {len(relevant_memories)} relevant memories for context",
                metadata={'relevant_memories': relevant_memories}
            )
        except Exception as e:
            logger.error(f"Context retrieval failed: {e}")
            return AgentResponse(
                request_id=request.id,
                content="No relevant context found",
                agent_id=self.agent_id,
                confidence=0.2,
                reasoning=f"Error during context retrieval: {str(e)}",
                success=False
            )
    
    async def create_interaction_summary(self, 
                                       user_input: str, 
                                       agent_response: str, 
                                       success_metrics: Dict) -> InteractionSummary:
        """Create a structured summary of a successful interaction"""
        
        # Extract user intent using simple keyword analysis
        # In production, this would use more sophisticated NLP
        intent_keywords = {
            'question': ['what', 'how', 'why', 'when', 'where', 'who'],
            'request': ['please', 'can you', 'could you', 'help me'],
            'command': ['create', 'make', 'build', 'generate', 'write'],
            'calculation': ['calculate', 'compute', 'solve', 'math'],
            'search': ['find', 'search', 'look up', 'information about']
        }
        
        user_intent = "general"
        for intent, keywords in intent_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                user_intent = intent
                break
        
        # Extract key concepts (simplified approach)
        key_concepts = []
        words = user_input.lower().split()
        # Filter out common words and keep potentially meaningful ones
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        for word in words:
            if len(word) > 3 and word not in stop_words:
                key_concepts.append(word)
        
        # Keep only unique concepts, max 5
        key_concepts = list(set(key_concepts))[:5]
        
        # Determine success indicators
        success_indicators = []
        if success_metrics.get('confidence', 0) > 0.7:
            success_indicators.append("high_confidence")
        if success_metrics.get('user_satisfaction', 0) > 0.8:
            success_indicators.append("user_satisfied")
        if len(agent_response) > 50:
            success_indicators.append("detailed_response")
        
        summary = InteractionSummary(
            timestamp=datetime.now().isoformat(),
            user_intent=user_intent,
            agent_response=agent_response[:200] + "..." if len(agent_response) > 200 else agent_response,
            success_indicators=success_indicators,
            key_concepts=key_concepts,
            confidence=success_metrics.get('confidence', 0.5),
            response_quality=success_metrics.get('response_quality', 0.5)
        )
        
        self.interaction_history.append(summary)
        logger.info(f"Created interaction summary with intent: {user_intent}, concepts: {key_concepts}")
        
        return summary
    
    async def store_summary(self, summary: InteractionSummary):
        """Store interaction summary in memory for future reference"""
        
        # Create a searchable text representation of the summary
        summary_text = f"""
        Intent: {summary.user_intent}
        Key Concepts: {', '.join(summary.key_concepts)}
        Response: {summary.agent_response}
        Success Indicators: {', '.join(summary.success_indicators)}
        Quality Score: {summary.response_quality}
        """
        
        # Add to memory using existing vector memory system
        # We'll create a temporary history entry to leverage existing save mechanism
        temp_history = [
            {"role": "summary", "content": summary_text.strip()},
            {"role": "metadata", "content": json.dumps({
                "timestamp": summary.timestamp,
                "intent": summary.user_intent,
                "concepts": summary.key_concepts,
                "confidence": summary.confidence,
                "quality": summary.response_quality
            })}
        ]
        
        # This will add the summary to the vector database
        current_texts_count = len(self.memory.texts)
        self.memory.save(self.memory.load() + temp_history)
        
        logger.info(f"Stored summary in memory. Total memories: {len(self.memory.texts)}")
    
    async def format_context_for_agents(self, relevant_memories: List[str], query: str) -> str:
        """Format retrieved memories into useful context for other agents"""
        
        if not relevant_memories:
            return "No relevant past experiences found."
        
        context_parts = [
            f"RELEVANT PAST EXPERIENCES for query: '{query}'",
            "-" * 50
        ]
        
        for i, memory in enumerate(relevant_memories, 1):
            context_parts.append(f"{i}. {memory}")
        
        context_parts.append("-" * 50)
        context_parts.append("Use this context to inform your response, but don't explicitly mention these past experiences unless directly relevant.")
        
        return "\n".join(context_parts)
    
    async def _generic_utility_response(self, request: AgentRequest) -> AgentResponse:
        """Handle generic utility requests"""
        return AgentResponse(
            request_id=request.id,
            content="I'm the Utility Agent. I can help with summarization and context management.",
            agent_id=self.agent_id,
            confidence=0.5,
            reasoning="Generic utility response for unspecified request"
        )
    
    async def process_successful_interaction(self, user_input: str, agent_response: str, 
                                           confidence: float, user_feedback: float = None):
        """
        Main entry point for processing successful interactions.
        This would be called by the coordinator after successful agent responses.
        """
        
        success_metrics = {
            'confidence': confidence,
            'user_satisfaction': user_feedback or 0.8,  # Default if no feedback
            'response_quality': min(confidence + 0.1, 1.0)  # Simple quality estimation
        }
        
        # Create and store summary
        summary = await self.create_interaction_summary(user_input, agent_response, success_metrics)
        await self.store_summary(summary)
        
        logger.info(f"Processed successful interaction - Intent: {summary.user_intent}, Quality: {summary.response_quality}")
        
        return summary
