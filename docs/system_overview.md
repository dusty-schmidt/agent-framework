# Agentic System - Network Layers Architecture

A progressive hierarchy of AI agent systems organized by complexity and capability.

## 🌐 Network Layers Tier System

### **Node** - Basic Chatbot
*Single point in network*
- **Location:** `node/`
- **Capabilities:** 
  - Basic conversational AI with vector memory
  - Simple tool integration
  - JSON backup persistence
  - Essential logging and configuration
- **Use Cases:** Personal assistant, simple Q&A, basic automation

### **Link** - Advanced Memory & Tools
*Connections between nodes*
- **Location:** `link/`
- **Capabilities:**
  - Advanced memory systems with semantic search
  - Robust tool ecosystem
  - Multi-persona agent routing (developer, creative)
  - Fallback model handling
  - Production-ready FastAPI backend + React frontend
- **Use Cases:** Development assistant, creative writing, research tool

### **Mesh** - Multi-Agent Systems
*Interconnected network*
- **Location:** `mesh/`
- **Capabilities:**
  - Modular multi-agent architecture
  - Agent coordination and scheduling
  - Advanced memory with PII handling
  - Separate backend/frontend with comprehensive docs
  - Phase-based development approach
- **Use Cases:** Complex project management, team coordination, enterprise solutions

### **Grid** - Self-Improving Systems
*Complete infrastructure*
- **Location:** `grid/`
- **Capabilities:**
  - Unified framework combining all previous features
  - Plugin system for unlimited extensibility
  - Advanced memory with retention policies
  - Self-improving and adaptive capabilities
  - Production deployment ready
- **Use Cases:** Autonomous systems, large-scale operations, evolving AI assistants

## 🚀 Getting Started

Each tier builds upon the previous, but can be used independently:

```bash
# Basic chatbot
cd node/gob-001-nano && python run_agent.py

# Advanced system with UI
cd link/gob001-mini && ./start.sh

# Multi-agent framework
cd mesh/gob01 && # See mesh/gob01/README.md

# Full unified system
cd grid/gob01-unified && ./start.sh
```

## 📁 Project Structure

```
agentic system/
├── node/                    # Node tier - Basic chatbots
│   ├── gob-001-nano/       # Original Gemini chatbot
│   └── gob-002-nano/       # Enhanced with TUI
├── link/                   # Link tier - Advanced memory & tools
│   └── gob001-mini/        # Production-ready chat app
├── mesh/                   # Mesh tier - Multi-agent systems
│   └── gob01/              # Modular framework
├── grid/                   # Grid tier - Self-improving systems
│   └── gob01-unified/      # Unified advanced framework
├── misc/                   # Experimental and utility scripts
├── agent_naming.toml       # Agent naming conventions
├── models.toml            # Model configurations
└── README.md              # This file
```

## 🔧 Development Philosophy

- **Progressive Complexity:** Start simple, add sophistication incrementally
- **Modular Design:** Each tier maintains clean separation of concerns  
- **Production Ready:** Higher tiers include deployment and monitoring
- **Extensible:** Plugin systems and modular architectures throughout

## 🎯 Next Steps

- Implement cross-tier communication protocols
- Add tier migration tools
- Develop standardized plugin interfaces
- Create unified monitoring dashboard

---

*Network Layers: From single nodes to intelligent grids*
