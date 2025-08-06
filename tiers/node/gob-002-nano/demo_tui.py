#!/usr/bin/env python3
"""
Simple TUI Demo to test the multi-agent system interface
"""

import asyncio
import logging
from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Button, RichLog, Label

class SimpleTUIDemo(App):
    """Simple TUI Demo for Multi-Agent System"""
    
    TITLE = "Multi-Agent System Demo"
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        with Container():
            with Horizontal():
                # Left pane - Conversation
                with Vertical():
                    yield Label("💬 Conversation")
                    yield RichLog(id="conversation", highlight=True, markup=True)
                
                # Right pane - System Logs
                with Vertical():
                    yield Label("📋 System Logs")
                    yield RichLog(id="logs", highlight=True, markup=True)
            
            # Bottom input area
            with Horizontal():
                yield Input(placeholder="Type your message...", id="input")
                yield Button("Send", id="send", variant="primary")
                yield Button("Clear", id="clear", variant="warning")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when app starts."""
        self.query_one("#input", Input).focus()
        
        # Add welcome messages
        conv_log = self.query_one("#conversation", RichLog)
        sys_log = self.query_one("#logs", RichLog)
        
        conv_log.write("[bold yellow]System:[/bold yellow] Welcome to Multi-Agent System!")
        conv_log.write("[bold yellow]System:[/bold yellow] Try commands like 'write code', 'research topic', or 'adjust behavior'")
        
        sys_log.write("[bold green]INFO:[/bold green] TUI Demo initialized")
        sys_log.write("[bold green]INFO:[/bold green] Multi-agent system ready")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "send":
            self.send_message()
        elif event.button.id == "clear":
            self.clear_conversation()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        if event.input.id == "input":
            self.send_message()
    
    def send_message(self) -> None:
        """Process and send user message."""
        input_widget = self.query_one("#input", Input)
        message = input_widget.value.strip()
        
        if not message:
            return
        
        input_widget.value = ""
        
        # Add to conversation
        conv_log = self.query_one("#conversation", RichLog)
        sys_log = self.query_one("#logs", RichLog)
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        conv_log.write(f"[bold blue][{timestamp}] You:[/bold blue] {message}")
        sys_log.write(f"[bold green]INFO:[/bold green] Processing message: {message[:50]}...")
        
        # Simple agent simulation
        asyncio.create_task(self.process_message(message))
    
    async def process_message(self, message: str):
        """Simulate agent processing."""
        conv_log = self.query_one("#conversation", RichLog)
        sys_log = self.query_one("#logs", RichLog)
        
        # Add processing indicator
        conv_log.write("[bold magenta]System:[/bold magenta] 🤔 Processing...")
        
        # Simulate processing delay
        await asyncio.sleep(1)
        
        # Simulate agent selection
        if any(word in message.lower() for word in ['code', 'program', 'develop']):
            agent = "Developer Agent"
            response = f"🔧 I'll help you with development. You asked: '{message}'"
            sys_log.write("[bold green]INFO:[/bold green] Selected Developer Agent")
        elif any(word in message.lower() for word in ['research', 'find', 'analyze']):
            agent = "Research Agent"
            response = f"🔍 I'll research that for you. Query: '{message}'"
            sys_log.write("[bold green]INFO:[/bold green] Selected Research Agent")
        elif message.lower().startswith('adjust behavior'):
            agent = "System"
            response = "✅ Behavior adjustment received and processed"
            sys_log.write("[bold green]INFO:[/bold green] Behavior adjustment applied")
        else:
            agent = "Main Agent"
            response = f"💬 I can help with that. You said: '{message}'"
            sys_log.write("[bold green]INFO:[/bold green] Selected Main Agent")
        
        # Add response
        timestamp = datetime.now().strftime("%H:%M:%S")
        conv_log.write(f"[bold green][{timestamp}] {agent}:[/bold green] {response}")
        sys_log.write(f"[bold green]INFO:[/bold green] Response generated successfully")
    
    def clear_conversation(self) -> None:
        """Clear the conversation."""
        conv_log = self.query_one("#conversation", RichLog)
        sys_log = self.query_one("#logs", RichLog)
        
        conv_log.clear()
        conv_log.write("[bold yellow]System:[/bold yellow] Conversation cleared. How can I help?")
        sys_log.write("[bold green]INFO:[/bold green] Conversation cleared by user")

if __name__ == "__main__":
    app = SimpleTUIDemo()
    app.run()
