"""
Multi-Agent System TUI Interface
A modern terminal user interface with multiple panes for real-time interaction and monitoring.
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import (
    Header, Footer, Static, Input, Button, 
    RichLog, ScrollView, Label
)
from textual.reactive import reactive
from textual.message import Message
from rich.text import Text
from rich.panel import Panel
from rich.console import Console

# Import our multi-agent system components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class LogCapture(logging.Handler):
    """Custom logging handler to capture logs for TUI display"""
    
    def __init__(self, tui_app):
        super().__init__()
        self.tui_app = tui_app
        self.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
    
    def emit(self, record):
        """Emit a log record to the TUI"""
        try:
            msg = self.format(record)
            if self.tui_app:
                self.tui_app.add_log_message(msg, record.levelname)
        except Exception:
            pass  # Avoid infinite loops

class MultiAgentTUI(App):
    """
    Multi-Agent System Terminal User Interface
    
    Features:
    - Conversation pane for chat interactions
    - Real-time log monitoring pane
    - Input field with send functionality
    - Agent status indicators
    """
    
    CSS_PATH = "tui_styles.css"
    TITLE = "Multi-Agent AI System"
    SUB_TITLE = "Real-time Chat & Monitoring Interface"
    
    # Reactive state
    conversation_text = reactive("")
    log_text = reactive("")
    
    def __init__(self):
        super().__init__()
        self.conversation_history: List[dict] = []
        self.log_messages: List[str] = []
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging to capture system logs"""
        # Create custom handler to capture logs
        self.log_handler = LogCapture(self)
        self.log_handler.setLevel(logging.INFO)
        
        # Add handler to root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)
        root_logger.setLevel(logging.INFO)
        
        # Initial log message
        logging.info("Multi-Agent TUI System initialized")
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        with Container(id="main-container"):
            with Horizontal(id="content-area"):
                # Left pane - Conversation
                with Vertical(id="conversation-pane"):
                    yield Label("💬 Conversation", id="conversation-header")
                    yield RichLog(id="conversation-log", highlight=True, markup=True)
                
                # Right pane - System Logs
                with Vertical(id="logs-pane"):
                    yield Label("📋 System Logs", id="logs-header")
                    yield RichLog(id="system-log", highlight=True, markup=True)
            
            # Bottom input area
            with Horizontal(id="input-area"):
                yield Input(placeholder="Type your message here...", id="message-input")
                yield Button("Send", id="send-button", variant="primary")
                yield Button("Clear", id="clear-button", variant="warning")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when app starts."""
        # Set focus to input field
        self.query_one("#message-input", Input).focus()
        
        # Add initial welcome message
        self.add_conversation_message(
            "System", 
            "Welcome to the Multi-Agent AI System! Type your message and press Send.",
            "system"
        )
        
        # Add initial log message
        self.add_log_message("TUI interface ready for interactions", "INFO")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "send-button":
            self.send_message()
        elif event.button.id == "clear-button":
            self.clear_conversation()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission (Enter key)."""
        if event.input.id == "message-input":
            self.send_message()
    
    def send_message(self) -> None:
        """Process and send user message."""
        input_widget = self.query_one("#message-input", Input)
        message = input_widget.value.strip()
        
        if not message:
            return
        
        # Clear input
        input_widget.value = ""
        
        # Add user message to conversation
        self.add_conversation_message("You", message, "user")
        
        # Process message asynchronously
        asyncio.create_task(self.process_message(message))
    
    async def process_message(self, message: str) -> None:
        """Process message through multi-agent system."""
        try:
            # Add processing indicator
            self.add_conversation_message(
                "System", 
                "🤔 Processing your request...", 
                "processing"
            )
            
            # Log the processing start
            logging.info(f"Processing user message: {message[:50]}...")
            
            # TODO: Integrate with actual multi-agent system
            # For now, simulate processing
            await asyncio.sleep(1)
            
            # Simulate agent selection
            if any(word in message.lower() for word in ['code', 'program', 'develop']):
                agent_type = "Developer Agent"
                response = f"🔧 I can help you with software development. You asked: '{message}'"
            elif any(word in message.lower() for word in ['research', 'find', 'analyze']):
                agent_type = "Research Agent"
                response = f"🔍 I'll research that for you. Your query: '{message}'"
            else:
                agent_type = "Main Agent"
                response = f"💬 I'm here to help with general questions. You said: '{message}'"
            
            # Log agent selection
            logging.info(f"Selected {agent_type} for processing")
            
            # Add agent response
            self.add_conversation_message(agent_type, response, "agent")
            
            # Log completion
            logging.info(f"Response generated successfully by {agent_type}")
            
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            self.add_conversation_message(
                "System", 
                f"❌ Error processing message: {str(e)}", 
                "error"
            )
    
    def add_conversation_message(self, sender: str, message: str, msg_type: str = "default") -> None:
        """Add a message to the conversation log."""
        conversation_log = self.query_one("#conversation-log", RichLog)
        
        # Format timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Style based on message type
        if msg_type == "user":
            styled_message = f"[bold blue][{timestamp}] {sender}:[/bold blue] {message}"
        elif msg_type == "agent":
            styled_message = f"[bold green][{timestamp}] {sender}:[/bold green] {message}"
        elif msg_type == "system":
            styled_message = f"[bold yellow][{timestamp}] {sender}:[/bold yellow] {message}"
        elif msg_type == "processing":
            styled_message = f"[bold magenta][{timestamp}] {sender}:[/bold magenta] {message}"
        elif msg_type == "error":
            styled_message = f"[bold red][{timestamp}] {sender}:[/bold red] {message}"
        else:
            styled_message = f"[{timestamp}] {sender}: {message}"
        
        conversation_log.write(styled_message)
        
        # Store in history
        self.conversation_history.append({
            "timestamp": timestamp,
            "sender": sender,
            "message": message,
            "type": msg_type
        })
    
    def add_log_message(self, message: str, level: str = "INFO") -> None:
        """Add a message to the system log."""
        system_log = self.query_one("#system-log", RichLog)
        
        # Format timestamp
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        
        # Style based on log level
        if level == "ERROR":
            styled_message = f"[bold red][{timestamp}] {level}:[/bold red] {message}"
        elif level == "WARNING":
            styled_message = f"[bold yellow][{timestamp}] {level}:[/bold yellow] {message}"
        elif level == "INFO":
            styled_message = f"[bold green][{timestamp}] {level}:[/bold green] {message}"
        elif level == "DEBUG":
            styled_message = f"[dim][{timestamp}] {level}:[/dim] {message}"
        else:
            styled_message = f"[{timestamp}] {level}: {message}"
        
        system_log.write(styled_message)
        
        # Store in log messages
        self.log_messages.append(f"[{timestamp}] {level}: {message}")
        
        # Keep log size manageable (last 1000 messages)
        if len(self.log_messages) > 1000:
            self.log_messages = self.log_messages[-1000:]
    
    def clear_conversation(self) -> None:
        """Clear the conversation log."""
        conversation_log = self.query_one("#conversation-log", RichLog)
        conversation_log.clear()
        
        self.conversation_history.clear()
        
        # Add clear notification
        self.add_conversation_message(
            "System", 
            "Conversation cleared. How can I help you?", 
            "system"
        )
        
        logging.info("Conversation history cleared by user")
    
    def action_quit(self) -> None:
        """Quit the application."""
        logging.info("TUI application shutting down")
        self.exit()

if __name__ == "__main__":
    app = MultiAgentTUI()
    app.run()

