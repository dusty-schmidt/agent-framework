# Agentic Framework - Development Guide

## 🚀 Quick Start for Development

### 1. **Setup Environment**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenRouter API key
# OPENROUTER_API_KEY=your-api-key-here
```

### 2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 3. **Test Everything**
```bash
python simple_test.py
```

That's it! 🎉

---

## 📁 **Key Files for Development**

### **Environment Setup**
- **`.env`** - Your local environment variables (create from `.env.example`)
- **`simple_env.py`** - Loads .env and sets up paths
- **`simple_test.py`** - Quick test to verify everything works

### **Configuration**
- **`model_config.py`** - Model configuration (uses .env values)
- **`requirements.txt`** - Python dependencies

### **Core Framework**
- **`central_nervous_system/`** - Central coordination system
- **`unified_memory/`** - Memory management system
- **`node/`, `link/`, `mesh/`, `grid/`** - The four tiers

---

## 🧪 **Development Workflow**

### **1. Start Any New Script**
```python
#!/usr/bin/env python3
from simple_env import setup_simple_env
setup_simple_env()

# Now all imports work and .env is loaded
from central_nervous_system.core.central_brain import CentralBrain
from model_config import get_model_config
```

### **2. Test Your Changes**
```bash
python simple_test.py
```

### **3. Add New Dependencies**
```bash
pip install new-package
pip freeze > requirements.txt
```

---

## 🐳 **Docker Deployment**

### **Build and Run**
```bash
# Build the image
docker build -t agentic-framework .

# Run with environment variables
docker run -e OPENROUTER_API_KEY=your-key agentic-framework

# Or use docker-compose
docker-compose up
```

### **Docker Environment Variables**
```bash
# Required
OPENROUTER_API_KEY=your-api-key

# Optional
DEFAULT_MODEL=openai/gpt-oss-20b
DEBUG=false
LOG_LEVEL=INFO
```

---

## 🔧 **Configuration Options**

### **Environment Variables (.env file)**
```bash
# Required
OPENROUTER_API_KEY=your-openrouter-api-key

# Optional Model Settings
DEFAULT_MODEL=openai/gpt-oss-20b
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=1000
API_TIMEOUT=30

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
```

### **Model Configuration**
The framework automatically uses your .env settings:
- **Default model**: `openai/gpt-oss-20b` (or from `DEFAULT_MODEL`)
- **Tier-specific settings**: Each tier gets optimized temperature/tokens
- **API settings**: Timeout, temperature, etc. from .env

---

## 🧪 **Testing**

### **Quick Test (Development)**
```bash
python simple_test.py
```

### **Full Test Suite**
```bash
# Mock tests (no API key needed)
python test_api_mock.py

# Real API tests (needs API key)
python test_api_calls.py

# Environment tests
python test_environment.py
```

---

## 📦 **Project Structure**

```
agentic-framework/
├── .env                    # Your environment variables
├── simple_env.py          # Simple environment setup
├── simple_test.py         # Quick development test
├── model_config.py        # Model configuration
├── requirements.txt       # Dependencies
├── Dockerfile            # Docker image
├── docker-compose.yml    # Docker orchestration
│
├── central_nervous_system/  # Central coordination
│   ├── core/
│   │   ├── central_brain.py
│   │   ├── system_prompt_manager.py
│   │   └── ...
│   └── config/
│
├── unified_memory/         # Memory system
│   ├── memory_interface.py
│   ├── memory_hub.py
│   └── storage/
│
├── node/                  # Tier 1: Simple agents
├── link/                  # Tier 2: Multi-persona
├── mesh/                  # Tier 3: Coordination
└── grid/                  # Tier 4: Self-improving
```

---

## 🔑 **API Key Setup**

### **Get OpenRouter API Key**
1. Go to https://openrouter.ai/keys
2. Create an account and generate an API key
3. Add it to your `.env` file:
   ```bash
   OPENROUTER_API_KEY=your-api-key-here
   ```

### **Test API Key**
```bash
python simple_test.py
```

---

## 🚨 **Troubleshooting**

### **Import Errors**
- Make sure you call `setup_simple_env()` at the top of your script
- Check that you're in the project root directory

### **API Errors**
- Verify your API key in `.env`
- Check your internet connection
- Run `python simple_test.py` to diagnose

### **Docker Issues**
- Make sure your `.env` file exists
- Check Docker logs: `docker-compose logs`
- Verify environment variables are set

---

## 🎯 **Next Steps**

1. **Set up your .env file** with your OpenRouter API key
2. **Run `python simple_test.py`** to verify everything works
3. **Start developing** - all imports and configuration are handled automatically
4. **Deploy with Docker** when ready for production

The framework is designed to be simple for development and robust for deployment! 🚀
