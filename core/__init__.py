"""
Core Framework Components

Consolidated central nervous system including:
- Brain: Central coordination and intelligence
- Memory: Unified memory management
- Config: System configuration
- Data: Persistent data storage
"""

# Import main components for easy access
from .brain.central_brain import CentralBrain
from .brain.system_prompt_manager import SystemPromptManager
from .brain.context_builder import UnifiedContextBuilder
from .brain.knowledge_manager import KnowledgeManager
from .brain.tool_manager import ToolManager

from .memory.memory_interface import UnifiedMemoryItem, MemoryType, RetentionPolicy
from .memory.memory_hub import UnifiedMemoryHub
from .memory.storage.json_storage import JSONMemoryStorage
from .memory.storage.sqlite_storage import SQLiteMemoryStorage
from .memory.storage.hybrid_storage import HybridMemoryStorage

__version__ = "1.0.0"
__all__ = [
    # Brain components
    "CentralBrain",
    "SystemPromptManager", 
    "UnifiedContextBuilder",
    "KnowledgeManager",
    "ToolManager",
    
    # Memory components
    "UnifiedMemoryItem",
    "MemoryType", 
    "RetentionPolicy",
    "UnifiedMemoryHub",
    "JSONMemoryStorage",
    "SQLiteMemoryStorage", 
    "HybridMemoryStorage"
]

# Convenience function
def get_central_brain():
    """Get a Central Brain instance with default configuration."""
    return CentralBrain()
