# Conda + ZSH Setup Guide

## 🐍 **Conda Environment Setup**

### **1. Create Conda Environment**
```bash
# Create environment from file
conda env create -f environment.yml

# Or create manually
conda create -n agentic-framework python=3.11
conda activate agentic-framework
pip install aiohttp textual rich toml pydantic numpy faiss-cpu
```

### **2. Activate Environment**
```bash
conda activate agentic-framework
```

## 🔑 **API Key Setup in ZSH**

### **Add to ~/.zshrc**
```bash
# Add these lines to your ~/.zshrc file
export OPENROUTER_API_KEY="your_api_key_here"
export MODEL_NAME="openai/gpt-oss-20b"  # Optional - defaults to this
export LOG_LEVEL="INFO"                  # Optional - defaults to INFO
```

### **Reload ZSH Config**
```bash
source ~/.zshrc
```

### **Verify Setup**
```bash
echo $OPENROUTER_API_KEY  # Should show your API key
```

## 🚀 **Development Workflow**

### **Daily Development**
```bash
# 1. Activate conda environment
conda activate agentic-framework

# 2. Run tests to verify everything works
python tests/complete_test.py

# 3. Start developing or chatting with agents
python simple_chat.py
```

### **Project Structure**
```
agentic-framework/
├── environment.yml       # Conda environment definition
├── config.toml          # Simple configuration
├── simple_env.py        # Minimal environment setup
└── ...
```

## 🐳 **Docker Deployment**

### **Build and Run**
```bash
# Set environment variables for Docker
export OPENROUTER_API_KEY="your_api_key_here"

# Build and run with docker-compose
cd docker/
docker-compose up --build
```

### **Environment Variables for Docker**
Docker will automatically pick up these environment variables:
- `OPENROUTER_API_KEY` - Your API key
- `MODEL_NAME` - Model to use (optional)
- `LOG_LEVEL` - Logging level (optional)

## ✅ **Benefits of This Setup**

### **1. Clean Environment Management**
- No complex Python environment logic
- Standard conda workflow
- Easy to reproduce

### **2. Secure API Key Management**
- API keys in zsh config (not in code)
- Same keys work for development and Docker
- No .env files to manage

### **3. Simple Configuration**
- TOML config file for settings
- Environment variables for secrets
- No hardcoded values

### **4. Docker Ready**
- Environment variables automatically passed to Docker
- Clean production deployment
- Same setup for dev and prod

## 🔧 **Troubleshooting**

### **API Key Not Found**
```bash
# Check if API key is set
echo $OPENROUTER_API_KEY

# If empty, add to ~/.zshrc and reload
source ~/.zshrc
```

### **Conda Environment Issues**
```bash
# Recreate environment
conda env remove -n agentic-framework
conda env create -f environment.yml
```

### **Import Errors**
```bash
# Make sure you're in the right environment
conda activate agentic-framework

# Run from project root directory
cd /path/to/agentic-framework
python tests/complete_test.py
```

## 📝 **Quick Commands**

```bash
# Setup (one time)
conda env create -f environment.yml
echo 'export OPENROUTER_API_KEY="your_key"' >> ~/.zshrc
source ~/.zshrc

# Daily workflow
conda activate agentic-framework
python tests/complete_test.py
python simple_chat.py

# Docker deployment
export OPENROUTER_API_KEY="your_key"
cd docker && docker-compose up --build
```

**Clean, simple, and production-ready!** 🚀
