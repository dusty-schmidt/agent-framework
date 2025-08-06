# Development Guide

## 🗂️ **Codebase Organization**

### Directory Structure
```
gob-001-mini/
├── backend/                 # Python FastAPI backend
│   ├── agents/             # Agent system (orchestrator, registry, etc.)
│   ├── assistants/         # Specialized assistants (coding, general)
│   ├── config/             # Configuration management
│   │   ├── environments/   # Environment-specific configs
│   │   ├── config.yaml     # Current active config
│   │   └── config.template.yaml
│   ├── services/           # Business logic services
│   └── main.py            # FastAPI application entry point
├── frontend/               # React frontend
│   ├── js/                # JavaScript/JSX files
│   ├── css/               # CSS files
│   └── index.html         # Main HTML file
├── tests/                  # Test suite
├── scripts/                # Development and utility scripts
├── docs/                   # Documentation
└── logs/                   # Application logs
```

### 🧪 **Testing Strategy**

#### Automated Tests
- **Location**: `tests/` directory
- **Health Checks**: `tests/test_health_endpoints.py`
- **Run Tests**: `python tests/test_health_endpoints.py`

#### Manual Testing
- **API Testing**: `scripts/test_api.py`
- **Usage**: `python scripts/test_api.py`

### 🔧 **Development Workflow**

#### 1. Environment Setup
```bash
# Activate conda environment
conda activate agentic-framework

# Start development servers
python start.py
```

#### 2. Configuration Management
- **Development**: Uses `backend/config/environments/development.yaml`
- **Production**: Uses `backend/config/environments/production.yaml`
- **Current**: `backend/config/config.yaml` (active configuration)

#### 3. Model Configuration
- **Development**: All models use `gemini-2.0-flash-lite` for cost efficiency
- **Production**: Mixed models optimized for performance
- **Health Checks**: Available at `/api/health/llm`

### 📊 **Monitoring and Health Checks**

#### Available Endpoints
```bash
# Basic API health
GET /api/health

# Comprehensive LLM health
GET /api/health/llm

# Individual provider health
GET /api/health/llm/google
GET /api/health/llm/groq
GET /api/health/llm/openrouter
```

#### Testing Commands
```bash
# Test all health endpoints
curl http://localhost:8001/api/health/llm

# Test chat functionality
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!", "sessionId": "test"}'
```

### 🔄 **Development Best Practices**

#### Code Organization
1. **Keep test code in `tests/` directory**
2. **Use `scripts/` for development utilities**
3. **Maintain environment-specific configurations**
4. **Update documentation as you develop**

#### Testing Guidelines
1. **Test health endpoints before major changes**
2. **Use development configuration for testing**
3. **Monitor API costs during development**
4. **Keep test sessions organized**

#### Git Workflow
1. **Commit frequently with descriptive messages**
2. **Keep `.gitignore` updated**
3. **Don't commit API keys or sensitive data**
4. **Use feature branches for major changes**

### 🚀 **Deployment Preparation**

#### Pre-deployment Checklist
- [ ] All tests passing
- [ ] Health checks working
- [ ] Production configuration ready
- [ ] API keys configured
- [ ] Documentation updated
- [ ] Logs reviewed

#### Configuration Switch
```bash
# Copy production config when ready
cp backend/config/environments/production.yaml backend/config/config.yaml
```

### 🔍 **Debugging and Troubleshooting**

#### Common Issues
1. **Import Errors**: Check VS Code Python interpreter
2. **API Failures**: Verify API keys in `.env`
3. **Model Errors**: Check model names in configuration
4. **Health Check Failures**: Verify network connectivity

#### Debugging Tools
- **Health Endpoints**: Real-time API status
- **Logs**: Check application logs
- **VS Code**: Configured for conda environment
- **Test Scripts**: Manual API testing

### 📝 **Documentation Updates**

When making changes:
1. Update relevant documentation
2. Add new endpoints to health checks
3. Update configuration examples
4. Keep README.md current

This guide ensures the codebase remains organized and professional throughout development and testing phases.
