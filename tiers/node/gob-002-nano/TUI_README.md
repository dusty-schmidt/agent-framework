# 🖥️ **Multi-Agent System TUI Interface**

## 📋 **Overview**

The Multi-Agent System now includes a modern Terminal User Interface (TUI) built with [Textual](https://textual.textualize.io/), providing real-time interaction and system monitoring capabilities.

## 🎯 **Features**

### **Multi-Pane Interface**
- 💬 **Conversation Pane**: Interactive chat with the multi-agent system
- 📋 **System Logs Pane**: Real-time backend process monitoring
- ⌨️ **Input Area**: Message input with send/clear controls
- 🎨 **Rich Text**: Colored, formatted output with timestamps

### **Real-Time Capabilities**
- 🔄 Live log streaming from all system components
- ⚡ Asynchronous message processing
- 📊 Agent selection and confidence scoring
- 🎯 Specialized agent routing (Main, Developer, Research)

### **Advanced Commands**
- `adjust behavior <feedback>` - Self-improvement system
- `schedule task <description>` - Task management with JSON storage
- Standard chat and questions
- Agent-specific routing based on keywords

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install textual rich
```

### **2. Run the Full Multi-Agent TUI**
```bash
export GEMINI_API_KEY="your-api-key-here"
python tui_multiagent.py
```

### **3. Run the Simple Demo**
```bash
python demo_tui.py
```

## 🖼️ **Interface Layout**

```
┌─────────────────────────────────────────────────────────────────┐
│                     Multi-Agent AI System                      │
├─────────────────────────────────────────────────────────────────┤
│  💬 Conversation              │  📋 System Logs               │
│                               │                                │
│  [10:30:15] You: Hello        │  [10:30:15] INFO: Processing   │
│  [10:30:16] Main Agent:       │  [10:30:16] INFO: Agent        │
│  Hi! How can I help?          │  selected: Main Agent         │
│                               │  [10:30:16] INFO: Response     │
│                               │  generated successfully       │
│                               │                                │
├─────────────────────────────────────────────────────────────────┤
│  Type your message... [Send] [Clear Chat] [Adjust Behavior]    │
└─────────────────────────────────────────────────────────────────┘
```

## 🎨 **Color Coding**

### **Conversation Messages**
- 🔵 **Blue**: User messages
- 🟢 **Green**: Agent responses  
- 🟡 **Yellow**: System messages
- 🟣 **Magenta**: Processing indicators
- 🔴 **Red**: Error messages

### **System Logs**
- 🟢 **Green**: INFO level logs
- 🟡 **Yellow**: WARNING level logs
- 🔴 **Red**: ERROR level logs
- ⚪ **Dim**: DEBUG level logs

## ⌨️ **Keyboard Shortcuts**

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Ctrl+C` | Quit application |
| `Tab` | Navigate between input and buttons |
| `Escape` | Clear current input |

## 🤖 **Agent System Integration**

### **Agent Selection**
The TUI automatically routes messages to appropriate agents based on keywords:

- **Developer Agent**: `code`, `program`, `develop`, `write`, `debug`
- **Research Agent**: `research`, `find`, `analyze`, `search`, `study`
- **Main Agent**: General queries and fallback

### **Real-Time Monitoring**
Watch the system logs to see:
- Agent selection process
- Memory embedding operations
- Confidence scoring
- Error handling
- Performance metrics

## 🔧 **Configuration**

### **Environment Variables**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### **CSS Customization**
Edit `interfaces/tui_styles.css` to customize the appearance:
- Colors and themes
- Layout proportions
- Border styles
- Font styling

## 📊 **Advanced Features**

### **Memory System Integration**
- View real-time memory embedding operations
- Semantic search logging
- Context retrieval monitoring

### **Self-Improvement**
```
adjust behavior be more technical
adjust behavior provide more examples
adjust behavior be more concise
```

### **Task Scheduling**
```
schedule task review code tomorrow
schedule task update documentation
```
Tasks are saved as JSON files in the `tasks/` directory.

## 🛠️ **Development**

### **File Structure**
```
interfaces/
├── tui_front.py           # Basic TUI implementation
├── tui_styles.css         # Styling and layout
└── README.md              # This file

tui_multiagent.py          # Full integration with multi-agent system
demo_tui.py               # Simple demo version
```

### **Extending the TUI**
To add new features:

1. **Add new widgets in `compose()`**
2. **Handle events in event handlers**
3. **Update CSS for styling**
4. **Add logging for monitoring**

### **Custom Log Capture**
The `LogCapture` class intercepts all system logs and displays them in real-time:

```python
class LogCapture(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        self.tui_app.add_log_message(msg, record.levelname)
```

## 🐛 **Troubleshooting**

### **Common Issues**

**CSS Errors**: 
- Check for unsupported CSS features
- Use basic color names instead of variables
- Validate border syntax

**Agent Not Responding**:
- Check API key environment variable
- Verify network connectivity
- Check system logs for error details

**Memory Issues**:
- Ensure memory directory exists
- Check disk space for embeddings
- Verify FAISS installation

### **Debug Mode**
Add logging level configuration:
```python
logging.getLogger().setLevel(logging.DEBUG)
```

## 🎉 **Demo Scenarios**

Try these example interactions:

### **Development Tasks**
```
write a Python function to sort a list
debug this code snippet
create a REST API endpoint
```

### **Research Tasks**
```
research machine learning trends
find information about quantum computing
analyze market data for tech stocks
```

### **System Commands**
```
adjust behavior be more detailed in explanations
schedule task implement new feature next week
clear
```

## 🔮 **Future Enhancements**

- 📊 Real-time memory visualization
- 🎭 Agent status indicators
- 📈 Performance metrics dashboard
- 🔄 Multi-session support
- 🎨 Theme customization
- 📱 Responsive design for different terminal sizes

---

## 🚀 **Ready to Use!**

The TUI provides a professional, real-time interface for interacting with your multi-agent system while monitoring all backend processes. Perfect for development, testing, and production use!

**Start exploring with:**
```bash
python tui_multiagent.py
```
