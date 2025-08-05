# Link Tier - Advanced Memory & Tools

*Connections between nodes*

## Overview

The Link tier bridges the gap between simple chatbots and complex multi-agent systems. These agents feature advanced memory systems, robust tool ecosystems, and production-ready interfaces.

## Projects

### gob001-mini
- **Production-ready chat application** with FastAPI backend and React frontend
- Advanced features: Multi-persona routing, fallback handling, comprehensive API
- Perfect for: Development assistance, creative projects, research workflows

## Key Characteristics

- ✅ **Production Ready** - FastAPI backend, React frontend
- ✅ **Multi-Persona Routing** - Developer, creative, and utility agents
- ✅ **Advanced Memory** - Session-based with semantic search
- ✅ **Fallback System** - Automatic failover to free models
- ✅ **Comprehensive API** - REST endpoints with documentation
- ✅ **Modern UI** - Terminal-style React interface

## Architecture

```
Frontend (React)     Backend (FastAPI)
├── Terminal UI  ←→  ├── Agent Router
├── Chat Interface   ├── Memory System
└── API Integration  ├── Tool Integration
                     └── Fallback Handler
```

## Getting Started

```bash
cd gob001-mini

# Quick start (recommended)
./start.sh

# Manual setup
conda env create -f environment.yml
conda activate agentic-framework
# Backend: python -m uvicorn main:app --port 8001 --reload
# Frontend: npm run dev
```

## Agent System

- **Main Agent** - Primary orchestrator and router
- **Developer Persona** - Programming and technical queries (low temperature)
- **Creative Persona** - Creative writing and brainstorming (high temperature)  
- **Universal Agents** - Utility, web browsing, embedding support

## When to Use Link Tier

- Need production web interface
- Require multi-persona capabilities
- Want robust error handling
- Building tools for team use
- Need API integration capabilities

## Graduation to Mesh Tier

Consider moving to Mesh tier when you need:
- Multiple coordinating agents
- Complex scheduling and orchestration
- Advanced memory with PII handling
- Modular plugin architecture
