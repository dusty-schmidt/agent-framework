#!/bin/bash
# Agentic Framework - Quick Start Script
# Usage: ./start.sh [your_api_key]

echo "🚀 AGENTIC FRAMEWORK - QUICK START"
echo "=================================="

# Check if API key provided as argument
if [ "$1" != "" ]; then
    export OPENROUTER_API_KEY="$1"
    echo "✅ API key set from command line (length: ${#1})"
else
    # Try to load from environment files
    if [ -f ~/.zshrc ]; then
        source ~/.zshrc 2>/dev/null
    fi
    if [ -f ~/.bashrc ]; then
        source ~/.bashrc 2>/dev/null
    fi

    # Check if we have a valid API key now
    if [ -z "$OPENROUTER_API_KEY" ] || [ "$OPENROUTER_API_KEY" = "your_key_here" ]; then
        echo "❌ No valid API key found!"
        echo ""
        echo "Usage options:"
        echo "  1. ./start.sh your_api_key_here"
        echo "  2. export OPENROUTER_API_KEY=your_key && ./start.sh"
        echo "  3. python quick_start.py (interactive setup)"
        echo ""
        echo "Get your API key from: https://openrouter.ai/"
        exit 1
    else
        echo "✅ API key loaded from environment (length: ${#OPENROUTER_API_KEY})"
    fi
fi

echo "🔧 Starting backend API server..."
python backend_api.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo "🌐 Starting web interface..."
echo "📱 Interface will open at: http://localhost:8080"
echo "🛑 Press Ctrl+C to stop"
echo "=================================="

# Start web interface (this will block)
python main.py --test

# Cleanup when web interface exits
echo "🛑 Stopping backend server..."
kill $BACKEND_PID 2>/dev/null
echo "✅ Shutdown complete"
