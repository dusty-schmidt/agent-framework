"""
Memory System for the unified agent framework.

Implements gob01's memory specification with gob01-mini's working infrastructure.
Provides hybrid, durable memory for agents to learn and recall across sessions.
"""

from .memory_system import MemorySystem
from .memory_types import MemoryFragment, UserData, Solution, MemoryMetadata
from .memory_interface import IMemoryProvider

__all__ = [
    'MemorySystem',
    'MemoryFragment',
    'UserData', 
    'Solution',
    'MemoryMetadata',
    'IMemoryProvider'
]
