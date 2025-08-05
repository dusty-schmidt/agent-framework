"""
Task types and data structures for the scheduler system.

Defines task priorities, statuses, and core task structure.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from pydantic import BaseModel, Field
from enum import Enum
import uuid


class TaskPriority(int, Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4
    BACKGROUND = 5


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    PAUSED = "paused"


class TaskType(str, Enum):
    """Types of tasks"""
    AGENT_EXECUTION = "agent_execution"
    MEMORY_OPERATION = "memory_operation"
    TOOL_EXECUTION = "tool_execution"
    SYSTEM_MAINTENANCE = "system_maintenance"
    USER_REQUEST = "user_request"


class Task(BaseModel):
    """Core task structure for the scheduler"""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str = Field(..., description="Human-readable task name")
    task_type: TaskType
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    
    # Execution details
    agent_id: Optional[str] = None
    tool_name: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    scheduled_for: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    timeout: Optional[timedelta] = None
    
    # Dependencies and relationships
    depends_on: List[str] = Field(default_factory=list, description="Task IDs this task depends on")
    blocks: List[str] = Field(default_factory=list, description="Task IDs this task blocks")
    parent_task_id: Optional[str] = None
    subtasks: List[str] = Field(default_factory=list)
    
    # Resource requirements
    required_resources: Dict[str, Any] = Field(default_factory=dict)
    estimated_duration: Optional[timedelta] = None
    max_retries: int = 3
    retry_count: int = 0
    
    # Results and error handling
    result: Optional[Any] = None
    error: Optional[str] = None
    logs: List[str] = Field(default_factory=list)
    
    # Metadata
    tags: List[str] = Field(default_factory=list)
    source: str = "system"  # user, agent, system
    
    def is_ready_to_run(self) -> bool:
        """Check if task is ready for execution"""
        if self.status != TaskStatus.PENDING:
            return False
            
        if self.scheduled_for and self.scheduled_for > datetime.utcnow():
            return False
            
        # Check dependencies (simplified - would need scheduler context)
        return len(self.depends_on) == 0
    
    def can_retry(self) -> bool:
        """Check if task can be retried"""
        return self.retry_count < self.max_retries and self.status == TaskStatus.FAILED
    
    def add_log(self, message: str):
        """Add a log entry"""
        timestamp = datetime.utcnow().isoformat()
        self.logs.append(f"[{timestamp}] {message}")


class TaskResult(BaseModel):
    """Result of task execution"""
    task_id: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time: Optional[timedelta] = None
    resource_usage: Dict[str, Any] = Field(default_factory=dict)
