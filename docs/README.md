# Agentic System Documentation

Welcome to the Agentic System documentation. This directory contains comprehensive guides and documentation for the multi-tier agent system.

## 📚 Documentation Structure

### Core Documentation
- **[System Overview](system_overview.md)** - High-level overview of the agentic system
- **[TUI Guide](tui_guide.md)** - Complete guide to the Terminal User Interface
- **[Architecture](architecture.md)** - System architecture and design principles
- **[Getting Started](getting_started.md)** - Quick start guide for new users

### Tier Documentation
- **[Node Tier](tiers/node_tier.md)** - Single-agent chatbot with basic tools
- **[Link Tier](tiers/link_tier.md)** - Production-ready multi-persona agent system
- **[Mesh Tier](tiers/mesh_tier.md)** - Multi-agent coordination with WebSocket events
- **[Grid Tier](tiers/grid_tier.md)** - Self-improving unified framework with plugins

### Development
- **[Development Guide](development/development_guide.md)** - How to develop and extend the system
- **[API Reference](development/api_reference.md)** - API documentation
- **[Contributing](development/contributing.md)** - How to contribute to the project

### Operations
- **[Deployment](operations/deployment.md)** - How to deploy the system
- **[Monitoring](operations/monitoring.md)** - System monitoring and logging
- **[Troubleshooting](operations/troubleshooting.md)** - Common issues and solutions

## 🚀 Quick Start

1. **Launch the TUI Manager**:
   ```bash
   cd "agentic system"
   python start_tui.py
   ```

2. **Navigate the Interface**:
   - Use Tab to switch between tabs
   - Click buttons to control tiers
   - Monitor status in real-time

3. **Check Logs**:
   ```bash
   tail -f logs/tui.log
   ```

## 🏗️ System Architecture

The agentic system is organized into multiple tiers:

```
agentic system/
├── frontend/           # User interfaces
│   └── tui/           # Terminal User Interface
├── docs/              # Documentation
├── logs/              # System logs
├── node/              # Node tier (single agent)
├── link/              # Link tier (multi-persona)
├── mesh/              # Mesh tier (coordination)
├── grid/              # Grid tier (self-improving)
└── misc/              # Utilities and tools
```

## 📖 Key Concepts

### Tiers
The system is organized into four main tiers, each with increasing complexity:
- **Node**: Basic single-agent functionality
- **Link**: Multi-persona agent interactions
- **Mesh**: Coordinated multi-agent systems
- **Grid**: Self-improving unified framework

### 80/20 Principle
The system follows the 80/20 principle - focusing on the 20% of features that provide 80% of the value:
- Essential tier management
- Real-time monitoring
- Centralized logging
- Simple, intuitive interface

### Modular Design
- **Interface-agnostic**: Core logic separated from UI
- **Agent-guided**: Intelligent automation where possible
- **User-first**: Designed around user workflows
- **Reversible changes**: All actions can be undone

## 🔧 Configuration

Key configuration files:
- `models.toml` - Model configurations
- `agent_naming.toml` - Agent naming conventions
- `frontend/tui/requirements_tui.txt` - TUI dependencies

## 📊 Monitoring

The system provides comprehensive logging:
- Real-time status monitoring
- Centralized log aggregation
- Session tracking
- Error reporting

## 🤝 Contributing

See [Contributing Guide](development/contributing.md) for details on:
- Code style guidelines
- Testing requirements
- Pull request process
- Development setup

## 📞 Support

For issues and questions:
1. Check the [Troubleshooting Guide](operations/troubleshooting.md)
2. Review the logs in `logs/` directory
3. Consult the relevant tier documentation

---

*This documentation follows the principle of progressive disclosure - start with the basics and dive deeper as needed.*
