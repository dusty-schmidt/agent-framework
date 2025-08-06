"""
Plugin system for the unified agent framework.

Enables extensibility and modularity by allowing dynamic loading of:
- Agent behaviors
- Tools and utilities
- API endpoints
- Memory providers
- UI components
"""

from .plugin_interface import IPlugin, PluginMetadata
from .plugin_manager import PluginManager
from .plugin_registry import plugin_registry

__all__ = [
    'IPlugin',
    'PluginMetadata', 
    'PluginManager',
    'plugin_registry'
]
