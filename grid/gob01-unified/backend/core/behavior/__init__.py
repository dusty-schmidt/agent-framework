"""
Behavior system for the unified agent framework.

Implements agent behavior management and customization
based on gob01's behavior specification.
"""

from .behavior_system import BehaviorSystem
from .behavior_types import Behavior, BehaviorTrigger, BehaviorContext
from .behavior_interface import IBehavior

__all__ = [
    'BehaviorSystem',
    'Behavior',
    'BehaviorTrigger',
    'BehaviorContext', 
    'IBehavior'
]
