"""
Central Brain - The unified intelligence coordinator for the entire agent framework.

This is the main orchestrator that manages and coordinates all shared systems:
- Unified Memory System  
- Knowledge Base
- Tool Registry
- Context Building
- System Prompt Management
"""

import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import unified memory system
from ..memory.memory_interface import UnifiedMemoryItem, MemoryType
from ..memory.storage.hybrid_storage import HybridMemoryStorage
from ..memory.memory_hub import UnifiedMemoryHub

# Import central nervous system components
from .system_prompt_manager import SystemPromptManager
from .context_builder import UnifiedContextBuilder
from .knowledge_manager import KnowledgeManager
from .tool_manager import ToolManager

logger = logging.getLogger(__name__)


class CentralBrain:
    """
    The Central Brain coordinates all shared intelligence systems across tiers.
    
    This is the single source of truth for:
    - Memory operations
    - Knowledge retrieval
    - Tool availability
    - Context building
    - System prompt generation
    """
    
    def __init__(self, base_path: str = "./core/data"):
        """Initialize the Central Brain with all subsystems."""
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize core systems
        self._init_memory_system()
        self._init_knowledge_system()
        self._init_tool_system()
        self._init_prompt_system()
        self._init_context_system()
        
        # Track connected tiers
        self.connected_tiers = {}
        
        logger.info("Central Brain initialized successfully")
    
    def _init_memory_system(self):
        """Initialize the unified memory system."""
        memory_path = self.base_path / "memory"
        storage = HybridMemoryStorage(str(memory_path))
        self.memory_hub = UnifiedMemoryHub(storage)
        logger.info("Memory system initialized")
    
    def _init_knowledge_system(self):
        """Initialize the knowledge management system."""
        knowledge_path = self.base_path / "knowledge"
        self.knowledge_manager = KnowledgeManager(knowledge_path)
        logger.info("Knowledge system initialized")
    
    def _init_tool_system(self):
        """Initialize the tool management system."""
        tools_path = self.base_path / "tools"
        self.tool_manager = ToolManager(tools_path)
        logger.info("Tool system initialized")
    
    def _init_prompt_system(self):
        """Initialize the system prompt management."""
        prompts_path = self.base_path / "config"
        self.prompt_manager = SystemPromptManager(prompts_path)
        logger.info("Prompt system initialized")
    
    def _init_context_system(self):
        """Initialize the context building system."""
        self.context_builder = UnifiedContextBuilder(
            memory_hub=self.memory_hub,
            knowledge_manager=self.knowledge_manager,
            tool_manager=self.tool_manager,
            prompt_manager=self.prompt_manager
        )
        logger.info("Context system initialized")
    
    # ==================== TIER MANAGEMENT ====================
    
    def register_tier(self, tier_name: str, tier_config: Dict[str, Any]):
        """Register a tier with the Central Brain."""
        self.connected_tiers[tier_name] = {
            "config": tier_config,
            "connected_at": datetime.utcnow(),
            "last_active": datetime.utcnow(),
            "request_count": 0
        }
        logger.info(f"Tier '{tier_name}' registered with Central Brain")
    
    def unregister_tier(self, tier_name: str):
        """Unregister a tier from the Central Brain."""
        if tier_name in self.connected_tiers:
            del self.connected_tiers[tier_name]
            logger.info(f"Tier '{tier_name}' unregistered from Central Brain")
    
    # ==================== UNIFIED INTERFACE ====================
    
    async def process_request(self, 
                            tier_name: str,
                            user_message: str,
                            session_id: str = "default",
                            context_override: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main interface for tiers to request processing from the Central Brain.
        
        Returns unified context with everything a tier needs to respond intelligently.
        """
        # Update tier activity
        if tier_name in self.connected_tiers:
            self.connected_tiers[tier_name]["last_active"] = datetime.utcnow()
            self.connected_tiers[tier_name]["request_count"] += 1
        
        # Build comprehensive context
        context = self.context_builder.build_context(
            request=user_message,
            session_id=session_id,
            tier_name=tier_name
        )
        
        # Log the interaction for system learning
        await self._log_interaction(tier_name, user_message, session_id)
        
        return context
    
    async def save_interaction(self,
                             tier_name: str,
                             user_message: str,
                             agent_response: str,
                             session_id: str = "default",
                             metadata: Optional[Dict[str, Any]] = None):
        """Save a completed interaction to unified memory."""
        
        # Save user message
        user_memory = UnifiedMemoryItem(
            content=user_message,
            memory_type=MemoryType.CONVERSATION,
            tier_source=tier_name,
            tags=["user_input", session_id],
            metadata={
                "session_id": session_id,
                "role": "user",
                **(metadata or {})
            }
        )
        
        # Save agent response
        agent_memory = UnifiedMemoryItem(
            content=agent_response,
            memory_type=MemoryType.CONVERSATION,
            tier_source=tier_name,
            tags=["agent_response", session_id],
            metadata={
                "session_id": session_id,
                "role": "assistant",
                **(metadata or {})
            }
        )
        
        # Save both to memory
        await self.memory_hub.save_memory(user_memory)
        await self.memory_hub.save_memory(agent_memory)
        
        logger.debug(f"Saved interaction for tier '{tier_name}', session '{session_id}'")
    
    async def save_solution(self,
                          tier_name: str,
                          problem_description: str,
                          solution_content: str,
                          solution_type: str = "general",
                          success_metrics: Optional[Dict[str, Any]] = None):
        """Save a successful solution that could be reused."""
        
        solution_memory = UnifiedMemoryItem(
            content=solution_content,
            memory_type=MemoryType.SOLUTION,
            tier_source=tier_name,
            tags=["solution", solution_type, tier_name],
            metadata={
                "problem_description": problem_description,
                "solution_type": solution_type,
                "success_metrics": success_metrics or {},
                "tier_source": tier_name
            }
        )
        
        await self.memory_hub.save_memory(solution_memory)
        logger.info(f"Saved solution from tier '{tier_name}': {solution_type}")
    
    async def save_user_data(self,
                           key: str,
                           value: Any,
                           category: str = "general",
                           tier_source: str = "system"):
        """Save user data/preferences that persist across sessions."""
        
        user_data_memory = UnifiedMemoryItem(
            content=str(value),
            memory_type=MemoryType.USER_DATA,
            tier_source=tier_source,
            tags=["user_data", category, key],
            metadata={
                "key": key,
                "category": category,
                "data_type": type(value).__name__
            }
        )
        
        await self.memory_hub.save_memory(user_data_memory)
        logger.debug(f"Saved user data: {key} = {value}")
    
    # ==================== SYSTEM MANAGEMENT ====================
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all Central Brain systems."""
        
        memory_stats = await self.memory_hub.get_stats()
        knowledge_stats = await self.knowledge_manager.get_stats()
        tool_stats = await self.tool_manager.get_stats()
        
        return {
            "central_brain": {
                "status": "active",
                "connected_tiers": len(self.connected_tiers),
                "tier_details": self.connected_tiers
            },
            "memory_system": memory_stats,
            "knowledge_system": knowledge_stats,
            "tool_system": tool_stats,
            "uptime": datetime.utcnow() - self._start_time if hasattr(self, '_start_time') else None
        }
    
    async def cleanup_systems(self):
        """Perform maintenance cleanup on all systems."""
        
        # Cleanup expired memories
        cleanup_stats = await self.memory_hub.cleanup_expired()
        
        # Cleanup knowledge cache
        knowledge_cleanup = await self.knowledge_manager.cleanup_cache()
        
        # Cleanup tool cache
        tool_cleanup = await self.tool_manager.cleanup_cache()
        
        logger.info("System cleanup completed", extra={
            "memory_cleanup": cleanup_stats,
            "knowledge_cleanup": knowledge_cleanup,
            "tool_cleanup": tool_cleanup
        })
        
        return {
            "memory": cleanup_stats,
            "knowledge": knowledge_cleanup,
            "tools": tool_cleanup
        }
    
    async def _log_interaction(self, tier_name: str, user_message: str, session_id: str):
        """Log interaction for system analytics and learning."""
        
        interaction_log = UnifiedMemoryItem(
            content=f"Tier '{tier_name}' processing: {user_message[:100]}...",
            memory_type=MemoryType.SYSTEM,
            tier_source="central_brain",
            tags=["system_log", "interaction", tier_name],
            metadata={
                "tier_name": tier_name,
                "session_id": session_id,
                "message_length": len(user_message),
                "log_type": "interaction"
            }
        )
        
        await self.memory_hub.save_memory(interaction_log)


# Global instance - single source of truth
_central_brain_instance = None

def get_central_brain(base_path: str = "./core/data") -> CentralBrain:
    """Get the global Central Brain instance (singleton pattern)."""
    global _central_brain_instance
    
    if _central_brain_instance is None:
        _central_brain_instance = CentralBrain(base_path)
        _central_brain_instance._start_time = datetime.utcnow()
    
    return _central_brain_instance
