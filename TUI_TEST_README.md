# 🎯 Minimal TUI - Easy Testing Guide

## Quick Test (Recommended)

**Super simple - just run this:**

```bash
# Option 1: Simple Python script
python test_tui.py

# Option 2: Bash script with more info
./run_test.sh
```

## What You'll See

**Left Side - Tier Panels:**
```
┌─────────────────────────┐
│ NODE    LAUNCH  KILL  ● │  ← Click LAUNCH to start
├─────────────────────────┤
│ LINK    LAUNCH  KILL  ● │  ← Each tier is independent  
├─────────────────────────┤
│ MESH    LAUNCH  KILL  ● │  ← Status: Green=running, Red=stopped
├─────────────────────────┤
│ GRID    LAUNCH  KILL  ● │  ← Click KILL to stop
└─────────────────────────┘
```

**Right Side - Logs Panel:**
```
┌─────────────────────┐
│ LOGS - TEST MODE    │
├─────────────────────┤
│ 🎯 TEST MODE ACTIVE │
│ NODE: Heartbeat 1   │  ← Color-coded output
│ LINK: Processing 1  │  ← Real-time updates
│ MESH: Network 1     │  ← Each tier different color
│ GRID: Computing 1   │  ← Scrollable history
└─────────────────────┘
```

## Demo Processes

When you click **LAUNCH**, each tier runs a simple demo:

- **NODE**: Heartbeat every 2 seconds (cyan)
- **LINK**: Processing every 1.5 seconds (green)  
- **MESH**: Network sync every 3 seconds (yellow)
- **GRID**: Computing every 2.5 seconds (magenta)

## Controls

- **Mouse**: Click LAUNCH/KILL buttons
- **Keyboard**: Tab to navigate, Enter to click
- **Exit**: Ctrl+C (automatically kills all processes)

## What Gets Tested

✅ **Process Management**: Real subprocess launching/killing  
✅ **Status Indicators**: Live green/red status dots  
✅ **Color-coded Logs**: Each tier has different colors  
✅ **Real-time Output**: Live streaming from processes  
✅ **Clean UI**: Matches your mockup design exactly  

## Files Created

- `test_tui.py` - Simple launcher
- `run_test.sh` - Bash launcher with info
- `frontend/tui/test_minimal_tui.py` - Test TUI with demo processes
- `frontend/tui/minimal_tui.py` - Real TUI for actual tiers
- `frontend/tui/minimal_tui.css` - Clean styling

## Next Steps

After testing the demo:

1. **For Real Tiers**: Use `python start_tui.py` (launches actual tier processes)
2. **Customize**: Edit tier commands in `minimal_tui.py`
3. **Styling**: Modify `minimal_tui.css` for different colors/layout

---

**🚀 Ready to test? Just run:**
```bash
python test_tui.py
```

Click LAUNCH buttons and watch the magic! 🎨
