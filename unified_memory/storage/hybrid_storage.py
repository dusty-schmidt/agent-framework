"""
Hybrid memory storage backend for unified memory system.

Combines JSON for metadata, SQLite for queries, and FAISS for semantic similarity.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from .json_storage import JSONMemoryStorage
from .sqlite_storage import SQLiteMemoryStorage
from .faiss_storage import FAISSMemoryStorage
from ..memory_interface import IUnifiedMemoryProvider, UnifiedMemoryItem, MemoryQueryFilter, MemorySearchResult
import os

class HybridMemoryStorage(IUnifiedMemoryProvider):
    def __init__(self, base_path: str):
        """
        Initialize hybrid storage across JSON, SQLite, and FAISS.

        Args:
            base_path (str): Base directory for all storage files.
        """

        self.json_store = JSONMemoryStorage(Path(base_path) / "json")
        self.sqlite_store = SQLiteMemoryStorage(Path(base_path) / "sqlite")
        self.faiss_store = FAISSMemoryStorage(Path(base_path) / "faiss")

    async def save(self, item: UnifiedMemoryItem) -> str:
        """
        Save memory item and return its ID.
        """
        await self.json_store.save(item)
        await self.sqlite_store.save(item)
        await self.faiss_store.save(item)
        return item.id

    async def get_by_id(self, memory_id: str) -> Optional[UnifiedMemoryItem]:
        """
        Retrieve a specific memory item by its ID.
        """
        return await self.json_store.get_by_id(memory_id)

    async def query(self, filter_params: MemoryQueryFilter) -> MemorySearchResult:
        """
        Query memory items by advanced attributes.
        """
        return await self.sqlite_store.query(filter_params)

    async def semantic_search(self, query: str, memory_types: Optional[List] = None, tier_sources: Optional[List[str]] = None, limit: int = 10) -> MemorySearchResult:
        """
        Perform semantic search using vector embeddings.
        """
        return await self.faiss_store.semantic_search(query, memory_types, tier_sources, limit)

    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update memory item with given properties.
        """
        updated = await self.json_store.update(memory_id, updates)
        if updated:
            await self.sqlite_store.update(memory_id, updates)
        return updated

    async def delete(self, memory_id: str) -> bool:
        """
        Delete a memory item completely.
        """
        deleted = await self.json_store.delete(memory_id)
        if deleted:
            await self.sqlite_store.delete(memory_id)
            await self.faiss_store.delete(memory_id)
        return deleted

    async def batch_save(self, items: List[UnifiedMemoryItem]) -> List[str]:
        """
        Efficiently save a batch of memory items.
        """
        ids = [item.id for item in items]
        await self.json_store.batch_save(items)
        await self.sqlite_store.batch_save(items)
        await self.faiss_store.batch_save(items)
        return ids

    async def cleanup_expired(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Remove expired items from memory.
        """
        return await self.json_store.cleanup_expired(dry_run)

    async def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics and status.
        """
        stats = await self.json_store.get_stats()
        stats.update(await self.sqlite_store.get_stats())
        stats.update(await self.faiss_store.get_stats())
        return stats

