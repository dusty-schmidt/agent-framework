"""
Memory interface for the unified agent framework.

Defines the contract for memory providers and operations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from .memory_types import MemoryFragment, UserData, Solution, MemoryType


class IMemoryProvider(ABC):
    """Interface for memory storage providers"""
    
    @abstractmethod
    async def save(self, memory_item: Any) -> str:
        """Save a memory item and return its ID"""
        pass
    
    @abstractmethod
    async def query(self, 
                   memory_type: Optional[MemoryType] = None,
                   tags: Optional[List[str]] = None,
                   content_filter: Optional[str] = None,
                   limit: int = 10) -> List[Any]:
        """Query memory items with filters"""
        pass
    
    @abstractmethod
    async def get_by_id(self, memory_id: str) -> Optional[Any]:
        """Get a specific memory item by ID"""
        pass
    
    @abstractmethod
    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory item"""
        pass
    
    @abstractmethod
    async def delete(self, memory_id: str) -> bool:
        """Delete a memory item"""
        pass
    
    @abstractmethod
    async def summarize_conversation(self, conversation_data: List[Dict[str, Any]]) -> List[MemoryFragment]:
        """Produce structured summaries from conversation data"""
        pass
    
    @abstractmethod
    async def compress_history(self, memory_ids: List[str]) -> List[MemoryFragment]:
        """Multi-level compression preserving originals"""
        pass
