# Terminal Chat Interface

## 🖥️ **Minimalistic Terminal-Style Chatbot**

A clean, monitor-style chat interface for the Agentic Framework with terminal aesthetics and functional design.

## 🎨 **Design Philosophy**

- **Minimalistic** - Clean terminal aesthetics
- **Functional** - Focus on usability over decoration  
- **Monitor-Style** - Similar to system monitoring interfaces
- **Color-Coded** - Different colors for different message types
- **Real-Time** - Live status updates and timestamps

## 🚀 **Features**

### **Terminal Styling**
- ASCII art header with framework branding
- Color-coded messages (user, agent, system, error)
- Real-time status bar with tier, message count, uptime
- Clean monospace font for authentic terminal feel

### **Multi-Tier Support**
- Switch between all 4 agent tiers (node, link, mesh, grid)
- Tier-specific system prompts and personalities
- Visual tier indicator in status bar and prompts

### **Interactive Commands**
- `/tier <name>` - Switch between agent tiers
- `/clear` - Clear conversation history
- `/status` - Show current session status
- `/help` - Display available commands
- `/quit` - Exit the interface

### **Smart Features**
- Conversation history with context
- Processing indicators while waiting for responses
- Session statistics (uptime, message count)
- Keyboard interrupt handling

## 📁 **Files Created**

### **1. Python Terminal Interface**
```
frontend/terminal_chat.py
```
- Full-featured terminal chat interface
- Real API integration with OpenRouter
- Color-coded terminal output
- Complete command system

### **2. Launch Script**
```
frontend/run_terminal_chat.sh
```
- Ensures zsh environment is loaded
- One-command launch for easy use

### **3. Web Terminal Interface**
```
frontend/terminal_chat.html
```
- Browser-based terminal emulation
- Same visual style as Python version
- Mock responses for demonstration
- Fully interactive web interface

## 🎯 **Usage**

### **Python Terminal Chat**
```bash
# Method 1: Direct launch (loads zsh environment)
./frontend/run_terminal_chat.sh

# Method 2: Manual launch
source ~/.zshrc && python frontend/terminal_chat.py

# Method 3: From any shell
source ~/.zshrc
python frontend/terminal_chat.py
```

### **Web Terminal Chat**
```bash
# Open in browser
open frontend/terminal_chat.html
# or
firefox frontend/terminal_chat.html
```

## 🎨 **Visual Design**

### **Color Scheme**
- **Header**: Cyan (`#00ffff`) - Framework branding
- **User Messages**: Green (`#00ff00`) - Input text
- **Agent Messages**: Blue (`#00aaff`) - AI responses  
- **System Messages**: Gray (`#666666`) - Status updates
- **Error Messages**: Red (`#ff4444`) - Error notifications
- **Tier Indicator**: Yellow (`#ffff00`) - Current tier
- **Background**: Dark (`#0a0a0a`) - Terminal black

### **Layout Elements**
```
╭─────────────────────────────────────────────────────────────╮
│                    AGENTIC FRAMEWORK                       │
│                  Terminal Chat Interface                   │
╰─────────────────────────────────────────────────────────────╯

┌─ STATUS ─────────────────────────────────────────────────────┐
│ Tier: NODE   │ Messages:   5 │ Uptime:  45s │ 14:23:17 │
└──────────────────────────────────────────────────────────────┘

[SYSTEM] Terminal chat ready. Type /help for commands.
[SYSTEM] Current tier: node

[NODE] You: Hello! What's 7 + 5?
[NODE] Agent: 7 + 5 equals 12.

[NODE] You: /tier link
[SYSTEM] Switched to link tier
[LINK] You: What can you help me with?
[LINK] Agent: I can help with many tasks including...
```

## ⚙️ **Technical Details**

### **Python Implementation**
- **Async/Await** - Non-blocking API calls
- **aiohttp** - HTTP client for OpenRouter API
- **ANSI Colors** - Terminal color codes
- **Error Handling** - Graceful error management
- **Memory Management** - Conversation history limits

### **Web Implementation**
- **Pure JavaScript** - No external dependencies
- **CSS Grid/Flexbox** - Responsive layout
- **Local Storage** - Session persistence (future)
- **WebSocket Ready** - Easy to add real-time features

### **API Integration**
- **OpenRouter API** - Real AI model access
- **Tier-Specific Prompts** - Different personalities per tier
- **Context Management** - Conversation history included
- **Rate Limiting** - Respectful API usage

## 🔧 **Configuration**

### **Tier Personalities**
```python
system_prompts = {
    "node": "You are a Node tier agent. Be direct and concise.",
    "link": "You are a Link tier agent. Be versatile and helpful.", 
    "mesh": "You are a Mesh tier agent. Focus on coordination.",
    "grid": "You are a Grid tier agent. Provide analytical responses."
}
```

### **Color Customization**
```python
colors = {
    'header': '\033[96m',    # Cyan
    'user': '\033[92m',      # Green  
    'agent': '\033[94m',     # Blue
    'system': '\033[90m',    # Gray
    'error': '\033[91m',     # Red
    'tier': '\033[93m',      # Yellow
}
```

## 📊 **Session Features**

### **Real-Time Status**
- Current active tier
- Total messages sent
- Session uptime
- Current timestamp

### **Conversation Management**
- History limit (20 messages)
- Context inclusion (last 4 messages)
- Clear command for fresh start
- Persistent across tier switches

## 🎉 **Result**

**A beautiful, functional terminal chat interface that:**
- ✅ Looks professional and clean
- ✅ Provides real AI conversations
- ✅ Supports all 4 agent tiers
- ✅ Has intuitive commands
- ✅ Shows real-time status
- ✅ Works in terminal and browser
- ✅ Integrates seamlessly with the framework

**Perfect for development, testing, and demonstration of the Agentic Framework!** 🚀
