"""
JSON Storage Backend - Simple file-based persistence for memory items.

This storage provides an easy-to-use JSON file format for storing 
memory items, making it easy to inspect, backup, and share.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..memory_interface import IUnifiedMemoryProvider, UnifiedMemoryItem, MemoryQueryFilter, MemorySearchResult
import os

class JSONMemoryStorage(IUnifiedMemoryProvider):
    def __init__(self, base_path: Path):
        """
        Initialize JSON Storage for memory items.

        Args:
            base_path (Path): Base directory path where JSON files are stored.
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _memory_file_path(self, memory_id: str) -> Path:
        return self.base_path / f"{memory_id}.json"

    async def save(self, item: UnifiedMemoryItem) -> str:
        """
        Save memory item to a JSON file.
        """
        file_path = self._memory_file_path(item.id)
        
        # Convert datetime objects to ISO format strings for JSON serialization
        item_dict = item.dict()
        if item_dict.get('timestamp'):
            item_dict['timestamp'] = item_dict['timestamp'].isoformat()
        if item_dict.get('last_accessed'):
            item_dict['last_accessed'] = item_dict['last_accessed'].isoformat()
        if item_dict.get('last_modified'):
            item_dict['last_modified'] = item_dict['last_modified'].isoformat()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(item_dict, f, ensure_ascii=False, indent=4)
        return item.id

    async def get_by_id(self, memory_id: str) -> Optional[UnifiedMemoryItem]:
        """
        Retrieve a specific memory item by its ID.
        """
        file_path = self._memory_file_path(memory_id)
        if not file_path.exists():
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return UnifiedMemoryItem(**data)

    async def query(self, filter_params: MemoryQueryFilter) -> MemorySearchResult:
        """
        Query memory items based on filter parameters.
        """
        all_files = list(self.base_path.glob('*.json'))
        results = []
        for file_path in all_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Simple check - in real case, we would apply complex filter logic
                if not filter_params.content_search or filter_params.content_search.lower() in data.get('content', '').lower():
                    results.append(UnifiedMemoryItem(**data))

        return MemorySearchResult(
            items=results[:filter_params.limit],
            total_count=len(results),
            search_time_ms=0,
            query_filter=filter_params
        )

    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a memory item with given properties.
        """
        item = await self.get_by_id(memory_id)
        if not item:
            return False
        for key, value in updates.items():
            setattr(item, key, value)
        await self.save(item)  # Save updated item
        return True

    async def delete(self, memory_id: str) -> bool:
        """
        Delete a memory item completely.
        """
        file_path = self._memory_file_path(memory_id)
        if file_path.exists():
            os.remove(file_path)
            return True
        return False

    async def batch_save(self, items: List[UnifiedMemoryItem]) -> List[str]:
        """
        Save multiple memory items efficiently.
        """
        ids = []
        for item in items:
            await self.save(item)
            ids.append(item.id)
        return ids

    async def cleanup_expired(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Remove expired items from memory.
        """
        # For JSON storage, we'll define expiration as any item older than a threshold
        expired_count = 0
        all_files = list(self.base_path.glob('*.json'))
        for file_path in all_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                item = UnifiedMemoryItem(**data)
                if item.retention_policy == 'temporary' and (datetime.utcnow() - item.timestamp).total_seconds() > 24 * 3600:
                    if not dry_run:
                        os.remove(file_path)
                    expired_count += 1
        return {'expired_count': expired_count}

    async def semantic_search(self, 
                            query: str, 
                            memory_types: Optional[List] = None,
                            tier_sources: Optional[List[str]] = None,
                            limit: int = 10) -> MemorySearchResult:
        """
        Simple text-based search implementation (not true semantic search).
        For real semantic search, use FAISS storage backend.
        """
        # Use content search as a fallback for semantic search
        filter_params = MemoryQueryFilter(
            content_search=query,
            memory_types=memory_types,
            tier_sources=tier_sources,
            limit=limit
        )
        
        result = await self.query(filter_params)
        return result

    async def get_stats(self) -> Dict[str, Any]:
        """
        Get memory storage statistics.
        """
        total_files = len(list(self.base_path.glob('*.json')))
        total_size = sum(f.stat().st_size for f in self.base_path.glob('*.json'))
        return {
            'total_items': total_files,
            'total_size_bytes': total_size
        }

