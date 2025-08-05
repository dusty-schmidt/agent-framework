from typing import List, Dict, Protocol
import os, json, logging
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Configure logging for memory operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MemorySystem')


class MemoryProvider(Protocol):
    def load(self) -> List[Dict]: ...
    def save(self, history: List[Dict]) -> None: ...

class InMemoryMemory:
    def __init__(self): self._store = []
    def load(self): return self._store.copy()
    def save(self, history): self._store = history.copy()

class JSONFileMemory:
    def __init__(self, path="chat_history.json"): self.path = path
    def load(self):
        if not os.path.exists(self.path): return []
        with open(self.path, "r") as f: return json.load(f)
    def save(self, history):
        with open(self.path, "w") as f: json.dump(history, f, indent=2)





class VectorMemory:
    def __init__(self, embedding_model="all-MiniLM-L6-v2", persist_path=None):
        logger.info(f"Initializing VectorMemory with model: {embedding_model}")
        self.texts = []
        self.embeddings = []
        self.model = SentenceTransformer(embedding_model)
        self.index = None
        self.persist_path = persist_path
        logger.info(f"VectorMemory initialized. Persistence: {'enabled' if persist_path else 'disabled'}")
        
        # Load from disk if persistence is enabled
        if self.persist_path:
            self._load_from_disk()

    def load(self) -> List[Dict]:
        logger.info(f"Loading memory. Total texts stored: {len(self.texts)}")
        # Return as normal chat history for compatibility
        memory_items = [{"role": "memory", "content": t} for t in self.texts]
        logger.debug(f"Returning {len(memory_items)} memory items as chat history")
        return memory_items

    def save(self, history: List[Dict]) -> None:
        logger.info(f"Saving history with {len(history)} items")
        
        # Save only user/assistant content
        old_count = len(self.texts)
        self.texts = [x["content"] for x in history if x.get("role") in ("user", "assistant")]
        new_count = len(self.texts)
        
        logger.info(f"Extracted {new_count} texts from history (was {old_count})")
        
        if not self.texts:
            logger.warning("No texts to embed")
            return
            
        logger.info("Generating embeddings...")
        self.embeddings = self.model.encode(self.texts).tolist()
        logger.info(f"Generated {len(self.embeddings)} embeddings, dimension: {len(self.embeddings[0]) if self.embeddings else 0}")
        
        if self.embeddings:
            logger.info("Building FAISS index...")
            arr = np.array(self.embeddings).astype('float32')
            self.index = faiss.IndexFlatL2(arr.shape[1])
            self.index.add(arr)
            logger.info(f"FAISS index built with {self.index.ntotal} vectors")
            
            # Persist to disk if enabled
            if self.persist_path:
                self._save_to_disk()
        else:
            logger.warning("No embeddings generated")

    def semantic_search(self, query: str, top_k: int = 3):
        logger.info(f"Performing semantic search for: '{query[:50]}...' (top_k={top_k})")
        
        if not self.index or not self.texts:
            logger.warning("No index or texts available for search")
            return []
            
        logger.debug("Encoding query...")
        q_emb = self.model.encode([query]).astype('float32')
        
        logger.debug("Searching FAISS index...")
        D, I = self.index.search(q_emb, min(top_k, len(self.texts)))
        
        results = [self.texts[i] for i in I[0] if i < len(self.texts)]
        logger.info(f"Found {len(results)} relevant memories")
        
        # Log search results with distances
        for i, (distance, text_idx) in enumerate(zip(D[0], I[0])):
            if text_idx < len(self.texts):
                logger.debug(f"Result {i+1}: distance={distance:.4f}, text='{self.texts[text_idx][:100]}...'")
        
        return results
    
    def _save_to_disk(self):
        """Save embeddings and texts to disk for persistence"""
        try:
            data = {
                'texts': self.texts,
                'embeddings': self.embeddings
            }
            with open(self.persist_path, 'w') as f:
                json.dump(data, f)
            logger.info(f"Memory persisted to {self.persist_path}")
        except Exception as e:
            logger.error(f"Failed to persist memory: {e}")
    
    def _load_from_disk(self):
        """Load embeddings and texts from disk"""
        if not os.path.exists(self.persist_path):
            logger.info(f"No persistent memory found at {self.persist_path}")
            return
            
        try:
            with open(self.persist_path, 'r') as f:
                data = json.load(f)
            
            self.texts = data.get('texts', [])
            self.embeddings = data.get('embeddings', [])
            
            if self.embeddings:
                arr = np.array(self.embeddings).astype('float32')
                self.index = faiss.IndexFlatL2(arr.shape[1])
                self.index.add(arr)
                logger.info(f"Loaded {len(self.texts)} texts and {len(self.embeddings)} embeddings from disk")
            else:
                logger.info("No embeddings found in persistent storage")
                
        except Exception as e:
            logger.error(f"Failed to load persistent memory: {e}")
