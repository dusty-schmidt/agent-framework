# Filename: main_agent.py
# Location: backend/agents/main_agent.py

from typing import Dict, Any, List, Optional, Tuple
from langchain.schema import HumanMessage, SystemMessage
from .base import BaseAgent, AgentConfig, LLMTier, AgentCapability
from .registry import agent_registry
from ..config.config_loader import config_loader
import logging

logger = logging.getLogger(__name__)


class MainAgent(BaseAgent):
    """Primary agent that users interact with. Handles most tasks and summons specialists when needed."""
    
    def __init__(self, api_key: str):
        config = AgentConfig(
            name="main_agent",
            description="Primary conversational agent that handles most user interactions and summons specialists for complex tasks",
            llm_tier=LLMTier.CHAT,  # Main chat model for primary interactions
            system_prompt=self._get_system_prompt(),
            capabilities=[
                AgentCapability(
                    name="general_conversation",
                    description="Handle general conversations, questions, and explanations",
                    keywords=["hello", "hi", "how", "what", "why", "explain", "tell", "help"]
                ),
                AgentCapability(
                    name="task_coordination",
                    description="Coordinate complex tasks by summoning appropriate specialists",
                    keywords=["complex", "detailed", "specific", "technical", "advanced"]
                ),
                AgentCapability(
                    name="information_synthesis",
                    description="Synthesize information from multiple sources or specialists",
                    keywords=["combine", "compare", "analyze", "summarize", "overview"]
                )
            ],
            temperature=0.7  # Balanced temperature for natural conversation
        )
        super().__init__(config, api_key, "main", "main")
    
    def _get_system_prompt(self) -> str:
        return """You are the Main Agent - the primary interface that users interact with. You are helpful, knowledgeable, and capable of handling most user requests directly.

Your role and responsibilities:
1. **Primary Interface**: You are the main point of contact for users
2. **Direct Assistance**: Handle most questions, conversations, and tasks yourself
3. **Specialist Coordination**: For highly specialized or complex tasks, summon appropriate specialists
4. **Context Maintenance**: Keep track of conversation context and user needs

When to summon specialists:
- **Coding Tasks**: Complex programming, debugging, or technical implementation → summon coding_assistant
- **Creative Tasks**: Creative writing, storytelling, artistic content → summon creative_assistant  
- **Research Tasks**: Deep research, fact-checking, web browsing → summon research_assistant
- **Technical Analysis**: Complex technical analysis or specialized domain knowledge → summon appropriate specialist

Available specialists:
{specialist_capabilities}

Guidelines for specialist summoning:
- Only summon specialists for tasks that truly require specialized expertise
- Handle simple questions, explanations, and general conversations yourself
- When summoning a specialist, format your response as: "[Summoning specialist_name] reason for summoning"
- After specialist completes their task, you can add your own insights or explanations

Your personality:
- Helpful and knowledgeable
- Natural conversational style
- Proactive in offering assistance
- Clear about when you're summoning specialists and why

Remember: You are the main agent users talk to. Most interactions should be handled by you directly."""

    async def process(self, message: str, context: Dict[str, Any] = None) -> str:
        """Main process method required by BaseAgent"""
        # Convert context format if needed
        history = context.get("history", []) if context else []
        return await self.process_message(message, history)

    async def process_message(self, message: str, context: List[Dict[str, Any]] = None) -> str:
        """Process user message and decide whether to handle directly or summon specialist"""

        # For now, handle everything directly to test the basic functionality
        # TODO: Add specialist summoning logic back once basic functionality works
        return await self._handle_directly(message, context)
    
    def _should_summon_specialist(self, message: str) -> Optional[Tuple[str, str]]:
        """Determine if a specialist should be summoned and why"""
        message_lower = message.lower()
        
        # Coding-related keywords
        coding_keywords = ["code", "program", "function", "debug", "python", "javascript", "java", "c++", "algorithm", "api", "database", "sql"]
        if any(keyword in message_lower for keyword in coding_keywords):
            if any(complex_word in message_lower for complex_word in ["write", "create", "build", "implement", "develop", "fix", "debug"]):
                return ("coding_assistant", "This requires specialized programming expertise")
        
        # Creative writing keywords
        creative_keywords = ["story", "poem", "creative", "write", "narrative", "character", "plot", "fiction"]
        if any(keyword in message_lower for keyword in creative_keywords):
            if any(creative_word in message_lower for creative_word in ["write", "create", "story", "poem", "creative"]):
                return ("creative_assistant", "This requires creative writing expertise")
        
        # Research keywords
        research_keywords = ["research", "find", "search", "investigate", "facts", "data", "study", "analysis"]
        if any(keyword in message_lower for keyword in research_keywords):
            if any(research_word in message_lower for research_word in ["detailed", "comprehensive", "thorough", "deep"]):
                return ("research_assistant", "This requires detailed research capabilities")
        
        return None
    
    async def _summon_specialist(self, specialist_name: str, message: str, context: List[Dict[str, Any]] = None) -> str:
        """Summon a specialist agent to handle the task"""
        try:
            # Find the specialist in the registry
            specialist_agent = agent_registry.get_agent(specialist_name)
            if specialist_agent:
                return await specialist_agent.process_message(message, context)
            else:
                # Fallback to available agent
                best_agent, confidence = agent_registry.find_best_agent(message)
                if best_agent:
                    return await best_agent.process_message(message, context)
                else:
                    return await self._handle_directly(message, context)
        except Exception as e:
            logger.error(f"Error summoning specialist {specialist_name}: {e}")
            return await self._handle_directly(message, context)
    
    async def _handle_directly(self, message: str, context: List[Dict[str, Any]] = None) -> str:
        """Handle the message directly as the main agent"""
        try:
            # Prepare context
            messages = []
            
            # Add system message
            messages.append(SystemMessage(content=self.config.system_prompt.format(
                specialist_capabilities=self._get_specialist_capabilities()
            )))
            
            # Add conversation context if available
            if context:
                for ctx in context[-5:]:  # Last 5 messages for context
                    if ctx.get("role") == "user":
                        messages.append(HumanMessage(content=ctx["content"]))
                    # Note: We don't add assistant messages to avoid confusion
            
            # Add current message
            messages.append(HumanMessage(content=message))
            
            # Get response from LLM
            response = await self.llm.agenerate([messages])
            return response.generations[0][0].text.strip()
            
        except Exception as e:
            logger.error(f"Error in main agent direct handling: {e}")
            return "I apologize, but I encountered an error processing your request. Please try again."
    
    def _get_specialist_capabilities(self) -> str:
        """Get formatted list of specialist capabilities"""
        # Simplified for now - hardcoded list to avoid registry issues
        return """- coding_assistant: Expert programming assistant for code development and debugging
- general_assistant: Helpful general assistant for various tasks and questions"""
