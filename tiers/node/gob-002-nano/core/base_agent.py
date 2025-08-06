"""
Core base agent framework with hierarchical prompt system and self-improvement capabilities
"""

import logging
import json
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
from datetime import datetime
import uuid

logger = logging.getLogger('MultiAgentSystem')

@dataclass
class AgentRequest:
    """Standardized request format for inter-agent communication"""
    id: str
    user_input: str
    context: Dict[str, Any]
    priority: int = 1
    source_agent: Optional[str] = None
    target_agent: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.id:
            self.id = str(uuid.uuid4())

@dataclass
class AgentResponse:
    """Standardized response format for inter-agent communication"""
    request_id: str
    content: str
    agent_id: str
    confidence: float
    reasoning: str
    metadata: Dict[str, Any] = None
    success: bool = True
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class AgentCapability:
    """Define what an agent can do"""
    name: str
    description: str
    keywords: List[str]
    confidence_threshold: float = 0.7

class BaseAgent(ABC):
    """Base class for all agents with hierarchical prompt system"""
    
    def __init__(self, 
                 agent_id: str,
                 name: str,
                 capabilities: List[AgentCapability],
                 system_prompt: str,
                 memory_namespace: str = None):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = capabilities
        self.system_prompt = system_prompt
        self.memory_namespace = memory_namespace or agent_id
        self.logger = logging.getLogger(f'Agent.{name}')
        
        # For self-improvement tracking
        self.behavior_adjustments = []
        self.performance_metrics = {
            'tasks_completed': 0,
            'success_rate': 0.0,
            'avg_confidence': 0.0,
            'user_feedback_score': 0.0
        }
        
        self.logger.info(f"Initialized {self.name} agent with {len(capabilities)} capabilities")
    
    @abstractmethod
    async def process_request(self, request: AgentRequest) -> AgentResponse:
        """Main processing method - must be implemented by each agent"""
        pass
    
    def can_handle(self, request: AgentRequest) -> float:
        """Determine if this agent can handle the request and with what confidence"""
        user_input_lower = request.user_input.lower()
        
        # Check capabilities against user input
        total_confidence = 0.0
        matches = 0
        
        for capability in self.capabilities:
            keyword_matches = sum(1 for keyword in capability.keywords 
                                if keyword.lower() in user_input_lower)
            if keyword_matches > 0:
                # Confidence based on keyword density and capability threshold
                density = keyword_matches / len(capability.keywords)
                confidence = min(density * capability.confidence_threshold, 1.0)
                total_confidence += confidence
                matches += 1
        
        if matches == 0:
            return 0.0
        
        # Average confidence across all matching capabilities
        final_confidence = min(total_confidence / matches, 1.0)
        
        self.logger.debug(f"Confidence for '{request.user_input[:50]}...': {final_confidence:.3f}")
        return final_confidence
    
    async def adjust_behavior(self, feedback: str, adjustment_type: str = "system_prompt"):
        """Self-improvement mechanism - adjust agent behavior based on feedback"""
        self.logger.info(f"Adjusting behavior: {adjustment_type}")
        
        adjustment = {
            'timestamp': datetime.now().isoformat(),
            'type': adjustment_type,
            'feedback': feedback,
            'previous_state': None
        }
        
        if adjustment_type == "system_prompt":
            adjustment['previous_state'] = self.system_prompt
            # Use the feedback to modify system prompt
            # This is a simplified version - in production, this would be more sophisticated
            if "more detailed" in feedback.lower():
                self.system_prompt += "\n\nProvide more detailed explanations and examples."
            elif "more concise" in feedback.lower():
                self.system_prompt += "\n\nBe more concise and direct in responses."
            elif "more technical" in feedback.lower():
                self.system_prompt += "\n\nProvide technical details and implementation specifics."
            
            self.logger.info(f"System prompt adjusted based on: {feedback}")
        
        self.behavior_adjustments.append(adjustment)
        
        # Save adjustment to file for persistence
        await self.save_adjustments()
    
    async def save_adjustments(self):
        """Persist behavior adjustments to disk"""
        try:
            adjustments_file = f"config/agents/{self.agent_id}_adjustments.json"
            with open(adjustments_file, 'w') as f:
                json.dump({
                    'agent_id': self.agent_id,
                    'current_system_prompt': self.system_prompt,
                    'adjustments': self.behavior_adjustments,
                    'performance_metrics': self.performance_metrics
                }, f, indent=2)
            self.logger.info(f"Saved adjustments to {adjustments_file}")
        except Exception as e:
            self.logger.error(f"Failed to save adjustments: {e}")
    
    async def load_adjustments(self):
        """Load previous behavior adjustments from disk"""
        try:
            adjustments_file = f"config/agents/{self.agent_id}_adjustments.json"
            with open(adjustments_file, 'r') as f:
                data = json.load(f)
                self.system_prompt = data.get('current_system_prompt', self.system_prompt)
                self.behavior_adjustments = data.get('adjustments', [])
                self.performance_metrics = data.get('performance_metrics', self.performance_metrics)
            self.logger.info(f"Loaded {len(self.behavior_adjustments)} previous adjustments")
        except FileNotFoundError:
            self.logger.info("No previous adjustments found")
        except Exception as e:
            self.logger.error(f"Failed to load adjustments: {e}")
    
    def update_metrics(self, success: bool, confidence: float, user_feedback: float = None):
        """Update performance metrics for self-improvement tracking"""
        self.performance_metrics['tasks_completed'] += 1
        
        # Update success rate
        total_tasks = self.performance_metrics['tasks_completed']
        current_successes = (self.performance_metrics['success_rate'] * (total_tasks - 1))
        if success:
            current_successes += 1
        self.performance_metrics['success_rate'] = current_successes / total_tasks
        
        # Update average confidence
        current_avg = self.performance_metrics['avg_confidence']
        self.performance_metrics['avg_confidence'] = (
            (current_avg * (total_tasks - 1) + confidence) / total_tasks
        )
        
        # Update user feedback if provided
        if user_feedback is not None:
            current_feedback = self.performance_metrics['user_feedback_score']
            self.performance_metrics['user_feedback_score'] = (
                (current_feedback * (total_tasks - 1) + user_feedback) / total_tasks
            )
    
    def get_hierarchical_prompt(self, request: AgentRequest, base_context: str = "") -> str:
        """Build hierarchical prompt with main context + agent-specific context"""
        
        # Start with agent's specialized system prompt
        prompt_parts = [f"AGENT: {self.name}", self.system_prompt]
        
        # Add base context if provided (from main coordinator)
        if base_context:
            prompt_parts.append(f"OVERALL CONTEXT: {base_context}")
        
        # Add agent's performance context for self-awareness
        if self.performance_metrics['tasks_completed'] > 0:
            prompt_parts.append(
                f"PERFORMANCE CONTEXT: "
                f"Success rate: {self.performance_metrics['success_rate']:.2f}, "
                f"Avg confidence: {self.performance_metrics['avg_confidence']:.2f}"
            )
        
        # Add recent behavior adjustments
        if self.behavior_adjustments:
            recent_adjustments = self.behavior_adjustments[-3:]  # Last 3 adjustments
            adjustments_text = "; ".join([adj['feedback'] for adj in recent_adjustments])
            prompt_parts.append(f"RECENT ADJUSTMENTS: {adjustments_text}")
        
        # Add request context
        if request.context:
            context_str = json.dumps(request.context, indent=2)
            prompt_parts.append(f"REQUEST CONTEXT: {context_str}")
        
        # Add the actual user request
        prompt_parts.append(f"USER REQUEST: {request.user_input}")
        
        return "\n\n".join(prompt_parts)
