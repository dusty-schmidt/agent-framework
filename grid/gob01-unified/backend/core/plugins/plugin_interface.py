"""
Plugin interface for the unified agent framework.

Defines the contract for plugins to extend system functionality.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from fastapi import APIRouter


class PluginMetadata(BaseModel):
    """Metadata for plugins"""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str] = []
    api_version: str = "1.0.0"
    enabled: bool = True


class IPlugin(ABC):
    """Base interface for all plugins"""
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """Plugin metadata"""
        pass
    
    @abstractmethod
    async def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the plugin with configuration"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> bool:
        """Clean shutdown of the plugin"""
        pass
    
    def register_tools(self) -> List[Any]:
        """Register tools provided by this plugin"""
        return []
    
    def register_behaviors(self) -> List[Any]:
        """Register agent behaviors provided by this plugin"""
        return []
    
    def register_endpoints(self) -> Optional[APIRouter]:
        """Register API endpoints provided by this plugin"""
        return None
    
    def register_memory_providers(self) -> List[Any]:
        """Register memory providers offered by this plugin"""
        return []
    
    def get_config_schema(self) -> Dict[str, Any]:
        """Return JSON schema for plugin configuration"""
        return {}


class AgentPlugin(IPlugin):
    """Plugin specifically for agent extensions"""
    
    @abstractmethod
    def get_agent_class(self) -> type:
        """Return the agent class provided by this plugin"""
        pass


class ToolPlugin(IPlugin):
    """Plugin specifically for tool extensions"""
    
    @abstractmethod
    def get_tool_classes(self) -> List[type]:
        """Return tool classes provided by this plugin"""
        pass


class MemoryPlugin(IPlugin):
    """Plugin specifically for memory system extensions"""
    
    @abstractmethod
    def get_memory_provider_class(self) -> type:
        """Return memory provider class"""
        pass
