"""
Memory types and data structures for the unified agent framework.

Based on gob01's memory specification:
- User Data: user-provided facts (names, API keys)
- Fragments: auto-updated conversation nuggets
- Solutions: successful outcomes; code artifacts promotable to tools
- Metadata: ids, timestamps, pii flags, retention policy, tags
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class MemoryType(str, Enum):
    """Types of memory entries"""
    USER_DATA = "user_data"
    FRAGMENT = "fragment"
    SOLUTION = "solution"


class RetentionPolicy(str, Enum):
    """Memory retention policies"""
    PERMANENT = "permanent"
    SESSION = "session"
    TEMPORARY = "temporary"
    AUTO_EXPIRE = "auto_expire"


class MemoryMetadata(BaseModel):
    """Metadata for memory entries"""
    id: str = Field(..., description="Unique identifier")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    memory_type: MemoryType
    tags: List[str] = Field(default_factory=list)
    retention_policy: RetentionPolicy = RetentionPolicy.AUTO_EXPIRE
    has_pii: bool = Field(default=False, description="Contains personally identifiable information")
    source: Optional[str] = Field(None, description="Source of the memory (agent, user, system)")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence score")
    access_count: int = Field(default=0, description="Number of times accessed")
    last_accessed: Optional[datetime] = None


class MemoryFragment(BaseModel):
    """Auto-updated conversation nuggets"""
    metadata: MemoryMetadata
    content: str = Field(..., description="The memory content")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")
    summary: Optional[str] = Field(None, description="Compressed summary for aging memories")
    related_fragments: List[str] = Field(default_factory=list, description="IDs of related fragments")


class UserData(BaseModel):
    """User-provided facts and preferences"""
    metadata: MemoryMetadata
    key: str = Field(..., description="Data key (e.g., 'name', 'api_key')")
    value: Any = Field(..., description="Data value")
    category: str = Field(..., description="Category (e.g., 'personal', 'credentials', 'preferences')")
    encrypted: bool = Field(default=False, description="Whether the value is encrypted")


class Solution(BaseModel):
    """Successful outcomes and code artifacts"""
    metadata: MemoryMetadata
    problem_description: str = Field(..., description="Description of the problem solved")
    solution_content: str = Field(..., description="The solution (code, instructions, etc.)")
    solution_type: str = Field(..., description="Type of solution (code, process, configuration)")
    success_metrics: Dict[str, Any] = Field(default_factory=dict, description="Metrics proving success")
    promotable_to_tool: bool = Field(default=False, description="Can be promoted to a reusable tool")
    usage_count: int = Field(default=0, description="Number of times this solution was reused")
