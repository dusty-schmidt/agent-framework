"""
Unified Memory System for Agentic Framework

This module provides a unified memory interface across all tiers of the agent framework,
enabling consistent memory operations, cross-tier data sharing, and intelligent context building.
"""

"""
Unified Memory System

Comprehensive memory management for the Agentic Framework.
"""

from .memory_interface import (
    IUnifiedMemoryProvider,
    UnifiedMemoryItem,
    MemoryType,
    RetentionPolicy,
    MemoryQueryFilter,
    MemorySearchResult
)
from .memory_hub import UnifiedMemoryHub

__version__ = "1.0.0"
__all__ = [
    "IUnifiedMemoryProvider",
    "UnifiedMemoryItem",
    "MemoryType",
    "RetentionPolicy",
    "MemoryQueryFilter",
    "MemorySearchResult",
    "UnifiedMemoryHub"
]
