"""
Core memory interface and data models for the unified memory system.

Defines the contract for memory providers and standardized data structures
that work consistently across all tiers of the agent framework.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
import uuid


class MemoryType(str, Enum):
    """Types of memory entries in the unified system"""
    USER_DATA = "user_data"           # User facts, preferences, API keys
    CONVERSATION = "conversation"     # Chat history, interactions
    FRAGMENT = "fragment"            # Auto-updated conversation nuggets
    SOLUTION = "solution"            # Successful outcomes, code artifacts
    SYSTEM = "system"                # System state, configurations
    SYSTEM_STATE = "system_state"    # System state, configurations (alias)
    KNOWLEDGE = "knowledge"          # External facts, documentation
    USER_PREFERENCE = "user_preference"  # User preferences
    ERROR_LOG = "error_log"          # Error logs
    TASK = "task"                    # Tasks and todos


class RetentionPolicy(str, Enum):
    """Memory retention policies"""
    PERMANENT = "permanent"          # Never delete
    SESSION = "session"              # Delete at session end
    TEMPORARY = "temporary"          # Delete after short time (hours)
    AUTO_EXPIRE = "auto_expire"      # Smart expiration based on usage (days/weeks)
    TIER_SPECIFIC = "tier_specific"  # Each tier manages its own


class MemoryPriority(str, Enum):
    """Priority levels for memory items"""
    CRITICAL = "critical"    # Essential data (user preferences, API keys)
    HIGH = "high"           # Important conversations, solutions
    MEDIUM = "medium"       # Regular interactions
    LOW = "low"            # Temporary data, system logs


class UnifiedMemoryItem(BaseModel):
    """Standardized memory item that works across all tiers"""
    
    # Core identification
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str = Field(..., description="The main memory content")
    
    # Classification
    memory_type: MemoryType = Field(..., description="Type of memory")
    tier_source: str = Field(..., description="Which tier created this memory")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Categorization tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    
    # Timestamps
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Creation time")
    last_accessed: Optional[datetime] = Field(None, description="Last access time")
    last_modified: Optional[datetime] = Field(None, description="Last modification time")
    
    # Policies
    retention_policy: RetentionPolicy = Field(default=RetentionPolicy.AUTO_EXPIRE)
    priority: MemoryPriority = Field(default=MemoryPriority.MEDIUM)
    
    # Usage tracking
    access_count: int = Field(default=0, description="Number of times accessed")
    usage_score: float = Field(default=0.0, description="Weighted usage score")
    
    # Vector embeddings for semantic search
    embeddings: Optional[List[float]] = Field(None, description="Vector embeddings")
    embedding_model: Optional[str] = Field(None, description="Model used for embeddings")
    
    # Relationships
    related_items: List[str] = Field(default_factory=list, description="Related memory IDs")
    parent_id: Optional[str] = Field(None, description="Parent memory for hierarchical data")
    
    # Quality metrics
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score")
    relevance_decay: float = Field(default=0.0, description="Relevance decay rate over time")
    
    # Privacy and security
    has_pii: bool = Field(default=False, description="Contains PII")
    encryption_key: Optional[str] = Field(None, description="Encryption key if encrypted")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class MemoryQueryFilter(BaseModel):
    """Filter criteria for memory queries"""
    
    # Content filters
    content_search: Optional[str] = None
    semantic_query: Optional[str] = None
    
    # Type and tier filters
    memory_types: Optional[List[MemoryType]] = None
    tier_sources: Optional[List[str]] = None
    
    # Tag and metadata filters
    tags: Optional[List[str]] = None
    metadata_filters: Optional[Dict[str, Any]] = None
    
    # Time filters
    start_time: Optional[datetime] = None  # For compatibility
    end_time: Optional[datetime] = None    # For compatibility
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    accessed_after: Optional[datetime] = None
    
    # Quality filters
    min_confidence: Optional[float] = None
    min_usage_score: Optional[float] = None
    priorities: Optional[List[MemoryPriority]] = None
    
    # Relationship filters
    related_to: Optional[str] = None
    parent_id: Optional[str] = None
    
    # Result controls
    limit: int = Field(default=10, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)
    sort_by: str = Field(default="timestamp", pattern="^(timestamp|usage_score|relevance|access_count)$")
    sort_desc: bool = Field(default=True)


class MemorySearchResult(BaseModel):
    """Result from memory search operations"""
    
    items: List[UnifiedMemoryItem]
    total_count: int
    search_time_ms: float
    query_filter: MemoryQueryFilter
    
    # For semantic search
    semantic_scores: Optional[List[float]] = None
    query_embedding: Optional[List[float]] = None


class IUnifiedMemoryProvider(ABC):
    """
    Abstract interface for unified memory providers.
    
    This interface defines the contract that all memory storage backends
    must implement to work with the unified memory system.
    """
    
    @abstractmethod
    async def save(self, item: UnifiedMemoryItem) -> str:
        """
        Save a memory item and return its ID.
        
        Args:
            item: The memory item to save
            
        Returns:
            str: The unique ID of the saved item
            
        Raises:
            MemoryStorageException: If save operation fails
        """
        pass
    
    @abstractmethod
    async def get_by_id(self, memory_id: str) -> Optional[UnifiedMemoryItem]:
        """
        Retrieve a specific memory item by ID.
        
        Args:
            memory_id: The unique ID of the memory item
            
        Returns:
            UnifiedMemoryItem or None if not found
        """
        pass
    
    @abstractmethod
    async def query(self, filter_params: MemoryQueryFilter) -> MemorySearchResult:
        """
        Query memory items with advanced filtering.
        
        Args:
            filter_params: Comprehensive filter criteria
            
        Returns:
            MemorySearchResult with matching items and metadata
        """
        pass
    
    @abstractmethod
    async def semantic_search(self, 
                            query: str, 
                            memory_types: Optional[List[MemoryType]] = None,
                            tier_sources: Optional[List[str]] = None,
                            limit: int = 10) -> MemorySearchResult:
        """
        Perform vector-based semantic search.
        
        Args:
            query: Natural language search query
            memory_types: Filter by memory types
            tier_sources: Filter by tier sources
            limit: Maximum results to return
            
        Returns:
            MemorySearchResult with semantically similar items
        """
        pass
    
    @abstractmethod
    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a memory item.
        
        Args:
            memory_id: ID of item to update
            updates: Dictionary of field updates
            
        Returns:
            bool: True if update successful
        """
        pass
    
    @abstractmethod
    async def delete(self, memory_id: str) -> bool:
        """
        Delete a memory item.
        
        Args:
            memory_id: ID of item to delete
            
        Returns:
            bool: True if deletion successful
        """
        pass
    
    @abstractmethod
    async def batch_save(self, items: List[UnifiedMemoryItem]) -> List[str]:
        """
        Save multiple memory items efficiently.
        
        Args:
            items: List of memory items to save
            
        Returns:
            List[str]: List of saved item IDs
        """
        pass
    
    @abstractmethod
    async def cleanup_expired(self, dry_run: bool = False) -> Dict[str, int]:
        """
        Clean up expired memories based on retention policies.
        
        Args:
            dry_run: If True, return what would be deleted without deleting
            
        Returns:
            Dict with cleanup statistics by retention policy
        """
        pass
    
    @abstractmethod
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get memory system statistics.
        
        Returns:
            Dictionary with storage statistics
        """
        pass


class MemoryStorageException(Exception):
    """Exception raised by memory storage operations"""
    
    def __init__(self, message: str, operation: str = None, memory_id: str = None):
        super().__init__(message)
        self.operation = operation
        self.memory_id = memory_id
