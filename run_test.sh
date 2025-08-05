#!/bin/bash

echo "🎯 Agentic System - Minimal TUI Test"
echo "===================================="
echo ""
echo "This will launch the TEST VERSION of the minimal TUI"
echo "• Demo processes that you can see working immediately"
echo "• Click LAUNCH to start colored demo processes"
echo "• Click KILL to stop them"
echo "• Watch the logs panel for real-time output"
echo ""
echo "Controls:"
echo "• Tab/Shift+Tab: Navigate between buttons"
echo "• Enter/Space: Click buttons"
echo "• Ctrl+C: Exit"
echo ""

# Check if we're in the right directory
if [ ! -f "test_tui.py" ]; then
    echo "❌ Error: Please run this from the agentic system directory"
    echo "   cd to the directory containing test_tui.py"
    exit 1
fi

# Check if textual is installed
python -c "import textual" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: textual not installed"
    echo "   Install with: pip install textual"
    exit 1
fi

echo "🚀 Starting test TUI..."
echo ""

# Run the test TUI
python test_tui.py
