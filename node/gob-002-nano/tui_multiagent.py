#!/usr/bin/env python3
"""
Integrated Multi-Agent System with TUI Frontend
Combines the multi-agent system with the TUI interface for real-time interaction and monitoring.
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import List, Optional

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Button, RichLog, Label
from textual.reactive import reactive

# Import our multi-agent components
from core.base_agent import BaseAgent, AgentRequest, AgentResponse, AgentCapability
from core.coordinator.agent_coordinator import AgentCoordinator
from core.utils.utility_agent import UtilityAgent
from agents.main.main_agent import MainAgent
from agents.developer.developer_agent import DeveloperAgent
from agents.research.research_agent import ResearchAgent
from agents.simple_gemini_bot import GeminiProvider
from loaders.config_loader import load_config
from tools.embed_memory import VectorMemory

class LogCapture(logging.Handler):
    """Custom logging handler to capture logs for TUI display"""
    
    def __init__(self, tui_app):
        super().__init__()
        self.tui_app = tui_app
        self.setFormatter(logging.Formatter(
            '%(name)s - %(levelname)s - %(message)s'
        ))
    
    def emit(self, record):
        """Emit a log record to the TUI"""
        try:
            msg = self.format(record)
            if self.tui_app and hasattr(self.tui_app, 'add_log_message'):
                self.tui_app.add_log_message(msg, record.levelname)
        except Exception:
            pass  # Avoid infinite loops

class MultiAgentTUI(App):
    """
    Multi-Agent System Terminal User Interface with Real Backend Integration
    """
    
    CSS_PATH = "interfaces/tui_styles.css"
    TITLE = "Multi-Agent AI System"
    SUB_TITLE = "Real-time Chat & System Monitoring"
    
    def __init__(self):
        super().__init__()
        self.conversation_history: List[dict] = []
        self.log_messages: List[str] = []
        self.setup_logging()
        self.setup_multi_agent_system()
        
    def setup_logging(self):
        """Setup logging to capture system logs"""
        # Create custom handler to capture logs
        self.log_handler = LogCapture(self)
        self.log_handler.setLevel(logging.INFO)
        
        # Configure root logger
        root_logger = logging.getLogger()
        
        # Remove existing handlers to avoid duplicates
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Add our custom handler
        root_logger.addHandler(self.log_handler)
        root_logger.setLevel(logging.INFO)
        
        # Initial log message
        logging.info("Multi-Agent TUI System initialized")
    
    def setup_multi_agent_system(self):
        """Initialize the multi-agent system components"""
        try:
            logging.info("Initializing multi-agent system components...")
            
            # Load configuration
            config_dict = load_config("config/config.json")
            api_key = config_dict["api_key"]
            model = config_dict.get("model", "gemini-1.5-flash")
            
            # Initialize Gemini provider
            self.gemini_provider = GeminiProvider(
                api_key,
                model=model,
                system_prompt=config_dict.get("system_prompt", "You are a helpful AI assistant."),
                user_prompt_prefix=config_dict.get("user_prompt_prefix", "")
            )
            
            # Initialize memory system
            self.memory = VectorMemory(
                embedding_model="all-MiniLM-L6-v2",
                persist_path="memory/vector_memory.json"
            )
            
            # Initialize utility agent
            self.utility_agent = UtilityAgent(self.memory)
            
            # Initialize specialized agents
            self.main_agent = MainAgent()
            self.developer_agent = DeveloperAgent(self.gemini_provider)
            self.research_agent = ResearchAgent(self.gemini_provider)
            
            # Note: Will load adjustments after mount
            
            # Initialize coordinator with all agents
            self.agents = [
                self.main_agent,
                self.developer_agent, 
                self.research_agent,
                self.utility_agent
            ]
            
            self.coordinator = AgentCoordinator(self.agents)
            
            logging.info(f"Multi-agent system initialized with {len(self.agents)} agents")
            
        except Exception as e:
            logging.error(f"Failed to initialize multi-agent system: {e}")
            # Initialize with minimal setup
            self.coordinator = None
            self.agents = []
    
    async def _load_agent_adjustments(self):
        """Load previous agent adjustments"""
        try:
            for agent in [self.main_agent, self.developer_agent, self.research_agent, self.utility_agent]:
                await agent.load_adjustments()
        except Exception as e:
            logging.warning(f"Could not load agent adjustments: {e}")
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        with Container(id="main-container"):
            with Horizontal(id="content-area"):
                # Left pane - Conversation (2/3 width)
                with Vertical(id="conversation-pane"):
                    yield Label("💬 Multi-Agent Conversation", id="conversation-header")
                    yield RichLog(id="conversation-log", highlight=True, markup=True)
                
                # Right pane - System Logs (1/3 width)
                with Vertical(id="logs-pane"):
                    yield Label("📋 System Logs", id="logs-header")
                    yield RichLog(id="system-log", highlight=True, markup=True)
            
            # Bottom input area
            with Horizontal(id="input-area"):
                yield Input(placeholder="Ask any question or give a command...", id="message-input")
                yield Button("Send", id="send-button", variant="primary")
                yield Button("Clear Chat", id="clear-button", variant="warning")
                yield Button("Adjust Behavior", id="adjust-button", variant="default")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Called when app starts."""
        # Set focus to input field
        self.query_one("#message-input", Input).focus()
        
        # Add initial welcome message
        self.add_conversation_message(
            "System", 
            "🚀 Multi-Agent AI System Ready! I have specialized agents for development, research, and general tasks.",
            "system"
        )
        
        # Show available commands
        self.add_conversation_message(
            "System",
            "Commands: 'adjust behavior <feedback>' to improve responses, 'schedule task <description>' for task management, or just ask anything!",
            "system"
        )
        
        # Add initial log message
        self.add_log_message("TUI interface ready - multi-agent system online", "INFO")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "send-button":
            self.send_message()
        elif event.button.id == "clear-button":
            self.clear_conversation()
        elif event.button.id == "adjust-button":
            self.show_adjust_dialog()
    
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
                "🤔 Analyzing request and selecting appropriate agent...", 
                "processing"
            )
            
            # Check for special commands
            if message.lower().startswith("adjust behavior"):
                await self.handle_behavior_adjustment(message)
                return
            elif message.lower().startswith("schedule task"):
                await self.handle_task_scheduling(message)
                return
            
            # Process through coordinator if available
            if self.coordinator:
                # Route to appropriate agent
                response = await self.coordinator.route_request(message)
                
                if response and response.success:
                    # Add agent response
                    agent_name = response.agent_id.replace("_", " ").title()
                    self.add_conversation_message(
                        f"{agent_name} Agent", 
                        response.content, 
                        "agent"
                    )
                    
                    # Process successful interaction through utility agent
                    if response.confidence > 0.7:
                        await self.utility_agent.process_successful_interaction(
                            message, response.content, response.confidence
                        )
                    
                    # Log agent metrics
                    logging.info(f"Response from {agent_name}: confidence={response.confidence:.2f}")
                    
                else:
                    # Handle failed response
                    self.add_conversation_message(
                        "System", 
                        "❌ Sorry, I couldn't process your request. Please try rephrasing.",
                        "error"
                    )
            else:
                # Fallback if coordinator not available
                self.add_conversation_message(
                    "System",
                    "⚠️ Multi-agent system not fully initialized. Please check configuration.",
                    "error"
                )
                
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            self.add_conversation_message(
                "System", 
                f"❌ Error processing message: {str(e)}", 
                "error"
            )
    
    async def handle_behavior_adjustment(self, message: str) -> None:
        """Handle behavior adjustment commands"""
        try:
            # Extract feedback from message
            feedback = message[len("adjust behavior"):].strip()
            if not feedback:
                self.add_conversation_message(
                    "System",
                    "Please provide feedback after 'adjust behavior'. Example: 'adjust behavior be more detailed'",
                    "system"
                )
                return
            
            # Apply adjustment to all agents
            for agent in self.agents:
                await agent.adjust_behavior(feedback)
            
            self.add_conversation_message(
                "System",
                f"✅ Behavior adjusted based on feedback: '{feedback}'. All agents have been updated.",
                "system"
            )
            
            logging.info(f"Behavior adjustment applied: {feedback}")
            
        except Exception as e:
            logging.error(f"Error adjusting behavior: {e}")
            self.add_conversation_message(
                "System",
                f"❌ Error adjusting behavior: {str(e)}",
                "error"
            )
    
    async def handle_task_scheduling(self, message: str) -> None:
        """Handle task scheduling commands"""
        try:
            # Extract task description
            task_description = message[len("schedule task"):].strip()
            if not task_description:
                self.add_conversation_message(
                    "System",
                    "Please provide a task description after 'schedule task'. Example: 'schedule task review code tomorrow'",
                    "system"
                )
                return
            
            # Create task JSON structure
            import json
            task = {
                "id": f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "description": task_description,
                "created": datetime.now().isoformat(),
                "status": "scheduled",
                "priority": "normal"
            }
            
            # Ensure tasks directory exists
            os.makedirs("tasks", exist_ok=True)
            
            # Save task to file
            task_file = f"tasks/{task['id']}.json"
            with open(task_file, 'w') as f:
                json.dump(task, f, indent=2)
            
            self.add_conversation_message(
                "System",
                f"✅ Task scheduled: '{task_description}' (ID: {task['id']})",
                "system"
            )
            
            logging.info(f"Task scheduled: {task['id']} - {task_description}")
            
        except Exception as e:
            logging.error(f"Error scheduling task: {e}")
            self.add_conversation_message(
                "System",
                f"❌ Error scheduling task: {str(e)}",
                "error"
            )
    
    def show_adjust_dialog(self) -> None:
        """Show a quick adjustment dialog"""
        # For now, just prompt in conversation
        self.add_conversation_message(
            "System",
            "💡 To adjust my behavior, type: 'adjust behavior <your feedback>'\nExamples:\n- 'adjust behavior be more technical'\n- 'adjust behavior provide more examples'\n- 'adjust behavior be more concise'",
            "system"
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
        try:
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
                
        except Exception:
            # Fail silently to avoid log loops
            pass
    
    def clear_conversation(self) -> None:
        """Clear the conversation log."""
        conversation_log = self.query_one("#conversation-log", RichLog)
        conversation_log.clear()
        
        self.conversation_history.clear()
        
        # Add clear notification
        self.add_conversation_message(
            "System", 
            "🔄 Conversation cleared. How can I help you?", 
            "system"
        )
        
        logging.info("Conversation history cleared by user")
    
    def action_quit(self) -> None:
        """Quit the application."""
        logging.info("TUI application shutting down")
        self.exit()

def main():
    """Main entry point"""
    # Ensure required directories exist
    os.makedirs("tasks", exist_ok=True)
    os.makedirs("config/agents", exist_ok=True)
    
    # Run the TUI application
    app = MultiAgentTUI()
    app.run()

if __name__ == "__main__":
    main()
