"""
Unified Memory System for Agentic Framework

This module provides a unified memory interface across all tiers of the agent framework,
enabling consistent memory operations, cross-tier data sharing, and intelligent context building.
"""

from .memory_interface import (
    IUnifiedMemoryProvider,
    UnifiedMemoryItem,
    MemoryType,
    RetentionPolicy,
    MemoryQueryFilter
)
# from .memory_hub import UnifiedMemoryHub  # TODO: Implement memory hub
# from .context_manager import UnifiedContextManager  # TODO: Implement context manager

__version__ = "1.0.0"
__all__ = [
    "IUnifiedMemoryProvider",
    "UnifiedMemoryItem", 
    "MemoryType",
    "RetentionPolicy",
    "MemoryQueryFilter"
    # "UnifiedMemoryHub",  # TODO: Implement
    # "UnifiedContextManager"  # TODO: Implement
]
