"""
SQLite Storage Backend - Relational database storage for memory items.

This storage provides a SQL-based persistence mechanism using SQLite,
allowing for complex queries, relationships, and data management.
"""

import aiosqlite
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from ..memory_interface import IUnifiedMemoryProvider, UnifiedMemoryItem, MemoryQueryFilter, MemorySearchResult


class SQLiteMemoryStorage(IUnifiedMemoryProvider):
    def __init__(self, db_path: Path):
        """
        Initialize SQLite Storage for memory items.

        Args:
            db_path (Path): Path to SQLite database file.
        """
        self.db_path = db_path

    async def _initialize_db(self):
        """
        Initialize the database schema if not already done.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                tier_source TEXT,
                tags TEXT,
                metadata TEXT,
                timestamp DATETIME NOT NULL,
                retention_policy TEXT,
                access_count INTEGER DEFAULT 0,
                last_accessed DATETIME
            )
            """)
            await db.commit()

    async def save(self, item: UnifiedMemoryItem) -> str:
        """
        Save memory item to the SQLite database.
        """
        await self._initialize_db()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
            INSERT OR REPLACE INTO memories (id, content, memory_type, tier_source, tags, metadata, timestamp, retention_policy, access_count, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.id, item.content, item.memory_type.value, 
                item.tier_source, ','.join(item.tags), json.dumps(item.metadata),
                item.timestamp.isoformat(), item.retention_policy,
                item.access_count, item.last_accessed.isoformat() if item.last_accessed else None
            ))
            await db.commit()
        return item.id

    async def get_by_id(self, memory_id: str) -> Optional[UnifiedMemoryItem]:
        """
        Retrieve a specific memory item by its ID.
        """
        await self._initialize_db()
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT * FROM memories WHERE id = ?", (memory_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return UnifiedMemoryItem(
                        id=row[0], content=row[1], memory_type=row[2],
                        tier_source=row[3], tags=row[4].split(','),
                        metadata=json.loads(row[5]),
                        timestamp=datetime.fromisoformat(row[6]),
                        retention_policy=row[7], access_count=row[8],
                        last_accessed=datetime.fromisoformat(row[9]) if row[9] else None
                    )
        return None

    async def query(self, filter_params: MemoryQueryFilter) -> MemorySearchResult:
        """
        Query memory items based on filter parameters.
        """
        await self._initialize_db()
        sql = "SELECT * FROM memories WHERE 1=1"
        params = []

        if filter_params.content_search:
            sql += " AND content LIKE ?"
            params.append(f'%{filter_params.content_search}%')

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(sql, params) as cursor:
                rows = await cursor.fetchall()
                results = [
                    UnifiedMemoryItem(
                        id=row[0], content=row[1], memory_type=row[2],
                        tier_source=row[3], tags=row[4].split(','),
                        metadata=json.loads(row[5]),
                        timestamp=datetime.fromisoformat(row[6]),
                        retention_policy=row[7], access_count=row[8],
                        last_accessed=datetime.fromisoformat(row[9]) if row[9] else None
                    )
                    for row in rows
                ]

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

        await self.save(item)
        return True

    async def delete(self, memory_id: str) -> bool:
        """
        Delete a memory item completely.
        """
        await self._initialize_db()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            await db.commit()
        return True

    async def batch_save(self, items: List[UnifiedMemoryItem]) -> List[str]:
        """
        Save multiple memory items efficiently.
        """
        await self._initialize_db()
        async with aiosqlite.connect(self.db_path) as db:
            for item in items:
                await db.execute("""
                INSERT OR REPLACE INTO memories (id, content, memory_type, tier_source, tags, metadata, timestamp, retention_policy, access_count, last_accessed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.id, item.content, item.memory_type.value, 
                    item.tier_source, ','.join(item.tags), json.dumps(item.metadata),
                    item.timestamp.isoformat(), item.retention_policy,
                    item.access_count, item.last_accessed.isoformat() if item.last_accessed else None
                ))
            await db.commit()

        return [item.id for item in items]

    async def cleanup_expired(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Remove expired items from memory.
        """
        await self._initialize_db()
        expired_count = 0
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT id, timestamp FROM memories") as cursor:
                rows = await cursor.fetchall()
                for row in rows:
                    timestamp = datetime.fromisoformat(row[1])
                    if (datetime.utcnow() - timestamp).total_seconds() > 24 * 3600:  # example 1 day expiration
                        if not dry_run:
                            await db.execute("DELETE FROM memories WHERE id = ?", (row[0],))
                        expired_count += 1
                if not dry_run:
                    await db.commit()

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
        await self._initialize_db()
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM memories") as cursor:
                total_items = await cursor.fetchone()

        return {
            'total_items': total_items[0],
            'storage_type': 'SQLite'
        }

