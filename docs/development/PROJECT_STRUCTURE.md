# Agentic Framework - Project Structure

## 📁 **Clean Project Organization**

```
agentic-framework/
├── 📋 Core Configuration
│   ├── .env.example              # Environment template
│   ├── simple_env.py            # Environment setup
│   ├── model_config.py          # Model configuration
│   ├── requirements.txt         # Dependencies
│   └── simple_test.py           # Quick development test
│
├── 🐳 Docker Deployment
│   ├── Dockerfile               # Container definition
│   ├── docker-compose.yml       # Multi-container setup
│   └── .dockerignore           # Docker ignore rules
│
├── 🧪 Testing
│   ├── tests/                   # All test files
│   │   ├── test_api_mock.py     # Mock API tests
│   │   ├── test_api_calls.py    # Real API tests
│   │   ├── test_environment.py  # Environment tests
│   │   └── test_storage_backends.py
│   └── run_tests.py            # Test runner
│
├── 🛠️ Development Tools
│   ├── dev/                     # Development utilities
│   │   ├── setup_environment.py # Legacy environment setup
│   │   ├── check_deps.py        # Dependency checker
│   │   └── demo_minimal_tui.py  # TUI demo
│   └── start_tui.py            # TUI launcher
│
├── 🧠 Core Framework
│   ├── central_nervous_system/  # Central coordination
│   │   ├── core/               # Core components
│   │   ├── config/             # Configuration files
│   │   └── examples/           # Usage examples
│   │
│   ├── unified_memory/         # Memory management
│   │   ├── memory_interface.py
│   │   ├── memory_hub.py
│   │   └── storage/            # Storage backends
│   │
│   └── central_nervous_system_data/  # Data storage
│       ├── config/
│       ├── knowledge/
│       ├── memory/
│       └── tools/
│
├── 🏗️ Agent Tiers
│   ├── node/                   # Tier 1: Simple agents
│   ├── link/                   # Tier 2: Multi-persona
│   ├── mesh/                   # Tier 3: Coordination
│   └── grid/                   # Tier 4: Self-improving
│
├── 🎨 User Interfaces
│   ├── frontend/               # Web interfaces
│   │   ├── chatbot_ui.html
│   │   └── tui/               # Terminal UI components
│   └── run_node.py            # Node runner
│
├── 📊 Data & Logs
│   ├── data/                   # Application data
│   ├── logs/                   # Log files
│   └── misc/                   # Miscellaneous tools
│
└── 📚 Documentation
    ├── README.md               # Main documentation
    ├── DEVELOPMENT_GUIDE.md    # Development guide
    ├── TO-DO.md               # Task list
    └── docs/                   # Detailed documentation
        ├── architecture.md
        ├── getting_started.md
        └── tiers/
```

## 🎯 **Key Files by Purpose**

### **🚀 Getting Started**
- `simple_test.py` - Quick test to verify setup
- `.env.example` - Environment template
- `DEVELOPMENT_GUIDE.md` - Complete setup guide

### **🧪 Testing**
- `run_tests.py` - Run all tests
- `tests/test_api_mock.py` - Test without API key
- `tests/test_api_calls.py` - Test with real API

### **⚙️ Configuration**
- `simple_env.py` - Environment setup
- `model_config.py` - Model configuration
- `central_nervous_system/config/` - System configuration

### **🏗️ Core Components**
- `central_nervous_system/core/central_brain.py` - Main orchestrator
- `unified_memory/memory_hub.py` - Memory coordination
- `node/`, `link/`, `mesh/`, `grid/` - Agent tiers

### **🐳 Deployment**
- `Dockerfile` - Container image
- `docker-compose.yml` - Multi-container setup
- `requirements.txt` - Dependencies

## 🧹 **Cleanup Completed**

### **✅ Organized**
- All test files moved to `tests/`
- Development utilities moved to `dev/`
- Clean root directory structure
- Proper import paths updated

### **✅ Removed**
- Obsolete test files
- Duplicate utilities
- Cluttered temporary files
- `__pycache__` directories

### **✅ Improved**
- Clear separation of concerns
- Easy navigation
- Consistent organization
- Better maintainability

## 🎯 **Usage Patterns**

### **Development**
```bash
# Quick test
python simple_test.py

# Full test suite
python run_tests.py

# Start TUI
python start_tui.py
```

### **Testing**
```bash
# Mock tests (no API key)
python tests/test_api_mock.py

# Real API tests
python tests/test_api_calls.py
```

### **Deployment**
```bash
# Docker build
docker build -t agentic-framework .

# Docker run
docker-compose up
```

**The project is now clean, organized, and maintainable!** 🎉
