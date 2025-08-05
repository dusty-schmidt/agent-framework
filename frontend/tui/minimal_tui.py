#!/usr/bin/env python3
"""
Minimal TUI for Agentic System Management
Simple panels for each tier + logs panel
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
from rich.text import Text

# Import our centralized logging
from logging_config import get_agentic_logger


class TierManager:
    """Simple tier manager"""
    
    def __init__(self, name: str, start_cmd: str, cwd: str, color: str = "white"):
        self.name = name
        self.start_cmd = start_cmd
        self.cwd = Path(cwd)
        self.color = color
        self.process: Optional[subprocess.Popen] = None
        self.start_time: Optional[float] = None
        self.log_buffer = deque(maxlen=50)
        
        # Get logger for this tier
        self.logger_system = get_agentic_logger()
        self.logger = self.logger_system.get_logger(self.name)

    def launch(self) -> bool:
        """Launch the tier process"""
        if self.is_running():
            self.log_buffer.append(f"[{self.color}]{self.name.upper()} already running![/{self.color}]")
            return False

        try:
            if not self.cwd.exists():
                self.log_buffer.append(f"[{self.color}]❌ ERROR: Directory {self.cwd} not found[/{self.color}]")
                self.log_buffer.append(f"[{self.color}]   Create the directory or check your tier configuration[/{self.color}]")
                return False

            self.log_buffer.append(f"[{self.color}]🚀 Launching {self.name.upper()}...[/{self.color}]")
            self.log_buffer.append(f"[{self.color}]   Command: {self.start_cmd}[/{self.color}]")
            self.log_buffer.append(f"[{self.color}]   Directory: {self.cwd}[/{self.color}]")

            self.process = subprocess.Popen(
                self.start_cmd,
                shell=True,
                cwd=str(self.cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            self.start_time = time.time()
            self.log_buffer.append(f"[{self.color}]✅ {self.name.upper()} started (PID: {self.process.pid})[/{self.color}]")

            # Start output monitoring
            threading.Thread(target=self._monitor_output, daemon=True).start()
            return True

        except Exception as e:
            self.log_buffer.append(f"[{self.color}]❌ ERROR: Failed to launch {self.name.upper()}: {e}[/{self.color}]")
            return False
    
    def kill(self) -> bool:
        """Kill the tier process"""
        if not self.is_running():
            return False
            
        try:
            self.log_buffer.append(f"[{self.color}]Killing {self.name.upper()}...[/{self.color}]")
            
            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            
            self.log_buffer.append(f"[{self.color}]{self.name.upper()} killed[/{self.color}]")
            self.process = None
            self.start_time = None
            return True
            
        except Exception as e:
            self.log_buffer.append(f"[{self.color}]ERROR: Failed to kill {self.name.upper()}: {e}[/{self.color}]")
            return False
    
    def is_running(self) -> bool:
        """Check if running"""
        if self.process is None:
            return False
        return self.process.poll() is None
    
    def get_logs(self) -> List[str]:
        """Get recent logs"""
        return list(self.log_buffer)

    def _monitor_output(self):
        """Monitor process output"""
        if not self.process or not self.process.stdout:
            return
            
        try:
            while self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line:
                    clean_line = line.strip()
                    self.log_buffer.append(f"[{self.color}]{self.name.upper()}: {clean_line}[/{self.color}]")
                else:
                    time.sleep(0.1)
        except Exception as e:
            self.log_buffer.append(f"[{self.color}]ERROR: Monitor failed: {e}[/{self.color}]")


class TierPanel(Container):
    """Simple tier control panel"""
    
    def __init__(self, tier: TierManager, **kwargs):
        super().__init__(**kwargs)
        self.tier = tier
    
    def compose(self) -> ComposeResult:
        with Horizontal(classes="tier-panel"):
            yield Static(self.tier.name.upper(), classes="tier-name")
            yield Button("LAUNCH", id=f"launch_{self.tier.name}", classes="launch-btn")
            yield Button("KILL", id=f"kill_{self.tier.name}", classes="kill-btn")
            yield Static("●", id=f"status_{self.tier.name}", classes="status-indicator")
    
    def update_status(self):
        """Update the status indicator"""
        try:
            status_widget = self.query_one(f"#status_{self.tier.name}")
            if self.tier.is_running():
                status_widget.update("●")
                status_widget.add_class("running")
                status_widget.remove_class("stopped")
            else:
                status_widget.update("●")
                status_widget.add_class("stopped")
                status_widget.remove_class("running")
        except Exception:
            pass


class MinimalTUI(App):
    """Minimal TUI matching the mockup design"""
    
    CSS_PATH = "minimal_tui.css"
    TITLE = "Agentic System"
    
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
                start_cmd="python run_agent.py",
                cwd=str(root_dir / "node" / "node-agent"),
                color="cyan"
            ),
            "link": TierManager(
                name="link",
                start_cmd="python start.py",
                cwd=str(root_dir / "link" / "gob001-mini"),
                color="green"
            ),
            "mesh": TierManager(
                name="mesh",
                start_cmd="python -m uvicorn src.api.server:app --host 0.0.0.0 --port 8080",
                cwd=str(root_dir / "mesh" / "gob01" / "backend"),
                color="yellow"
            ),
            "grid": TierManager(
                name="grid",
                start_cmd="python start.py",
                cwd=str(root_dir / "grid" / "gob01-unified"),
                color="magenta"
            )
        }
        
        self.tier_panels = {}
    
    def compose(self) -> ComposeResult:
        """Create the minimal UI layout"""
        yield Header()
        
        with Horizontal(classes="main-layout"):
            # Left side: Tier panels
            with Vertical(classes="tiers-column"):
                for name, tier in self.tiers.items():
                    panel = TierPanel(tier, classes="tier-panel-container")
                    self.tier_panels[name] = panel
                    yield panel
            
            # Right side: Logs panel
            with Vertical(classes="logs-column"):
                yield Static("LOGS", classes="logs-title")
                yield RichLog(id="logs", classes="logs-display")
        
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
        
        if action == "launch":
            if tier.launch():
                self.notify(f"{tier_name.upper()} launched")
            else:
                self.notify(f"Failed to launch {tier_name.upper()}", severity="error")
                
        elif action == "kill":
            if tier.kill():
                self.notify(f"{tier_name.upper()} killed")
            else:
                self.notify(f"Failed to kill {tier_name.upper()}", severity="error")
        
        # Update status
        if tier_name in self.tier_panels:
            self.tier_panels[tier_name].update_status()
    
    def _update_logs(self):
        """Update the logs panel with color-coded output"""
        try:
            logs_widget = self.query_one("#logs", RichLog)
            
            # Collect all logs from all tiers
            all_logs = []
            for tier in self.tiers.values():
                all_logs.extend(tier.get_logs())
            
            # Show new logs only
            if hasattr(self, '_last_log_count'):
                new_logs = all_logs[self._last_log_count:]
            else:
                new_logs = all_logs[-10:]  # Show last 10 on startup
            
            for log_line in new_logs:
                logs_widget.write(log_line)
            
            self._last_log_count = len(all_logs)
            
        except Exception as e:
            self.logger.error(f"Error updating logs: {e}")
    
    def _update_status_indicators(self):
        """Update all status indicators"""
        for name, panel in self.tier_panels.items():
            panel.update_status()
    
    def on_mount(self) -> None:
        """Called when the app is mounted"""
        self.title = "Agentic System"
        self.sub_title = "Minimal tier control"
        
        # Log startup
        self.logger.info("Minimal TUI started")
        
        # Start update timers
        self.set_interval(1.0, self._update_logs)
        self.set_interval(2.0, self._update_status_indicators)
    
    def action_quit(self) -> None:
        """Quit and cleanup"""
        self.logger.info("Shutting down...")
        
        # Kill all running tiers
        for tier in self.tiers.values():
            if tier.is_running():
                tier.kill()
        
        self.exit()


def main():
    """Main entry point"""
    # Ensure we're in the agentic system root directory
    root_dir = Path(__file__).parent.parent.parent
    os.chdir(root_dir)
    
    app = MinimalTUI()
    app.run()


if __name__ == "__main__":
    main()
