"""
Behavior types and data structures for the behavior system.

Defines behavior triggers, contexts, and core behavior structure.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class BehaviorTrigger(str, Enum):
    """Types of behavior triggers"""
    USER_MESSAGE = "user_message"
    SYSTEM_EVENT = "system_event"
    SCHEDULED = "scheduled"
    ERROR_OCCURRED = "error_occurred"
    TASK_COMPLETED = "task_completed"
    MEMORY_UPDATED = "memory_updated"
    PLUGIN_EVENT = "plugin_event"


class BehaviorPriority(int, Enum):
    """Behavior execution priority"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


class BehaviorContext(BaseModel):
    """Context information for behavior execution"""
    trigger: BehaviorTrigger
    event_data: Dict[str, Any] = Field(default_factory=dict)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    agent_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class Behavior(BaseModel):
    """Core behavior structure"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Human-readable behavior name")
    description: str = Field(..., description="Behavior description")
    
    # Trigger configuration
    triggers: List[BehaviorTrigger] = Field(..., description="Events that trigger this behavior")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Conditions for execution")
    priority: BehaviorPriority = BehaviorPriority.NORMAL
    
    # Execution details
    handler_class: str = Field(..., description="Class that handles this behavior")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    
    # State and lifecycle
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_executed: Optional[datetime] = None
    execution_count: int = 0
    
    # Metadata
    tags: List[str] = Field(default_factory=list)
    source: str = "system"  # user, plugin, system
    version: str = "1.0.0"
    
    def should_execute(self, context: BehaviorContext) -> bool:
        """Check if behavior should execute given the context"""
        if not self.enabled:
            return False
            
        if context.trigger not in self.triggers:
            return False
            
        # Check conditions (simplified - would need proper condition evaluation)
        return True
