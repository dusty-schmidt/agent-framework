"""
System Prompt Manager - Unified prompt generation for all tiers.

Manages the centralized system prompt that all tiers share, with dynamic
context injection and tier-specific customizations.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class SystemPromptManager:
    """
    Manages unified system prompts across all tiers.
    
    Provides a single source of truth for system behavior with
    tier-specific customizations and dynamic context injection.
    """
    
    def __init__(self, config_path: Path):
        """Initialize system prompt manager."""
        self.config_path = Path(config_path)
        self.config_path.mkdir(parents=True, exist_ok=True)
        
        # Load or create base configuration
        self.config_file = self.config_path / "system_prompts.yaml"
        self.prompt_config = self._load_prompt_config()
        
        # Cache for built prompts
        self.prompt_cache = {}
    
    def _load_prompt_config(self) -> Dict[str, Any]:
        """Load system prompt configuration from file."""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            # Create default configuration
            default_config = self._create_default_config()
            self._save_config(default_config)
            return default_config
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default system prompt configuration."""
        return {
            "base_prompt": {
                "identity": "You are an intelligent AI assistant in a multi-tier agent framework called the Agentic System.",
                "core_principles": [
                    "Be helpful, accurate, and thoughtful in all responses",
                    "Leverage your memory system to provide contextual responses", 
                    "Use available tools when they would be beneficial",
                    "Be transparent about your capabilities and limitations",
                    "Prioritize user safety and privacy",
                    "Maintain consistency across different interaction contexts"
                ],
                "capabilities": [
                    "Access to persistent memory across sessions",
                    "Knowledge retrieval and semantic search",
                    "Tool usage for enhanced functionality",
                    "Context-aware response generation",
                    "Learning from successful solutions"
                ],
                "behavior_guidelines": [
                    "Always consider relevant memories when formulating responses",
                    "Suggest tools when they could enhance your response",
                    "Ask clarifying questions when user intent is unclear",
                    "Provide explanations for your reasoning when helpful",
                    "Remember user preferences and apply them consistently"
                ]
            },
            "tier_customizations": {
                "node": {
                    "focus": "single-task completion",
                    "style": "concise and direct",
                    "additional_guidelines": [
                        "Focus on the specific task at hand",
                        "Minimize complexity in responses",
                        "Be efficient with token usage"
                    ]
                },
                "link": {
                    "focus": "multi-persona capability management",
                    "style": "balanced and comprehensive",
                    "additional_guidelines": [
                        "Consider which persona or capability is most appropriate",
                        "Balance multiple aspects of complex requests",
                        "Route tasks to the most suitable agent when applicable"
                    ]
                },
                "mesh": {
                    "focus": "multi-agent coordination",
                    "style": "collaborative and systematic",
                    "additional_guidelines": [
                        "Think about how different agents could work together",
                        "Consider workflow orchestration and task dependencies",
                        "Facilitate communication between different system components"
                    ]
                },
                "grid": {
                    "focus": "advanced reasoning and self-improvement",
                    "style": "sophisticated and adaptive",
                    "additional_guidelines": [
                        "Leverage all available capabilities and plugins",
                        "Consider long-term implications and learning opportunities",
                        "Adapt behavior based on accumulated experience",
                        "Propose system improvements when relevant"
                    ]
                }
            },
            "context_sections": {
                "user_context": {
                    "enabled": True,
                    "template": "User Context:\\n{context}\\n"
                },
                "memory_context": {
                    "enabled": True,
                    "template": "Relevant Memories:\\n{memories}\\n"
                },
                "tool_context": {
                    "enabled": True,
                    "template": "Available Tools:\\n{tools}\\n"
                },
                "knowledge_context": {
                    "enabled": True,
                    "template": "Relevant Knowledge:\\n{knowledge}\\n"
                },
                "session_context": {
                    "enabled": True,
                    "template": "Session: {session_id} | Tier: {tier_name}\\n"
                }
            },
            "dynamic_elements": {
                "timestamp": True,
                "session_info": True,
                "tier_info": True,
                "memory_stats": False,
                "tool_availability": True
            }
        }
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    def build_system_prompt(self,
                          tier_name: str,
                          user_context: Optional[Dict[str, Any]] = None,
                          memory_context: Optional[List[str]] = None,
                          tool_context: Optional[List[str]] = None,
                          knowledge_context: Optional[List[str]] = None,
                          session_id: str = "default") -> str:
        """
        Build a comprehensive system prompt for a specific tier.
        
        Args:
            tier_name: Name of the requesting tier
            user_context: User preferences and data
            memory_context: Relevant memories
            tool_context: Available tools
            knowledge_context: Relevant knowledge
            session_id: Current session identifier
            
        Returns:
            Complete system prompt string
        """
        
        # Check cache first
        cache_key = f"{tier_name}_{session_id}_{hash(str(user_context))}"
        if cache_key in self.prompt_cache:
            cached_prompt, cached_time = self.prompt_cache[cache_key]
            # Use cache if less than 5 minutes old
            if (datetime.utcnow() - cached_time).seconds < 300:
                return cached_prompt
        
        prompt_parts = []
        
        # 1. Base identity and principles
        base = self.prompt_config["base_prompt"]
        prompt_parts.append(base["identity"])
        prompt_parts.append("\\nCore Principles:")
        for principle in base["core_principles"]:
            prompt_parts.append(f"- {principle}")
        
        # 2. Capabilities overview
        prompt_parts.append("\\nCapabilities:")
        for capability in base["capabilities"]:
            prompt_parts.append(f"- {capability}")
        
        # 3. Tier-specific customization
        if tier_name in self.prompt_config["tier_customizations"]:
            tier_config = self.prompt_config["tier_customizations"][tier_name]
            prompt_parts.append(f"\\nTier-Specific Focus: {tier_config['focus']}")
            prompt_parts.append(f"Response Style: {tier_config['style']}")
            
            if tier_config.get("additional_guidelines"):
                prompt_parts.append("\\nTier-Specific Guidelines:")
                for guideline in tier_config["additional_guidelines"]:
                    prompt_parts.append(f"- {guideline}")
        
        # 4. Dynamic context sections
        context_config = self.prompt_config["context_sections"]
        
        # Session context
        if context_config["session_context"]["enabled"]:
            session_info = context_config["session_context"]["template"].format(
                session_id=session_id,
                tier_name=tier_name
            )
            prompt_parts.append(f"\\n{session_info}")
        
        # User context
        if user_context and context_config["user_context"]["enabled"]:
            user_info = "\\n".join([f"{k}: {v}" for k, v in user_context.items()])
            prompt_parts.append(f"\\n{context_config['user_context']['template'].format(context=user_info)}")
        
        # Memory context
        if memory_context and context_config["memory_context"]["enabled"]:
            memory_info = "\\n".join([f"- {memory}" for memory in memory_context[:5]])
            if memory_info:
                prompt_parts.append(f"\\n{context_config['memory_context']['template'].format(memories=memory_info)}")
        
        # Tool context
        if tool_context and context_config["tool_context"]["enabled"]:
            tool_info = "\\n".join([f"- {tool}" for tool in tool_context[:10]])
            if tool_info:
                prompt_parts.append(f"\\n{context_config['tool_context']['template'].format(tools=tool_info)}")
        
        # Knowledge context
        if knowledge_context and context_config["knowledge_context"]["enabled"]:
            knowledge_info = "\\n".join([f"- {knowledge}" for knowledge in knowledge_context[:3]])
            if knowledge_info:
                prompt_parts.append(f"\\n{context_config['knowledge_context']['template'].format(knowledge=knowledge_info)}")
        
        # 5. Behavior guidelines
        prompt_parts.append("\\nBehavior Guidelines:")
        for guideline in base["behavior_guidelines"]:
            prompt_parts.append(f"- {guideline}")
        
        # 6. Dynamic elements
        dynamic_config = self.prompt_config["dynamic_elements"]
        if dynamic_config.get("timestamp"):
            prompt_parts.append(f"\\nCurrent Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Build final prompt
        final_prompt = "\\n".join(prompt_parts)
        
        # Cache the result
        self.prompt_cache[cache_key] = (final_prompt, datetime.utcnow())
        
        # Limit cache size
        if len(self.prompt_cache) > 100:
            # Remove oldest entries
            sorted_cache = sorted(self.prompt_cache.items(), key=lambda x: x[1][1])
            for key, _ in sorted_cache[:50]:
                del self.prompt_cache[key]
        
        return final_prompt
    
    def update_config(self, updates: Dict[str, Any]):
        """Update prompt configuration."""
        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(self.prompt_config, updates)
        self._save_config(self.prompt_config)
        
        # Clear cache when config changes
        self.prompt_cache.clear()
    
    def get_config(self) -> Dict[str, Any]:
        """Get current prompt configuration."""
        return self.prompt_config.copy()
    
    def reset_to_defaults(self):
        """Reset configuration to defaults."""
        self.prompt_config = self._create_default_config()
        self._save_config(self.prompt_config)
        self.prompt_cache.clear()
