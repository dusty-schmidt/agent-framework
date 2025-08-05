# Directory Structure and Organization

This document describes the current directory structure and organization of the Agentic System after the major cleanup and reorganization.

## 📁 Root Directory Structure

```
agentic system/
├── 🎨 frontend/           # User interface components
│   └── tui/              # Terminal User Interface
├── 📚 docs/              # Comprehensive documentation
├── 📊 logs/              # Centralized system logs
├── 🔧 node/              # Node Tier (single agent)
├── 🔗 link/              # Link Tier (multi-persona)
├── 🕸️  mesh/              # Mesh Tier (coordination)
├── 🌐 grid/              # Grid Tier (self-improving)
├── 🛠️  misc/              # Utilities and tools
├── 📄 README.md          # Main project documentation
├── 🚀 start_tui.py       # Main TUI launcher
├── ⚙️  models.toml        # Model configurations
└── 🐍 run_node.py        # Node tier runner
```

## 🎨 Frontend Directory

```
frontend/
└── tui/                  # Terminal User Interface
    ├── unified_tui.py           # Main TUI application
    ├── logging_config.py        # Centralized logging system
    ├── run_node_tui.py          # Node tier TUI runner
    ├── run_unified_tui.py       # Alternative TUI launcher
    ├── unified_tui.css          # TUI styling
    └── requirements_tui.txt     # TUI dependencies
```

### Purpose
- **Separation of Concerns**: All UI code isolated from business logic
- **Modularity**: Easy to add new interfaces (CLI, Web, etc.)
- **Maintainability**: Clear organization of interface-specific code

## 📚 Documentation Directory

```
docs/
├── README.md                    # Documentation index
├── getting_started.md           # Quick start guide
├── architecture.md              # System architecture
├── system_overview.md           # High-level overview
├── tui_guide.md                # TUI user guide
├── tiers/                      # Tier-specific documentation
│   ├── node_tier.md
│   ├── link_tier.md
│   ├── mesh_tier.md
│   └── grid_tier.md
├── development/                # Development guides
│   ├── development_guide.md
│   ├── api_reference.md
│   └── contributing.md
└── operations/                 # Operational guides
    ├── deployment.md
    ├── monitoring.md
    ├── troubleshooting.md
    └── directory_structure.md
```

### Purpose
- **Comprehensive Coverage**: All aspects of the system documented
- **Progressive Disclosure**: From basic to advanced topics
- **Organized by Audience**: Users, developers, operators

## 📊 Logs Directory

```
logs/
├── tui.log                     # TUI manager activities
├── node_tier.log               # Node tier operations
├── link_tier.log               # Link tier operations
├── mesh_tier.log               # Mesh tier operations
├── grid_tier.log               # Grid tier operations
├── system.log                  # System-wide events
└── session_YYYYMMDD_HHMMSS.log # Session-specific logs
```

### Features
- **Centralized Logging**: All system activities in one location
- **Component Separation**: Individual logs for each tier
- **Session Tracking**: Unique log for each TUI session
- **Log Rotation**: Automatic cleanup and archiving

## 🏢 Tier Directories

Each tier maintains its own directory structure:

### Node Tier (`node/`)
```
node/
├── README.md
├── gob-001-nano/
├── gob-002-nano/
└── node-agent/
    ├── demo_tui.py
    ├── agents/
    ├── config/
    ├── interfaces/
    ├── memory/
    └── tools/
```

### Link Tier (`link/`)
```
link/
├── README.md
└── gob001-mini/
    ├── start.py
    ├── backend/
    ├── frontend/
    ├── docs/
    └── logs/
```

### Mesh Tier (`mesh/`)
```
mesh/
├── README.md
└── gob01/
    ├── backend/
    │   └── src/api/server.py
    ├── frontend/
    ├── docs/
    └── scripts/
```

### Grid Tier (`grid/`)
```
grid/
├── README.md
└── gob01-unified/
    ├── start.py
    ├── backend/
    ├── frontend/
    ├── plugins/
    ├── tools/
    └── configs/
```

## 🛠️ Miscellaneous Directory

```
misc/
├── api calls/
├── claude bot/
├── pinger/
└── zbot/
```

### Purpose
- **Utilities**: Helper scripts and tools
- **Experiments**: Proof-of-concept code
- **Legacy**: Older components being phased out

## 🔄 Migration Summary

### What Was Moved

#### To `frontend/tui/`:
- `unified_tui.py` → `frontend/tui/unified_tui.py`
- `logging_config.py` → `frontend/tui/logging_config.py`
- `run_node_tui.py` → `frontend/tui/run_node_tui.py`
- `run_unified_tui.py` → `frontend/tui/run_unified_tui.py`
- `unified_tui.css` → `frontend/tui/unified_tui.css`
- `requirements_tui.txt` → `frontend/tui/requirements_tui.txt`

#### To `docs/`:
- `README.md` → `docs/system_overview.md`
- `TUI_README.md` → `docs/tui_guide.md`
- Created comprehensive documentation structure

### What Was Removed
- `simple_unified_tui.py` (redundant)
- `simple_tui.css` (redundant)
- `test_tui.py` (temporary)
- `working_tui.py` (replaced unified_tui.py)
- Duplicate `__pycache__` directories
- Duplicate logs directories

### What Was Updated
- **Path References**: All imports and file paths updated for new structure
- **Logging Paths**: Centralized to root `logs/` directory
- **Launch Scripts**: Updated to work with new directory structure
- **Documentation**: Comprehensive rewrite and organization

## 🎯 Benefits of New Structure

### 1. **Clear Separation of Concerns**
- UI code isolated in `frontend/`
- Documentation centralized in `docs/`
- Logs centralized in `logs/`

### 2. **Improved Maintainability**
- Easier to find and modify components
- Clear dependency relationships
- Reduced code duplication

### 3. **Better Scalability**
- Easy to add new interfaces
- Modular documentation structure
- Extensible tier architecture

### 4. **Enhanced User Experience**
- Single entry point (`start_tui.py`)
- Comprehensive documentation
- Consistent logging

### 5. **Development Friendly**
- Clear project structure
- Organized documentation
- Separated concerns

## 🚀 Usage After Reorganization

### Launch TUI
```bash
# From agentic system root
python start_tui.py
```

### Access Documentation
```bash
# View main documentation
cat docs/README.md

# Quick start
cat docs/getting_started.md

# Architecture overview
cat docs/architecture.md
```

### Monitor Logs
```bash
# Follow TUI logs
tail -f logs/tui.log

# Monitor all activity
tail -f logs/*.log
```

### Development
```bash
# TUI development
cd frontend/tui/

# Documentation updates
cd docs/
```

## 📋 Maintenance Tasks

### Regular Cleanup
- Monitor log file sizes
- Clean up old session logs
- Remove unused __pycache__ directories

### Documentation Updates
- Keep tier documentation current
- Update API references
- Maintain troubleshooting guides

### Structure Evolution
- Add new interface directories under `frontend/`
- Expand documentation categories as needed
- Maintain backward compatibility

---

*This structure supports the system's growth while maintaining clarity and organization.*
