# Agentic System

A modular, interface-agnostic multi-tier agent system designed for progressive complexity and intelligent automation.

## 🚀 Quick Start

```bash
# 1. Create conda environment
conda env create -f environment.yml
conda activate agentic-framework

# 2. Add API key to your zsh config
echo 'export OPENROUTER_API_KEY="your_key_here"' >> ~/.zshrc
source ~/.zshrc

# 3. Test everything works
python tests/complete_test.py

# 4. Start the framework
python main.py                     # Web interface (primary)
python main.py --test             # Web interface with test panels
python main.py --terminal         # Terminal interface
python main.py --validate         # Validate configuration only
```

Navigate with Tab, control tiers with buttons, monitor in real-time.

## 🏗️ System Architecture

The system is organized into four progressive tiers:

```
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ Node Tier   │ │ Link Tier   │ │ Mesh Tier   │ │ Grid Tier   │
│ Single      │ │ Multi-      │ │ Multi-Agent │ │ Self-       │
│ Agent       │ │ Persona     │ │ Coordination│ │ Improving   │
│             │ │             │ │             │ │ Framework   │
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
      ↑               ↑               ↑               ↑
   Basic         Intermediate     Advanced        Expert
```

## 📁 Directory Structure

```
agentic-framework/
├── 📋 config.toml         # Main configuration
├── 🧠 core/              # Framework core components
│   ├── brain/            # Central intelligence
│   ├── memory/           # Unified memory system
│   ├── config/           # System configuration
│   └── data/             # Persistent data & logs
├── 🎯 tiers/             # Agent tier implementations
│   ├── node/             # Node Tier (single agent)
│   ├── link/             # Link Tier (multi-persona)
│   ├── mesh/             # Mesh Tier (coordination)
│   └── grid/             # Grid Tier (self-improving)
├── 🔧 scripts/           # Utilities & setup tools
├── 🧪 tests/             # Test suite
├── 🎨 frontend/          # User interfaces
├── 📚 docs/              # Documentation
└── 🐳 docker/            # Container configuration
```

## ✨ Key Features

### 🎯 **80/20 Principle**
Focus on the 20% of features that provide 80% of the value:
- Essential tier management
- Real-time monitoring  
- Centralized logging
- Intuitive interface

### 🧩 **Modular Design**
- **Interface-agnostic**: Core logic separated from UI
- **Agent-guided**: Intelligent automation where possible
- **User-first**: Designed around user workflows
- **Reversible changes**: All actions can be undone

### 📊 **Comprehensive Monitoring**
- Real-time status indicators (🟢/🔴)
- Centralized logging with rotation
- Session tracking
- Performance monitoring

## 🎮 TUI Interface

The Terminal User Interface provides:

- **Overview Tab**: Monitor all tiers at a glance
- **Individual Tier Tabs**: Detailed control and monitoring
- **Real-time Updates**: Live status and uptime tracking
- **Button Controls**: Start, Stop, Restart, Refresh
- **Notifications**: Success/error feedback

### Navigation
- **Tab**: Switch between tabs
- **Enter**: Activate buttons
- **Ctrl+C**: Exit
- **Mouse**: Click buttons (if supported)

## 🏢 Tier Overview

### Node Tier
- **Purpose**: Single-agent chatbot with basic tools
- **Complexity**: Basic
- **Use Case**: Testing, simple interactions
- **Resources**: Lightweight

### Link Tier
- **Purpose**: Production-ready multi-persona agent system
- **Complexity**: Intermediate
- **Use Case**: Production applications
- **Port**: 8001
- **Resources**: Moderate

### Mesh Tier
- **Purpose**: Multi-agent coordination with WebSocket events
- **Complexity**: Advanced
- **Use Case**: Complex workflows, agent collaboration
- **Port**: 8080
- **Resources**: Higher

### Grid Tier
- **Purpose**: Self-improving unified framework with plugins
- **Complexity**: Expert
- **Use Case**: Advanced AI applications
- **Port**: 8001
- **Resources**: Highest

## 📊 Monitoring & Logging

### Real-time Monitoring
- Status indicators with color coding
- Uptime counters
- Port information
- Process health checks

### Centralized Logging
```bash
logs/
├── tui.log              # TUI manager activities
├── node_tier.log        # Node tier operations
├── link_tier.log        # Link tier operations
├── mesh_tier.log        # Mesh tier operations
├── grid_tier.log        # Grid tier operations
├── system.log           # System-wide events
└── session_*.log        # Session-specific logs
```

### Log Monitoring
```bash
# Follow TUI logs
tail -f logs/tui.log

# Monitor specific tier
tail -f logs/node_tier.log

# View all recent activity
tail -f logs/*.log
```

## 🛠️ Configuration

### Key Files
- `models.toml` - Model configurations
- `frontend/tui/requirements_tui.txt` - TUI dependencies
- `frontend/tui/unified_tui.css` - TUI styling

### Environment
- Python 3.8+
- Terminal with ANSI support
- 4GB+ RAM recommended

## 📚 Documentation

Comprehensive documentation in `docs/`:

- **[Getting Started](docs/getting_started.md)** - Quick start guide
- **[Architecture](docs/architecture.md)** - System design and principles
- **[TUI Guide](docs/tui_guide.md)** - Complete TUI documentation
- **[Tier Guides](docs/tiers/)** - Individual tier documentation
- **[Development](docs/development/)** - Development guides
- **[Operations](docs/operations/)** - Deployment and monitoring

## 🚀 Common Workflows

### Development
1. Start with Node Tier for basic testing
2. Progress to Link Tier for multi-agent development
3. Use Mesh Tier for coordination testing
4. Deploy to Grid Tier for production

### Production
1. Launch required tiers based on needs
2. Monitor in Overview tab
3. Check logs for issues
4. Use Restart for maintenance

### Troubleshooting
1. Check tier status in TUI
2. Review relevant log files
3. Restart problematic tiers
4. Monitor system resources

## 🤝 Contributing

The system is designed for extensibility:

- **New Tiers**: Follow existing patterns
- **New Interfaces**: Implement common management interface
- **New Features**: Use plugin architecture in Grid tier

See [Development Guide](docs/development/development_guide.md) for details.

## 📞 Support

1. Check [Getting Started](docs/getting_started.md)
2. Review [Troubleshooting](docs/operations/troubleshooting.md)
3. Examine logs in `logs/` directory
4. Consult tier-specific documentation

## 🎯 Design Philosophy

> **"Build a modular, interface-agnostic 'nothing app' that adapts to users via agents, plugins, layouts, and memory."**

**Principles:**
- **Modular**: Each component serves a specific purpose
- **Agent-guided**: Intelligent automation where appropriate
- **Interface-neutral**: Core logic independent of presentation
- **User-first**: Designed around actual user workflows
- **Learn-from-use**: System improves based on usage patterns
- **Reversible changes**: All actions can be undone

**Behavior:**
1. Clarify user intent
2. Propose minimal modular step
3. Explain impact and reversal method
4. Provide exact steps/paths/commands
5. Log preferences and heuristics

---

*The Agentic System: Where simplicity meets sophistication in multi-tier agent management.*
