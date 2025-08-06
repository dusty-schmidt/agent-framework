#!/bin/bash
# Terminal Chat Launcher
# Ensures zsh environment is loaded before starting the chat interface

echo "🚀 Loading environment and starting Terminal Chat..."
source ~/.zshrc
python frontend/terminal_chat.py
