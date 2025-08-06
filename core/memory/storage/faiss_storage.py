"""
FAISS Storage Backend - Vector-based semantic search storage for memory items.

This storage provides semantic search capabilities using FAISS (Facebook AI Similarity Search),
allowing for efficient similarity-based retrieval of memory items based on content embeddings.
"""

import json
import pickle
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
import numpy as np
from ..memory_interface import IUnifiedMemoryProvider, UnifiedMemoryItem, MemoryQueryFilter, MemorySearchResult

try:
    import faiss
except ImportError:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None


class FAISSMemoryStorage(IUnifiedMemoryProvider):
    def __init__(self, index_path: Path, embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize FAISS Storage for memory items with semantic search.

        Args:
            index_path (Path): Path to store FAISS index and metadata files.
            embedding_model (str): Name of the sentence transformer model to use for embeddings.
        
        Raises:
            ImportError: If FAISS or sentence-transformers is not installed.
        """
        if faiss is None:
            raise ImportError("FAISS is required for vector storage. Install with: pip install faiss-cpu")
        
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is required for embeddings. Install with: pip install sentence-transformers")
        
        self.index_path = index_path
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        self.faiss_index_file = self.index_path / "memory.index"
        self.metadata_file = self.index_path / "metadata.pkl"
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        
        # FAISS index and metadata
        self.index = None
        self.id_to_memory = {}  # Maps FAISS index positions to memory items
        self.memory_id_to_index = {}  # Maps memory IDs to FAISS index positions
        self.next_index_position = 0
        
        self._load_index()

    def _load_index(self):
        """Load existing FAISS index and metadata from disk."""
        if self.faiss_index_file.exists() and self.metadata_file.exists():
            try:
                # Load FAISS index
                self.index = faiss.read_index(str(self.faiss_index_file))
                
                # Load metadata
                with open(self.metadata_file, 'rb') as f:
                    metadata = pickle.load(f)
                    self.id_to_memory = metadata.get('id_to_memory', {})
                    self.memory_id_to_index = metadata.get('memory_id_to_index', {})
                    self.next_index_position = metadata.get('next_index_position', 0)
                    
            except Exception as e:
                print(f"Error loading FAISS index: {e}. Creating new index.")
                self._create_new_index()
        else:
            self._create_new_index()

    def _create_new_index(self):
        """Create a new FAISS index."""
        # Using L2 distance for similarity search
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.id_to_memory = {}
        self.memory_id_to_index = {}
        self.next_index_position = 0

    def _save_index(self):
        """Save FAISS index and metadata to disk."""
        try:
            # Save FAISS index
            faiss.write_index(self.index, str(self.faiss_index_file))
            
            # Save metadata
            metadata = {
                'id_to_memory': self.id_to_memory,
                'memory_id_to_index': self.memory_id_to_index,
                'next_index_position': self.next_index_position
            }
            with open(self.metadata_file, 'wb') as f:
                pickle.dump(metadata, f)
                
        except Exception as e:
            print(f"Error saving FAISS index: {e}")

    def _get_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for given text."""
        return self.embedding_model.encode([text])[0]

    async def save(self, item: UnifiedMemoryItem) -> str:
        """
        Save memory item to the FAISS index with embedding.
        """
        # Generate embedding for the content
        embedding = self._get_embedding(item.content)
        
        # Check if item already exists
        if item.id in self.memory_id_to_index:
            # Update existing item
            index_pos = self.memory_id_to_index[item.id]
            self.id_to_memory[index_pos] = item
            
            # Note: FAISS doesn't support in-place updates easily,
            # so we'd need to rebuild index for updates. For now, we'll store the updated item
            # but the embedding won't change unless we rebuild.
        else:
            # Add new item
            embedding_2d = embedding.reshape(1, -1).astype('float32')
            self.index.add(embedding_2d)
            
            index_pos = self.next_index_position
            self.id_to_memory[index_pos] = item
            self.memory_id_to_index[item.id] = index_pos
            self.next_index_position += 1
        
        self._save_index()
        return item.id

    async def get_by_id(self, memory_id: str) -> Optional[UnifiedMemoryItem]:
        """
        Retrieve a specific memory item by its ID.
        """
        if memory_id in self.memory_id_to_index:
            index_pos = self.memory_id_to_index[memory_id]
            return self.id_to_memory.get(index_pos)
        return None

    async def query(self, filter_params: MemoryQueryFilter) -> MemorySearchResult:
        """
        Query memory items using semantic search and filters.
        """
        start_time = datetime.now()
        
        if filter_params.content_search:
            # Semantic search using FAISS
            query_embedding = self._get_embedding(filter_params.content_search)
            query_embedding_2d = query_embedding.reshape(1, -1).astype('float32')
            
            # Search for similar items
            k = min(filter_params.limit, self.index.ntotal) if self.index.ntotal > 0 else 0
            if k > 0:
                distances, indices = self.index.search(query_embedding_2d, k)
                
                results = []
                for i, idx in enumerate(indices[0]):
                    if idx != -1 and idx in self.id_to_memory:  # -1 indicates no match found
                        item = self.id_to_memory[idx]
                        # Add similarity score as metadata
                        item_copy = UnifiedMemoryItem(
                            id=item.id,
                            content=item.content,
                            memory_type=item.memory_type,
                            tier_source=item.tier_source,
                            tags=item.tags,
                            metadata={**item.metadata, 'similarity_score': float(distances[0][i])},
                            timestamp=item.timestamp,
                            retention_policy=item.retention_policy,
                            access_count=item.access_count,
                            last_accessed=item.last_accessed
                        )
                        results.append(item_copy)
            else:
                results = []
        else:
            # Return all items if no search query
            results = list(self.id_to_memory.values())[:filter_params.limit]
        
        # Apply additional filters
        if filter_params.memory_types:
            results = [r for r in results if r.memory_type in filter_params.memory_types]
        
        if filter_params.tier_sources:
            results = [r for r in results if r.tier_source in filter_params.tier_sources]
        
        if filter_params.tags:
            results = [r for r in results if any(tag in r.tags for tag in filter_params.tags)]
        
        if filter_params.start_time:
            results = [r for r in results if r.timestamp >= filter_params.start_time]
        
        if filter_params.end_time:
            results = [r for r in results if r.timestamp <= filter_params.end_time]
        
        # Limit results
        results = results[:filter_params.limit]
        
        search_time = (datetime.now() - start_time).total_seconds() * 1000
        
        return MemorySearchResult(
            items=results,
            total_count=len(results),
            search_time_ms=search_time,
            query_filter=filter_params
        )

    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a memory item with given properties.
        Note: Content updates will require re-embedding and index rebuild.
        """
        if memory_id not in self.memory_id_to_index:
            return False
        
        index_pos = self.memory_id_to_index[memory_id]
        item = self.id_to_memory[index_pos]
        
        content_changed = False
        for key, value in updates.items():
            if key == 'content' and value != item.content:
                content_changed = True
            setattr(item, key, value)
        
        # If content changed, we need to update the embedding
        if content_changed:
            # For simplicity, we'll save the item which will update metadata
            # but won't update the embedding in the index. A full rebuild would be needed.
            # In a production system, you might want to implement incremental updates.
            print("Warning: Content update detected. Consider rebuilding index for accurate semantic search.")
        
        self._save_index()
        return True

    async def delete(self, memory_id: str) -> bool:
        """
        Delete a memory item from the index.
        Note: FAISS doesn't support direct deletion, so we mark as deleted.
        """
        if memory_id not in self.memory_id_to_index:
            return False
        
        index_pos = self.memory_id_to_index[memory_id]
        
        # Remove from our metadata mappings
        del self.id_to_memory[index_pos]
        del self.memory_id_to_index[memory_id]
        
        # Note: The vector remains in FAISS index but won't be returned
        # A full rebuild would be needed to actually remove it from the index
        
        self._save_index()
        return True

    async def batch_save(self, items: List[UnifiedMemoryItem]) -> List[str]:
        """
        Save multiple memory items efficiently.
        """
        embeddings = []
        new_items = []
        
        for item in items:
            if item.id not in self.memory_id_to_index:
                embedding = self._get_embedding(item.content)
                embeddings.append(embedding)
                new_items.append(item)
        
        if embeddings:
            # Add all embeddings at once
            embeddings_array = np.array(embeddings).astype('float32')
            self.index.add(embeddings_array)
            
            # Update metadata for new items
            for item in new_items:
                index_pos = self.next_index_position
                self.id_to_memory[index_pos] = item
                self.memory_id_to_index[item.id] = index_pos
                self.next_index_position += 1
        
        # Update existing items
        for item in items:
            if item.id in self.memory_id_to_index:
                index_pos = self.memory_id_to_index[item.id]
                self.id_to_memory[index_pos] = item
        
        self._save_index()
        return [item.id for item in items]

    async def cleanup_expired(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Remove expired items from memory based on retention policies.
        """
        expired_count = 0
        current_time = datetime.utcnow()
        expired_ids = []
        
        for index_pos, item in self.id_to_memory.items():
            # Simple time-based expiration (24 hours as example)
            if (current_time - item.timestamp).total_seconds() > 24 * 3600:
                expired_ids.append(item.id)
                expired_count += 1
        
        if not dry_run:
            for memory_id in expired_ids:
                await self.delete(memory_id)
        
        return {'expired_count': expired_count}

    async def semantic_search(self, 
                            query: str, 
                            memory_types: Optional[List] = None,
                            tier_sources: Optional[List[str]] = None,
                            limit: int = 10) -> MemorySearchResult:
        """
        Perform semantic search using vector embeddings.
        """
        # Use the existing query method with content_search which does semantic search
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
        return {
            'total_items': len(self.id_to_memory),
            'faiss_index_size': self.index.ntotal if self.index else 0,
            'embedding_dimension': self.embedding_dim,
            'storage_type': 'FAISS',
            'embedding_model': self.embedding_model.get_sentence_embedding_dimension()
        }

    def rebuild_index(self):
        """
        Rebuild the FAISS index from scratch.
        Useful after many deletions or to optimize the index.
        """
        if not self.id_to_memory:
            self._create_new_index()
            return
        
        # Get all current items and their embeddings
        items = list(self.id_to_memory.values())
        embeddings = []
        
        for item in items:
            embedding = self._get_embedding(item.content)
            embeddings.append(embedding)
        
        # Create new index
        self._create_new_index()
        
        if embeddings:
            embeddings_array = np.array(embeddings).astype('float32')
            self.index.add(embeddings_array)
            
            # Rebuild metadata mappings
            for i, item in enumerate(items):
                self.id_to_memory[i] = item
                self.memory_id_to_index[item.id] = i
            
            self.next_index_position = len(items)
        
        self._save_index()
        print(f"Index rebuilt with {len(items)} items")
