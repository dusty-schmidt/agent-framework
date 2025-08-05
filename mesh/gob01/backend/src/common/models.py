from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class MemoryItem(BaseModel):
    id: str
    type: str
    tags: List[str] = []
    content: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}

class MemorySaveRequest(BaseModel):
    type: str
    tags: List[str] = []
    content: Dict[str, Any]
    metadata: Dict[str, Any] = {}

class MemoryQueryResponse(BaseModel):
    items: List[MemoryItem]

class BehaviorAdjustRequest(BaseModel):
    rules: List[str] = []
    scope: str = Field(default="global")

class AgentRunRequest(BaseModel):
    instruction: str
    tools: Optional[List[str]] = None
    timeout_ms: Optional[int] = 10000

class AgentRunResponse(BaseModel):
    run_id: str
    status: str = "started"

class ErrorResponse(BaseModel):
    error: Dict[str, Any]
