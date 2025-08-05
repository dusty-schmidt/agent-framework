#!/usr/bin/env python3
"""
Simple, Single-Screen TUI for Agentic System Management
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional
from collections import deque

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static, RichLog
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Import our centralized logging
from logging_config import get_agentic_logger


class TierManager:
    """Manages a single tier with proper output capture"""
    
    def __init__(self, name: str, display_name: str, start_cmd: str, cwd: str, 
                 description: str = "", port: Optional[int] = None, color: str = "white"):
        self.name = name
        self.display_name = display_name
        self.start_cmd = start_cmd
        self.cwd = Path(cwd)
        self.description = description
        self.port = port
        self.color = color
        self.process: Optional[subprocess.Popen] = None
        self.start_time: Optional[float] = None
        self.log_buffer = deque(maxlen=100)
        
        # Get logger for this tier
        self.logger_system = get_agentic_logger()
        self.logger = self.logger_system.get_logger(self.name)

    def start(self) -> bool:
        """Start the tier process with proper output capture"""
        if self.is_running():
            return False
            
        try:
            if not self.cwd.exists():
                error_msg = f"Working directory {self.cwd} does not exist"
                self.logger.error(error_msg)
                self.log_buffer.append(f"[{self.color}]ERROR: {error_msg}[/{self.color}]")
                return False
                
            self.logger_system.log_tier_start(self.name, self.start_cmd, str(self.cwd))
            self.log_buffer.append(f"[{self.color}]Starting {self.display_name}...[/{self.color}]")
            
            # For interactive applications, we need to handle them differently
            if "tui" in self.start_cmd.lower():
                # Launch interactive TUI in a new terminal or detached process
                self.process = subprocess.Popen(
                    f"gnome-terminal -- bash -c 'cd \"{self.cwd}\" && {self.start_cmd}; read -p \"Press Enter to close...\"'",
                    shell=True,
                    cwd=str(self.cwd)
                )
            else:
                # Launch with output capture for non-interactive processes
                self.process = subprocess.Popen(
                    self.start_cmd,
                    shell=True,
                    cwd=str(self.cwd),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1
                )
                
                # Start output monitoring thread for non-interactive processes
                threading.Thread(
                    target=self._monitor_output, 
                    daemon=True, 
                    name=f"{self.name}_monitor"
                ).start()
            
            self.start_time = time.time()
            success_msg = f"Started {self.display_name} with PID {self.process.pid}"
            self.logger.info(success_msg)
            self.log_buffer.append(f"[{self.color}]{success_msg}[/{self.color}]")
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to start {self.display_name}: {e}"
            self.logger.error(error_msg)
            self.log_buffer.append(f"[{self.color}]ERROR: {error_msg}[/{self.color}]")
            return False
    
    def stop(self) -> bool:
        """Stop the tier process"""
        if not self.is_running():
            return False
            
        try:
            self.logger_system.log_tier_stop(self.name)
            self.log_buffer.append(f"[{self.color}]Stopping {self.display_name}...[/{self.color}]")
            
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            
            success_msg = f"Stopped {self.display_name}"
            self.logger.info(success_msg)
            self.log_buffer.append(f"[{self.color}]{success_msg}[/{self.color}]")
            self.process = None
            self.start_time = None
            return True
            
        except Exception as e:
            error_msg = f"Error stopping {self.display_name}: {e}"
            self.logger.error(error_msg)
            self.log_buffer.append(f"[{self.color}]ERROR: {error_msg}[/{self.color}]")
            return False
    
    def is_running(self) -> bool:
        """Check if the tier is currently running"""
        if self.process is None:
            return False
        return self.process.poll() is None

    def get_uptime(self) -> int:
        """Get uptime in seconds"""
        if self.start_time and self.is_running():
            return int(time.time() - self.start_time)
        return 0
    
    def get_logs(self) -> List[str]:
        """Get recent log lines"""
        return list(self.log_buffer)

    def _monitor_output(self):
        """Monitor process output in a separate thread"""
        if not self.process or not self.process.stdout:
            return
            
        try:
            while self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line:
                    clean_line = line.strip()
                    self.log_buffer.append(f"[{self.color}]{self.name}: {clean_line}[/{self.color}]")
                    self.logger_system.log_tier_output(self.name, clean_line)
                else:
                    time.sleep(0.1)
        except Exception as e:
            error_msg = f"Output monitoring error: {e}"
            self.log_buffer.append(f"[{self.color}]ERROR: {error_msg}[/{self.color}]")
            self.logger.error(error_msg)


class TierStatusWidget(Static):
    """Compact tier status widget"""
    
    def __init__(self, tier: TierManager, **kwargs):
        super().__init__(**kwargs)
        self.tier = tier
    
    def render(self):
        status_color = "green" if self.tier.is_running() else "red"
        status_text = "🟢 RUNNING" if self.tier.is_running() else "🔴 STOPPED"
        
        table = Table.grid(padding=(0, 1))
        table.add_column(justify="left", width=12)
        table.add_column(justify="left", width=12)
        table.add_column(justify="left", width=8)
        table.add_column(justify="left", width=6)
        
        table.add_row(
            f"[bold {self.tier.color}]{self.tier.display_name}[/bold {self.tier.color}]",
            f"[{status_color}]{status_text}[/{status_color}]",
            f"{self.tier.get_uptime()}s" if self.tier.is_running() else "N/A",
            f":{self.tier.port}" if self.tier.port else ""
        )
        
        return table


class SimpleTUI(App):
    """Simple single-screen TUI for tier management"""

    CSS_PATH = "unified_tui.css"
    TITLE = "Agentic System Manager"
    
    def __init__(self):
        super().__init__()
        
        # Initialize logging
        self.logger_system = get_agentic_logger()
        self.logger = self.logger_system.get_logger('tui')
        
        # Initialize tiers with colors
        root_dir = Path(__file__).parent.parent.parent
        self.tiers = {
            "node": TierManager(
                name="node",
                display_name="Node",
                start_cmd="python run_agent.py",
                cwd=str(root_dir / "node" / "node-agent"),
                description="Single-agent chatbot",
                color="cyan"
            ),
            "link": TierManager(
                name="link",
                display_name="Link",
                start_cmd="python start.py",
                cwd=str(root_dir / "link" / "gob001-mini"),
                description="Multi-persona system",
                port=8001,
                color="green"
            ),
            "mesh": TierManager(
                name="mesh",
                display_name="Mesh",
                start_cmd="python -m uvicorn src.api.server:app --host 0.0.0.0 --port 8080",
                cwd=str(root_dir / "mesh" / "gob01" / "backend"),
                description="Multi-agent coordination",
                port=8080,
                color="yellow"
            ),
            "grid": TierManager(
                name="grid",
                display_name="Grid",
                start_cmd="python start.py",
                cwd=str(root_dir / "grid" / "gob01-unified"),
                description="Self-improving framework",
                port=8001,
                color="magenta"
            )
        }
    
    def compose(self) -> ComposeResult:
        """Create the single-screen UI layout"""
        yield Header()
        
        with Vertical():
            # Title
            yield Static("🚀 [bold]Agentic System Manager[/bold] - Single Screen Control", classes="title")
            
            # Tier status section
            with Container(classes="status-section"):
                yield Static("[bold]Tier Status[/bold]", classes="section-title")
                for name, tier in self.tiers.items():
                    yield TierStatusWidget(tier, id=f"status_{name}")
            
            # Control buttons section
            with Container(classes="controls-section"):
                yield Static("[bold]Controls[/bold]", classes="section-title")
                with Horizontal():
                    yield Button("Start Node", id="start_node", variant="success")
                    yield Button("Stop Node", id="stop_node", variant="error")
                    yield Button("Start Link", id="start_link", variant="success")
                    yield Button("Stop Link", id="stop_link", variant="error")
                with Horizontal():
                    yield Button("Start Mesh", id="start_mesh", variant="success")
                    yield Button("Stop Mesh", id="stop_mesh", variant="error")
                    yield Button("Start Grid", id="start_grid", variant="success")
                    yield Button("Stop Grid", id="stop_grid", variant="error")
            
            # Logs panel
            with Container(classes="logs-section"):
                yield Static("[bold]Live Logs[/bold] (Color-coded by tier)", classes="section-title")
                yield RichLog(id="logs", classes="logs-panel")
        
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        button_id = event.button.id
        
        if not button_id:
            return
            
        parts = button_id.split("_", 1)
        if len(parts) != 2:
            return
            
        action, tier_name = parts
        tier = self.tiers.get(tier_name)
        
        if not tier:
            return
        
        if action == "start":
            if tier.start():
                self.notify(f"Started {tier.display_name}")
                self._refresh_status(tier_name)
            else:
                self.notify(f"Failed to start {tier.display_name}", severity="error")
                
        elif action == "stop":
            if tier.stop():
                self.notify(f"Stopped {tier.display_name}")
                self._refresh_status(tier_name)
            else:
                self.notify(f"Failed to stop {tier.display_name}", severity="error")
    
    def _refresh_status(self, tier_name: str):
        """Refresh status display for a tier"""
        try:
            status_widget = self.query_one(f"#status_{tier_name}")
            status_widget.refresh()
        except Exception as e:
            self.logger.error(f"Error refreshing status for {tier_name}: {e}")
    
    def _update_logs(self):
        """Update the logs panel with color-coded output from all tiers"""
        try:
            logs_widget = self.query_one("#logs", RichLog)
            
            # Collect logs from all tiers
            all_logs = []
            for tier in self.tiers.values():
                recent_logs = tier.get_logs()
                all_logs.extend(recent_logs)
            
            # Sort by timestamp (simple approach - could be improved)
            # For now, just show the most recent logs
            if hasattr(self, '_last_log_count'):
                new_logs = all_logs[self._last_log_count:]
            else:
                new_logs = all_logs[-20:]  # Show last 20 logs on startup
            
            for log_line in new_logs:
                logs_widget.write(log_line)
            
            self._last_log_count = len(all_logs)
            
        except Exception as e:
            self.logger.error(f"Error updating logs: {e}")
    
    def on_mount(self) -> None:
        """Called when the app is mounted"""
        self.title = "Agentic System Manager"
        self.sub_title = "Single-screen tier control with live logs"
        
        # Log TUI startup
        self.logger.info("Simple TUI started")
        session_log = self.logger_system.create_session_log()
        self.logger.info(f"Session log: {session_log}")
        
        # Start log update timer
        self.set_interval(2.0, self._update_logs)
    
    def action_quit(self) -> None:
        """Quit the application and clean up"""
        self.logger.info("Shutting down TUI...")
        
        # Stop all running tiers
        for tier in self.tiers.values():
            if tier.is_running():
                self.logger.info(f"Stopping {tier.display_name} on exit...")
                tier.stop()
        
        self.logger.info("TUI shutdown complete")
        self.exit()


def main():
    """Main entry point"""
    # Ensure we're in the agentic system root directory
    root_dir = Path(__file__).parent.parent.parent
    os.chdir(root_dir)
    
    app = SimpleTUI()
    app.run()


if __name__ == "__main__":
    main()
