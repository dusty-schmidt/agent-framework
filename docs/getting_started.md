# Getting Started with Agentic System

This guide will help you get up and running with the Agentic System quickly.

## Prerequisites

- Python 3.8 or higher
- Terminal with ANSI color support
- At least 4GB RAM recommended

## Installation

1. **Navigate to the system directory**:
   ```bash
   cd "agentic system"
   ```

2. **Install TUI dependencies** (optional - will auto-install):
   ```bash
   pip install -r frontend/tui/requirements_tui.txt
   ```

## First Launch

### Start the TUI Manager

```bash
python start_tui.py
```

You should see:
```
🚀 Starting Agentic System TUI Manager...
=========================================
✅ Dependencies available
🎨 Launching TUI Manager...
   Use Ctrl+C to exit
   Use Tab to navigate between tabs
   Click buttons to control tiers
```

### Navigate the Interface

The TUI has several tabs:
- **Overview**: See all tiers at a glance
- **Node Tier**: Control the basic single-agent tier
- **Link Tier**: Manage multi-persona agents
- **Mesh Tier**: Coordinate multi-agent systems
- **Grid Tier**: Access self-improving framework

### Basic Operations

1. **Start a Tier**:
   - Navigate to a tier tab
   - Click the "Start" button
   - Watch the status change to 🟢 RUNNING

2. **Monitor Status**:
   - Check uptime and port information
   - View real-time status updates
   - Monitor in the Overview tab

3. **Stop a Tier**:
   - Click the "Stop" button
   - Status changes to 🔴 STOPPED

4. **Restart a Tier**:
   - Click "Restart" for a clean restart
   - Or use Stop → Start manually

## Understanding the Tiers

### Node Tier
- **Purpose**: Basic single-agent functionality
- **Best for**: Simple chatbot interactions, testing
- **Resources**: Lightweight, minimal dependencies

### Link Tier  
- **Purpose**: Multi-persona agent system
- **Best for**: Production applications, complex interactions
- **Port**: 8001
- **Resources**: Moderate resource usage

### Mesh Tier
- **Purpose**: Multi-agent coordination
- **Best for**: Complex workflows, agent collaboration
- **Port**: 8080
- **Resources**: Higher resource usage

### Grid Tier
- **Purpose**: Self-improving unified framework
- **Best for**: Advanced AI applications, plugin systems
- **Port**: 8001
- **Resources**: Highest resource usage

## Monitoring and Logs

### Real-time Monitoring
- Status indicators: 🟢 RUNNING / 🔴 STOPPED
- Uptime counters
- Port information
- Resource usage (basic)

### Log Files
All activities are logged to `logs/` directory:

```bash
# View TUI logs
tail -f logs/tui.log

# View specific tier logs
tail -f logs/node_tier.log
tail -f logs/link_tier.log
tail -f logs/mesh_tier.log
tail -f logs/grid_tier.log

# View system logs
tail -f logs/system.log
```

### Session Logs
Each TUI session creates a unique log file:
```bash
ls logs/session_*.log
```

## Common Workflows

### Development Workflow
1. Start with Node Tier for basic testing
2. Move to Link Tier for multi-agent development
3. Use Mesh Tier for coordination testing
4. Deploy to Grid Tier for production

### Production Workflow
1. Start required tiers based on your needs
2. Monitor status in Overview tab
3. Check logs for any issues
4. Use Restart if needed

### Troubleshooting Workflow
1. Check tier status in TUI
2. Review relevant log files
3. Try restarting the problematic tier
4. Check system resources

## Keyboard Shortcuts

- **Tab**: Navigate between tabs
- **Enter**: Activate focused button
- **Ctrl+C**: Exit the TUI
- **Mouse**: Click buttons and tabs (if supported)

## Next Steps

Once you're comfortable with the basics:

1. **Explore Tier Documentation**:
   - [Node Tier Guide](tiers/node_tier.md)
   - [Link Tier Guide](tiers/link_tier.md)
   - [Mesh Tier Guide](tiers/mesh_tier.md)
   - [Grid Tier Guide](tiers/grid_tier.md)

2. **Learn Advanced Features**:
   - [Development Guide](development/development_guide.md)
   - [API Reference](development/api_reference.md)

3. **Set Up Monitoring**:
   - [Monitoring Guide](operations/monitoring.md)
   - [Deployment Guide](operations/deployment.md)

## Troubleshooting

### TUI Won't Start
- Ensure you're in the "agentic system" directory
- Check Python version: `python --version`
- Install dependencies: `pip install textual rich`

### Tier Won't Start
- Check if the tier directory exists
- Review the tier's log file
- Ensure no port conflicts

### Display Issues
- Try a different terminal
- Ensure terminal supports ANSI colors
- Resize terminal window

For more detailed troubleshooting, see [Troubleshooting Guide](operations/troubleshooting.md).

---

*Remember: The system follows the 80/20 principle - start with the essential features and expand as needed.*
