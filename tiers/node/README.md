# Node Tier - Basic Chatbots

*Single point in network*

## Overview

The Node tier represents the foundation of the Network Layers architecture - simple, focused chatbots that excel at basic conversational AI with essential memory and tool capabilities.

## Projects

### gob-001-nano
- **Original Gemini chatbot** with vector memory
- Core features: Vector memory, JSON backup, basic tools
- Perfect for: Learning, simple automation, personal assistant

### gob-002-nano  
- **Enhanced version** with Terminal UI capabilities
- Additional features: TUI interface, multi-agent foundations
- Perfect for: Interactive development, terminal-based workflows

## Key Characteristics

- ✅ **Simplicity** - Minimal setup, easy to understand
- ✅ **Vector Memory** - Semantic search capabilities
- ✅ **Tool Integration** - Basic calculator, memory tools
- ✅ **Logging** - Essential debugging and monitoring
- ✅ **Configuration** - JSON-based config management

## Getting Started

```bash
# Run basic chatbot
cd gob-001-nano
python run_agent.py

# Run enhanced version with TUI
cd gob-002-nano
python tui_multiagent.py
```

## When to Use Node Tier

- Learning AI agent development
- Building simple personal assistants
- Prototyping conversational interfaces
- Need lightweight, focused solutions

## Graduation to Link Tier

Consider moving to Link tier when you need:
- Production web interface
- Multi-persona routing
- Advanced fallback handling
- Robust error handling and monitoring
