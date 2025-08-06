# Primary Interface - Web-Based Chatbot

## 🚀 **New Primary Startup Method**

The Agentic Framework now launches with a web-based interface as the primary method, with optional test mode for development and debugging.

## 📋 **Usage**

### **Primary Launch Command**
```bash
python main.py
```
This launches the web-based chatbot interface at `http://localhost:8080`

### **Available Options**
```bash
python main.py                    # Web interface (primary)
python main.py --test            # Web interface with test panels  
python main.py --terminal        # Terminal interface
python main.py --validate        # Validate configuration only
python main.py --port 9000       # Custom port
```

## 🎨 **Interface Modes**

### **1. Standard Web Interface**
- **Command:** `python main.py`
- **URL:** `http://localhost:8080/chatbots/chatbot_ui.html`
- **Features:**
  - Clean hacker-aesthetic design
  - Multi-conversation support
  - File upload capability
  - Tier switching (future)
  - Dark theme optimized

### **2. Test Interface with Live Panels**
- **Command:** `python main.py --test`
- **URL:** `http://localhost:8080/chatbots/chatbot_test.html`
- **Features:**
  - All standard features PLUS:
  - Live system logs panel
  - Real-time status monitoring
  - Memory context viewer
  - Agent tier switching
  - System commands (/clear, /status, /test)

### **3. Terminal Interface**
- **Command:** `python main.py --terminal`
- **Features:**
  - Full terminal-based chat
  - Real API integration
  - Tier switching commands
  - Hacker aesthetic

### **4. Validation Mode**
- **Command:** `python main.py --validate`
- **Features:**
  - Configuration validation
  - Environment checking
  - Dependency verification
  - Exit after validation

## 🔧 **Test Interface Features**

### **Live Panels**
The test interface includes three monitoring panels:

#### **1. LOGS Panel**
- Real-time system logs
- Color-coded log levels (INFO, WARN, ERROR)
- Automatic scrolling
- Timestamp tracking

#### **2. STATUS Panel**
- Active tier indicator
- Message count
- System uptime
- API status

#### **3. MEMORY Panel**
- Conversation context
- Recent message history
- Memory usage tracking

### **Agent Tier Switching**
- **NODE** - Direct, concise responses
- **LINK** - Versatile, multi-persona interactions
- **MESH** - Coordination and organization
- **GRID** - Analytical, self-improving responses

### **System Commands**
- `/CLEAR` - Clear chat history
- `/STATUS` - Show system status
- `/TEST` - Run system test

## 🎯 **Design Philosophy**

### **Hacker Aesthetic**
- **Colors:** Green on black terminal styling
- **Font:** Courier New monospace
- **UI Elements:** Minimal, functional design
- **Status Indicators:** Bracket notation [PASS]/[FAIL]
- **Prefixes:** `>>` for system messages

### **Professional Layout**
- Clean grid-based layout
- Responsive design
- Intuitive navigation
- Real-time updates

## 🔄 **Migration from Old Methods**

### **Before (Multiple Scripts)**
```bash
# Old scattered approach
python scripts/simple_chat.py      # Basic chat
./frontend/run_terminal_chat.sh    # Terminal chat
python tests/complete_test.py       # Testing
python scripts/validate_config.py  # Validation
```

### **After (Unified Entry Point)**
```bash
# New unified approach
python main.py                     # Primary interface
python main.py --test             # Development interface
python main.py --terminal         # Terminal interface  
python main.py --validate         # Validation
```

## 🚀 **Benefits**

### **1. Unified Entry Point**
- Single command to remember
- Consistent interface
- Clear options and help

### **2. Professional Presentation**
- Web-based interface looks professional
- Suitable for demonstrations
- Easy to share and use

### **3. Development-Friendly**
- Test mode with live monitoring
- Real-time logs and status
- Easy debugging and development

### **4. Flexible Options**
- Choose interface type based on need
- Terminal for development
- Web for presentation
- Test mode for debugging

## 📊 **Interface Comparison**

| Feature | Standard Web | Test Web | Terminal | Validation |
|---------|-------------|----------|----------|------------|
| **Chat Interface** | ✅ | ✅ | ✅ | ❌ |
| **Tier Switching** | 🔄 | ✅ | ✅ | ❌ |
| **Live Logs** | ❌ | ✅ | ❌ | ❌ |
| **Status Monitoring** | ❌ | ✅ | ✅ | ❌ |
| **Memory Viewer** | ❌ | ✅ | ❌ | ❌ |
| **File Upload** | ✅ | ❌ | ❌ | ❌ |
| **Multi-Chat** | ✅ | ❌ | ❌ | ❌ |
| **Config Check** | ❌ | ❌ | ❌ | ✅ |

## 🎉 **Result**

**The Agentic Framework now has a professional, unified entry point that:**
- ✅ **Looks professional** with hacker aesthetic
- ✅ **Easy to use** with single command
- ✅ **Development-friendly** with test mode
- ✅ **Flexible** with multiple interface options
- ✅ **Well-documented** with clear usage examples

**Perfect for both development and demonstration!** 🚀
