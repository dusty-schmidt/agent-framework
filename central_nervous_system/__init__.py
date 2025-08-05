"""
Central Nervous System for Agentic Framework

The unified brain that coordinates memory, knowledge, tools, context, and system prompts
across all tiers. This ensures consistent behavior and shared intelligence throughout
the entire agent framework.
"""

from .core.central_brain import CentralBrain
from .core.system_prompt_manager import SystemPromptManager
from .core.context_builder import UnifiedContextBuilder
from .core.knowledge_manager import KnowledgeManager
from .core.tool_manager import ToolManager

__version__ = "1.0.0"
__all__ = [
    "CentralBrain",
    "SystemPromptManager",
    "UnifiedContextBuilder", 
    "KnowledgeManager",
    "ToolManager"
]
