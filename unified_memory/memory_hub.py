"""
Unified Memory Hub - Central memory coordination for the Agentic Framework.

Provides a high-level interface for memory operations across all tiers.
"""

import logging
from typing import Dict, Any, List, Optional
from .memory_interface import UnifiedMemoryItem, MemoryType, MemoryQueryFilter, MemorySearchResult

logger = logging.getLogger(__name__)


class UnifiedMemoryHub:
    """
    Central hub for memory operations across all tiers.
    
    Provides a high-level interface that abstracts the underlying storage
    implementation and provides unified memory operations.
    """
    
    def __init__(self, storage_backend):
        """Initialize the memory hub with a storage backend."""
        self.storage = storage_backend
        self.session_memories = {}  # In-memory session cache
        
        logger.info("Unified Memory Hub initialized")
    
    async def save_memory(self, content: str, memory_type: MemoryType, 
                         tier_source: str, session_id: str = "default",
                         metadata: Optional[Dict[str, Any]] = None,
                         tags: Optional[List[str]] = None) -> str:
        """Save a memory item."""
        memory_item = UnifiedMemoryItem(
            content=content,
            memory_type=memory_type,
            tier_source=tier_source,
            session_id=session_id,
            metadata=metadata or {},
            tags=tags or []
        )
        
        memory_id = await self.storage.save(memory_item)
        
        # Cache in session memory
        if session_id not in self.session_memories:
            self.session_memories[session_id] = []
        self.session_memories[session_id].append(memory_id)
        
        logger.info(f"Saved memory: {memory_id} for session {session_id}")
        return memory_id
    
    async def get_memory(self, memory_id: str) -> Optional[UnifiedMemoryItem]:
        """Get a specific memory item by ID."""
        return await self.storage.get_by_id(memory_id)
    
    async def search_memories(self, query: str, memory_types: Optional[List[MemoryType]] = None,
                            tier_sources: Optional[List[str]] = None,
                            session_id: Optional[str] = None,
                            limit: int = 10) -> MemorySearchResult:
        """Search for relevant memories."""
        # Use semantic search if available
        if hasattr(self.storage, 'semantic_search'):
            return await self.storage.semantic_search(
                query=query,
                memory_types=memory_types,
                tier_sources=tier_sources,
                limit=limit
            )
        else:
            # Fall back to regular query
            filter_params = MemoryQueryFilter(
                memory_types=memory_types,
                tier_sources=tier_sources,
                session_id=session_id,
                limit=limit
            )
            return await self.storage.query(filter_params)
    
    async def get_session_memories(self, session_id: str, limit: int = 50) -> List[UnifiedMemoryItem]:
        """Get all memories for a session."""
        filter_params = MemoryQueryFilter(
            session_id=session_id,
            limit=limit
        )
        result = await self.storage.query(filter_params)
        return result.items
    
    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory item."""
        if hasattr(self.storage, 'update'):
            return await self.storage.update(memory_id, updates)
        else:
            # Get, modify, save pattern
            memory = await self.get_memory(memory_id)
            if memory:
                for key, value in updates.items():
                    if hasattr(memory, key):
                        setattr(memory, key, value)
                await self.storage.save(memory)
                return True
            return False
    
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory item."""
        if hasattr(self.storage, 'delete'):
            return await self.storage.delete(memory_id)
        return False
    
    def get_session_cache(self, session_id: str) -> List[str]:
        """Get cached memory IDs for a session."""
        return self.session_memories.get(session_id, [])
    
    def clear_session_cache(self, session_id: str):
        """Clear the session cache."""
        if session_id in self.session_memories:
            del self.session_memories[session_id]
            logger.info(f"Cleared session cache for {session_id}")
    
    async def get_statistics(self) -> Dict[str, Any]:
        """Get memory hub statistics."""
        stats = {"sessions": len(self.session_memories)}
        
        if hasattr(self.storage, 'get_statistics'):
            storage_stats = await self.storage.get_statistics()
            stats.update(storage_stats)
        
        return stats
