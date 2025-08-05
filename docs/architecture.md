# Agentic System Architecture

This document describes the high-level architecture and design principles of the Agentic System.

## Design Principles

### 1. Modular Architecture
- **Separation of Concerns**: Each tier has a specific purpose and scope
- **Loose Coupling**: Tiers can operate independently
- **Interface Abstraction**: Common interfaces across tiers

### 2. 80/20 Principle
- Focus on the 20% of features that provide 80% of the value
- Prioritize essential functionality over comprehensive features
- Iterative improvement based on actual usage

### 3. Interface-Agnostic Design
- Core logic separated from presentation layer
- Multiple interface options (TUI, CLI, API)
- Consistent behavior across interfaces

### 4. Agent-Guided Operations
- Intelligent automation where appropriate
- Human oversight for critical decisions
- Progressive automation as confidence builds

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Agentic System                           │
├─────────────────────────────────────────────────────────────┤
│  Frontend Layer                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │     TUI     │  │     CLI     │  │   Web UI    │         │
│  │  (Textual)  │  │  (Future)   │  │  (Future)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  Management Layer                                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │           Unified TUI Manager                           │ │
│  │  • Tier Lifecycle Management                           │ │
│  │  • Status Monitoring                                   │ │
│  │  • Centralized Logging                                 │ │
│  └─────────────────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Tier Layer                                                 │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐   │
│  │   Node    │ │   Link    │ │   Mesh    │ │   Grid    │   │
│  │   Tier    │ │   Tier    │ │   Tier    │ │   Tier    │   │
│  │           │ │           │ │           │ │           │   │
│  │ Single    │ │ Multi-    │ │ Multi-    │ │ Self-     │   │
│  │ Agent     │ │ Persona   │ │ Agent     │ │ Improving │   │
│  │           │ │           │ │ Coord.    │ │ Framework │   │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘   │
├─────────────────────────────────────────────────────────────┤
│  Infrastructure Layer                                       │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │  Logging • Configuration • Process Management          │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
agentic system/
├── frontend/              # User interface components
│   └── tui/              # Terminal User Interface
│       ├── unified_tui.py        # Main TUI application
│       ├── logging_config.py     # Centralized logging
│       ├── run_node_tui.py       # Node tier runner
│       └── requirements_tui.txt  # Dependencies
├── docs/                  # Documentation
│   ├── tiers/            # Tier-specific docs
│   ├── development/      # Development guides
│   └── operations/       # Operational guides
├── logs/                  # System logs
├── node/                  # Node Tier
│   └── node-agent/       # Single agent implementation
├── link/                  # Link Tier
│   └── gob001-mini/      # Multi-persona system
├── mesh/                  # Mesh Tier
│   └── gob01/            # Multi-agent coordination
├── grid/                  # Grid Tier
│   └── gob01-unified/    # Self-improving framework
└── misc/                  # Utilities and tools
```

## Component Architecture

### Frontend Layer

#### TUI Manager (`unified_tui.py`)
- **Purpose**: Primary user interface for system management
- **Technology**: Textual framework
- **Responsibilities**:
  - Tier lifecycle management (start/stop/restart)
  - Real-time status monitoring
  - Log aggregation and display
  - User interaction handling

#### Tier Manager (`SimpleTierManager`)
- **Purpose**: Individual tier process management
- **Responsibilities**:
  - Process spawning and monitoring
  - Status tracking
  - Log capture
  - Graceful shutdown

### Management Layer

#### Centralized Logging (`logging_config.py`)
- **Purpose**: Unified logging across all components
- **Features**:
  - Structured logging with timestamps
  - Log rotation and retention
  - Component-specific log files
  - Session tracking

#### Configuration Management
- **Model Configuration**: `models.toml`
- **Agent Naming**: `agent_naming.toml`
- **Dependencies**: `requirements_tui.txt`

### Tier Layer

Each tier represents a different level of agent system complexity:

#### Node Tier
- **Complexity**: Basic
- **Agents**: Single agent
- **Use Case**: Simple interactions, testing
- **Technology**: Python, basic tools

#### Link Tier
- **Complexity**: Intermediate
- **Agents**: Multi-persona system
- **Use Case**: Production applications
- **Technology**: FastAPI, advanced tools
- **Port**: 8001

#### Mesh Tier
- **Complexity**: Advanced
- **Agents**: Multi-agent coordination
- **Use Case**: Complex workflows
- **Technology**: WebSocket events, coordination
- **Port**: 8080

#### Grid Tier
- **Complexity**: Expert
- **Agents**: Self-improving framework
- **Use Case**: Advanced AI applications
- **Technology**: Plugin system, self-modification
- **Port**: 8001

## Data Flow

### Startup Flow
1. User launches `start_tui.py`
2. TUI Manager initializes
3. Centralized logging starts
4. Tier configurations loaded
5. TUI interface rendered
6. Status monitoring begins

### Tier Management Flow
1. User selects tier action (start/stop/restart)
2. TUI Manager validates request
3. Tier Manager executes action
4. Process status updated
5. Logs generated
6. UI refreshed
7. User notified

### Monitoring Flow
1. Tier processes generate output
2. Tier Managers capture logs
3. Centralized logging aggregates
4. TUI displays real-time status
5. Log files written to disk
6. Session tracking updated

## Security Considerations

### Process Isolation
- Each tier runs in separate processes
- Limited inter-tier communication
- Graceful failure handling

### Log Security
- Sensitive data filtering
- Log rotation and cleanup
- Access control considerations

### Network Security
- Port binding controls
- Local-only by default
- Configurable network access

## Scalability Considerations

### Horizontal Scaling
- Tiers can run on different machines
- Load balancing for web tiers
- Distributed logging options

### Vertical Scaling
- Resource monitoring per tier
- Dynamic resource allocation
- Performance optimization

## Extension Points

### New Tiers
- Follow existing tier patterns
- Implement standard interfaces
- Add to TUI configuration

### New Interfaces
- Implement common management interface
- Reuse tier management logic
- Maintain consistency

### New Features
- Plugin architecture in Grid tier
- Custom tool integration
- Advanced monitoring capabilities

## Technology Stack

### Core Technologies
- **Python 3.8+**: Primary language
- **Textual**: TUI framework
- **Rich**: Text formatting and display
- **FastAPI**: Web framework (tiers)
- **WebSockets**: Real-time communication

### Development Tools
- **Git**: Version control
- **pytest**: Testing framework
- **Black**: Code formatting
- **mypy**: Type checking

### Deployment
- **systemd**: Service management
- **Docker**: Containerization (future)
- **nginx**: Reverse proxy (web tiers)

---

*This architecture supports the system's core principles while providing flexibility for future growth and adaptation.*
