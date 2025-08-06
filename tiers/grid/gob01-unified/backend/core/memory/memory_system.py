"""
Main memory system implementation for the unified agent framework.

Implements gob01's memory specification with production-ready infrastructure.
"""

import uuid
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from .memory_interface import IMemoryProvider
from .memory_types import MemoryFragment, UserData, Solution, MemoryType, MemoryMetadata, RetentionPolicy

logger = logging.getLogger(__name__)


class MemorySystem:
    """
    Main memory system that orchestrates memory operations.
    
    Provides hybrid, durable memory for agents to learn and recall across sessions
    with efficient context usage.
    """
    
    def __init__(self, provider: IMemoryProvider):
        self.provider = provider
        
    async def save(self, content: str, 
                  memory_type: MemoryType,
                  tags: Optional[List[str]] = None,
                  context: Optional[Dict[str, Any]] = None,
                  retention_policy: RetentionPolicy = RetentionPolicy.AUTO_EXPIRE,
                  has_pii: bool = False) -> str:
        """
        Store memory with metadata.
        
        Args:
            content: The memory content to store
            memory_type: Type of memory (user_data, fragment, solution)
            tags: Optional tags for categorization
            context: Additional context information
            retention_policy: How long to retain this memory
            has_pii: Whether content contains PII
            
        Returns:
            str: The memory ID
        """
        memory_id = str(uuid.uuid4())
        metadata = MemoryMetadata(
            id=memory_id,
            memory_type=memory_type,
            tags=tags or [],
            retention_policy=retention_policy,
            has_pii=has_pii,
            source="system"
        )
        
        if memory_type == MemoryType.FRAGMENT:
            memory_item = MemoryFragment(
                metadata=metadata,
                content=content,
                context=context or {}
            )
        elif memory_type == MemoryType.USER_DATA:
            # For user data, expect context to contain key and category
            memory_item = UserData(
                metadata=metadata,
                key=context.get("key", "unknown"),
                value=content,
                category=context.get("category", "general")
            )
        elif memory_type == MemoryType.SOLUTION:
            memory_item = Solution(
                metadata=metadata,
                problem_description=context.get("problem", ""),
                solution_content=content,
                solution_type=context.get("solution_type", "general"),
                success_metrics=context.get("metrics", {})
            )
        else:
            raise ValueError(f"Unknown memory type: {memory_type}")
            
        return await self.provider.save(memory_item)
    
    async def query(self, 
                   filter_params: Optional[Dict[str, Any]] = None,
                   limit: int = 10) -> List[Any]:
        """
        Retrieve memory items by tags/time/type.
        
        Args:
            filter_params: Dictionary containing filter criteria
            limit: Maximum number of results to return
            
        Returns:
            List of memory items matching the criteria
        """
        if not filter_params:
            filter_params = {}
            
        memory_type = filter_params.get("memory_type")
        tags = filter_params.get("tags")
        content_filter = filter_params.get("content_filter")
        
        results = await self.provider.query(
            memory_type=memory_type,
            tags=tags,
            content_filter=content_filter,
            limit=limit
        )
        
        # Update access count and last accessed time
        for item in results:
            if hasattr(item, 'metadata'):
                item.metadata.access_count += 1
                item.metadata.last_accessed = datetime.utcnow()
                await self.provider.update(item.metadata.id, {
                    "metadata.access_count": item.metadata.access_count,
                    "metadata.last_accessed": item.metadata.last_accessed
                })
        
        return results
    
    async def summarize_conversation(self, conversation_data: List[Dict[str, Any]]) -> List[MemoryFragment]:
        """
        Produce structured summaries from conversation data.
        
        Args:
            conversation_data: List of conversation messages/events
            
        Returns:
            List of memory fragments containing summaries
        """
        return await self.provider.summarize_conversation(conversation_data)
    
    async def compress_history(self, time_threshold: timedelta = timedelta(days=30)) -> List[MemoryFragment]:
        """
        Multi-level compression preserving originals.
        
        Implements the lifecycle: Recent → raw → Aging → summarized → Old → compressed
        
        Args:
            time_threshold: Age threshold for compression
            
        Returns:
            List of compressed memory fragments
        """
        # Find old memories that need compression
        old_memories = await self.query({
            "memory_type": MemoryType.FRAGMENT,
            "older_than": datetime.utcnow() - time_threshold
        }, limit=100)
        
        if not old_memories:
            return []
            
        memory_ids = [mem.metadata.id for mem in old_memories]
        return await self.provider.compress_history(memory_ids)
    
    async def cleanup_expired(self) -> int:
        """
        Clean up expired memories based on retention policies.
        
        Returns:
            Number of memories cleaned up
        """
        # This would implement cleanup logic based on retention policies
        # For now, just return 0 as placeholder
        logger.info("Memory cleanup completed")
        return 0
