#!/usr/bin/env python3
"""
Test version of Minimal TUI with demo processes
Easy to test - launches simple Python processes that show output
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
from textual.widgets import Header, Footer, Button, Static, RichLog, Input
from textual.message import Message
from rich.text import Text
from pathlib import Path


class RealTierManager:
    """Real tier manager that launches actual processes"""

    def __init__(self, name: str, start_cmd: str, cwd: str, color: str = "white"):
        self.name = name
        self.start_cmd = start_cmd
        self.cwd = Path(cwd)
        self.color = color
        self.process: Optional[subprocess.Popen] = None
        self.start_time: Optional[float] = None
        self.log_buffer = deque(maxlen=100)
        self.chat_history = deque(maxlen=50)
        self.process_ended_logged = False

    def launch(self) -> bool:
        """Launch the real tier process"""
        if self.is_running():
            self.log_buffer.append(f"[{self.color}]{self.name.upper()} already running![/{self.color}]")
            return False

        try:
            if not self.cwd.exists():
                self.log_buffer.append(f"[{self.color}]❌ ERROR: Directory {self.cwd} not found[/{self.color}]")
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
                bufsize=0
            )

            self.start_time = time.time()
            self.process_ended_logged = False
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
            self.log_buffer.append(f"[{self.color}]{self.name.upper()} not running![/{self.color}]")
            return False

        try:
            self.log_buffer.append(f"[{self.color}]🛑 Killing {self.name.upper()}...[/{self.color}]")

            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

            runtime = time.time() - self.start_time if self.start_time else 0
            self.log_buffer.append(f"[{self.color}]💀 {self.name.upper()} killed (ran for {runtime:.1f}s)[/{self.color}]")
            self.process = None
            self.start_time = None
            return True

        except Exception as e:
            self.log_buffer.append(f"[{self.color}]❌ ERROR: Failed to kill {self.name.upper()}: {e}[/{self.color}]")
            return False

    def is_running(self) -> bool:
        """Check if running"""
        if self.process is None:
            return False

        poll_result = self.process.poll()
        is_running = poll_result is None

        if not is_running and poll_result is not None and not self.process_ended_logged:
            self.log_buffer.append(f"[{self.color}]DEBUG: {self.name.upper()} process ended with exit code {poll_result}[/{self.color}]")
            self.process_ended_logged = True

        return is_running

    def get_logs(self) -> List[str]:
        """Get recent logs"""
        return list(self.log_buffer)

    def send_message(self, message: str) -> bool:
        """Real tiers don't support direct messaging yet"""
        self.log_buffer.append(f"[{self.color}]INFO: {self.name.upper()} doesn't support direct messaging yet[/{self.color}]")
        return False

    def get_chat_history(self) -> List[str]:
        """Get chat history"""
        return list(self.chat_history)

    def _monitor_output(self):
        """Monitor process output"""
        if not self.process or not self.process.stdout:
            return

        try:
            while self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line:
                    clean_line = line.strip()
                    self.log_buffer.append(f"[{self.color}]{clean_line}[/{self.color}]")
                else:
                    time.sleep(0.1)

            # Process ended
            if self.process:
                exit_code = self.process.poll()
                if exit_code == 0:
                    self.log_buffer.append(f"[{self.color}]✅ {self.name.upper()} process ended normally[/{self.color}]")
                else:
                    self.log_buffer.append(f"[{self.color}]❌ {self.name.upper()} process crashed (exit code: {exit_code})[/{self.color}]")

        except Exception as e:
            self.log_buffer.append(f"[{self.color}]❌ Monitor error: {e}[/{self.color}]")


class TestTierManager:
    """Test tier manager with chat capability"""

    def __init__(self, name: str, color: str = "white"):
        self.name = name
        self.color = color
        self.process: Optional[subprocess.Popen] = None
        self.start_time: Optional[float] = None
        self.log_buffer = deque(maxlen=100)
        self.chat_history = deque(maxlen=50)
        self.process_ended_logged = False  # Flag to prevent spam

        # Create demo command for this tier - now interactive
        self.demo_cmd = self._get_demo_command()

    def _get_demo_command(self) -> str:
        """Get an interactive demo command for this tier"""
        # Create a simple file-based communication system
        import tempfile
        import os

        # Create a unique message file for this agent
        self.message_file = f"/tmp/agent_{self.name}_{os.getpid()}.txt"

        # Create a simple Python file instead of inline script to avoid escaping issues
        script_file = f"/tmp/agent_{self.name}_script.py"

        script_content = f'''import sys
import time
import os

message_file = "{self.message_file}"
count = 0

print("{self.name.upper()}: Interactive agent started!", flush=True)

try:
    while True:
        # Heartbeat every 10 seconds
        if count % 10 == 0:
            print("{self.name.upper()}: Ready for messages " + str(count // 10), flush=True)

        # Check for messages
        try:
            if os.path.exists(message_file):
                with open(message_file, 'r') as f:
                    content = f.read().strip()
                    if content:
                        lines = content.split('\\n')
                        for line in lines:
                            if line.strip():
                                print("{self.name.upper()}: Received: " + line.strip(), flush=True)
                                print("{self.name.upper()}: Response: I understand '" + line.strip() + "'. How can I help?", flush=True)
                        # Clear the file after processing
                        with open(message_file, 'w') as f:
                            f.write('')
        except Exception as e:
            print("{self.name.upper()}: Error: " + str(e), flush=True)

        time.sleep(1)
        count += 1

except KeyboardInterrupt:
    print("{self.name.upper()}: Agent shutting down", flush=True)
    try:
        if os.path.exists(message_file):
            os.remove(message_file)
    except:
        pass
'''

        # Write script to file
        try:
            with open(script_file, 'w') as f:
                f.write(script_content)
            self.script_file = script_file
            return f'python -u "{script_file}"'
        except Exception as e:
            # Fallback to simple echo if file creation fails
            return f'echo "{self.name.upper()}: Failed to create script: {e}"'

    def launch(self) -> bool:
        """Launch the demo process"""
        if self.is_running():
            self.log_buffer.append(f"[{self.color}]{self.name.upper()} already running![/{self.color}]")
            return False
            
        try:
            self.log_buffer.append(f"[{self.color}]🚀 Launching {self.name.upper()} demo process...[/{self.color}]")
            
            self.process = subprocess.Popen(
                self.demo_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=0  # Unbuffered
            )
            
            self.start_time = time.time()
            self.process_ended_logged = False  # Reset flag for new process
            self.log_buffer.append(f"[{self.color}]✅ {self.name.upper()} started (PID: {self.process.pid})[/{self.color}]")

            # Start output monitoring
            threading.Thread(target=self._monitor_output, daemon=True).start()
            return True
            
        except Exception as e:
            self.log_buffer.append(f"[{self.color}]❌ ERROR: Failed to launch {self.name.upper()}: {e}[/{self.color}]")
            return False
    
    def kill(self) -> bool:
        """Kill the demo process"""
        if not self.is_running():
            self.log_buffer.append(f"[{self.color}]{self.name.upper()} not running![/{self.color}]")
            return False
            
        try:
            self.log_buffer.append(f"[{self.color}]🛑 Killing {self.name.upper()}...[/{self.color}]")

            self.process.terminate()
            try:
                self.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()

            # Clean up files
            try:
                import os
                if hasattr(self, 'message_file') and os.path.exists(self.message_file):
                    os.remove(self.message_file)
                if hasattr(self, 'script_file') and os.path.exists(self.script_file):
                    os.remove(self.script_file)
            except Exception:
                pass

            runtime = time.time() - self.start_time if self.start_time else 0
            self.log_buffer.append(f"[{self.color}]💀 {self.name.upper()} killed (ran for {runtime:.1f}s)[/{self.color}]")
            self.process = None
            self.start_time = None
            return True
            
        except Exception as e:
            self.log_buffer.append(f"[{self.color}]❌ ERROR: Failed to kill {self.name.upper()}: {e}[/{self.color}]")
            return False
    
    def is_running(self) -> bool:
        """Check if running"""
        if self.process is None:
            return False

        # Check if process is still running
        poll_result = self.process.poll()
        is_running = poll_result is None

        # Debug logging - only once per process end
        if not is_running and poll_result is not None and not self.process_ended_logged:
            self.log_buffer.append(f"[{self.color}]DEBUG: {self.name.upper()} process ended with exit code {poll_result}[/{self.color}]")
            self.process_ended_logged = True

        return is_running
    
    def get_logs(self) -> List[str]:
        """Get recent logs"""
        return list(self.log_buffer)

    def send_message(self, message: str) -> bool:
        """Send a message to this agent if it's running"""
        if not self.is_running():
            return False

        try:
            # Write message to the agent's message file
            if hasattr(self, 'message_file'):
                with open(self.message_file, 'a') as f:
                    f.write(f"{message}\n")
                    f.flush()
                self.chat_history.append(f"[bold blue]You:[/bold blue] {message}")
                return True
            else:
                return False
        except Exception as e:
            self.log_buffer.append(f"[{self.color}]❌ Failed to send message: {e}[/{self.color}]")
            return False

    def get_chat_history(self) -> List[str]:
        """Get chat history"""
        return list(self.chat_history)

    def _monitor_output(self):
        """Monitor process output"""
        if not self.process or not self.process.stdout:
            return

        try:
            while self.process and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line:
                    clean_line = line.strip()
                    self.log_buffer.append(f"[{self.color}]{clean_line}[/{self.color}]")
                else:
                    time.sleep(0.1)

            # Process ended - check exit code
            if self.process:
                exit_code = self.process.poll()
                if exit_code == 0:
                    self.log_buffer.append(f"[{self.color}]✅ {self.name.upper()} process ended normally[/{self.color}]")
                else:
                    self.log_buffer.append(f"[{self.color}]❌ {self.name.upper()} process crashed (exit code: {exit_code})[/{self.color}]")

        except Exception as e:
            self.log_buffer.append(f"[{self.color}]❌ Monitor error: {e}[/{self.color}]")


class TierPanel(Container):
    """Simple tier control panel"""
    
    def __init__(self, tier: TestTierManager, **kwargs):
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


class TestMinimalTUI(App):
    """Test version of Minimal TUI with demo processes"""
    
    CSS_PATH = "minimal_tui.css"
    TITLE = "Agentic System - TEST MODE"
    
    def __init__(self):
        super().__init__()
        
        # Initialize real tiers with actual commands
        root_dir = Path(__file__).parent.parent.parent
        self.tiers = {
            "node": RealTierManager(
                name="node",
                start_cmd="python run_agent.py",
                cwd=str(root_dir / "node" / "node-agent"),
                color="cyan"
            ),
            "link": RealTierManager(
                name="link",
                start_cmd="python start.py",
                cwd=str(root_dir / "link" / "gob001-mini"),
                color="green"
            ),
            "mesh": RealTierManager(
                name="mesh",
                start_cmd="python -m uvicorn src.api.server:app --host 0.0.0.0 --port 8080",
                cwd=str(root_dir / "mesh" / "gob01" / "backend"),
                color="yellow"
            ),
            "grid": RealTierManager(
                name="grid",
                start_cmd="python start.py",
                cwd=str(root_dir / "grid" / "gob01-unified"),
                color="magenta"
            )
        }
        
        self.tier_panels = {}
        self._last_log_count = 0
    
    def compose(self) -> ComposeResult:
        """Create the minimal UI layout with separate chat and debug windows"""
        yield Header()

        with Horizontal(classes="main-layout"):
            # Left side: Tier panels
            with Vertical(classes="tiers-column"):
                for name, tier in self.tiers.items():
                    panel = TierPanel(tier, classes="tier-panel-container")
                    self.tier_panels[name] = panel
                    yield panel

            # Right side: Split between chat and debug
            with Vertical(classes="right-column"):
                # Top: Chat interface
                with Vertical(classes="chat-section"):
                    yield Static("AGENT CHAT", classes="section-title")
                    yield RichLog(id="chat", classes="chat-display")

                    # Chat input area
                    with Horizontal(classes="chat-input-area"):
                        yield Input(placeholder="Type message to active agents...", id="chat-input", classes="chat-input")
                        yield Button("SEND", id="send-btn", classes="send-btn")

                # Bottom: Debug/System logs
                with Vertical(classes="debug-section"):
                    yield Static("SYSTEM DEBUG", classes="section-title")
                    yield RichLog(id="debug", classes="debug-display")

        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        button_id = event.button.id

        if not button_id:
            return

        # Handle send button
        if button_id == "send-btn":
            self._send_chat_message()
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
                self._add_chat_message(f"[green]🚀 {tier_name.upper()} agent is now online[/green]")
                self._add_debug_message(f"[green]LAUNCH: {tier_name.upper()} process started (PID: {tier.process.pid if tier.process else 'unknown'})[/green]")
            else:
                self._add_chat_message(f"[red]❌ Failed to launch {tier_name.upper()}[/red]")
                self._add_debug_message(f"[red]LAUNCH FAILED: {tier_name.upper()} could not start[/red]")

        elif action == "kill":
            if tier.kill():
                self._add_chat_message(f"[red]🛑 {tier_name.upper()} agent went offline[/red]")
                self._add_debug_message(f"[red]KILL: {tier_name.upper()} process terminated[/red]")
            else:
                self._add_chat_message(f"[red]❌ Failed to kill {tier_name.upper()}[/red]")
                self._add_debug_message(f"[red]KILL FAILED: {tier_name.upper()} could not be terminated[/red]")

        # Update status
        if tier_name in self.tier_panels:
            self.tier_panels[tier_name].update_status()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission (Enter key)"""
        if event.input.id == "chat-input":
            self._send_chat_message()

    def _send_chat_message(self) -> None:
        """Send message from chat input to all active agents"""
        try:
            chat_input = self.query_one("#chat-input", Input)
            message = chat_input.value.strip()

            if not message:
                return

            # Clear input
            chat_input.value = ""

            # Find active agents
            active_agents = [tier for tier in self.tiers.values() if tier.is_running()]

            # Debug: Show agent status in debug window
            agent_status = []
            for name, tier in self.tiers.items():
                status = "RUNNING" if tier.is_running() else "STOPPED"
                agent_status.append(f"{name.upper()}:{status}")

            self._add_debug_message(f"SEND MESSAGE: Agent status - {', '.join(agent_status)}")

            if not active_agents:
                self._add_chat_message("[yellow]⚠️  No agents are currently active. Launch an agent first![/yellow]")
                self._add_debug_message("[yellow]SEND FAILED: No active agents found[/yellow]")
                return

            # Add user message to chat
            self._add_chat_message(f"[bold blue]You:[/bold blue] {message}")

            # Send to all active agents
            sent_count = 0
            for tier in active_agents:
                if tier.send_message(message):
                    sent_count += 1

            if sent_count > 0:
                agent_names = [tier.name.upper() for tier in active_agents]
                self._add_chat_message(f"[dim]→ Sent to {', '.join(agent_names)}[/dim]")
                self._add_debug_message(f"MESSAGE SENT: Delivered to {sent_count} agents: {', '.join(agent_names)}")
            else:
                self._add_chat_message("[red]❌ Failed to send message to agents[/red]")
                self._add_debug_message("[red]MESSAGE FAILED: Could not deliver to any agents[/red]")

        except Exception as e:
            self._add_chat_message(f"[red]❌ Error sending message: {e}[/red]")
            self._add_debug_message(f"[red]SEND ERROR: {e}[/red]")

    def _add_chat_message(self, message: str) -> None:
        """Add a message to the chat display"""
        try:
            chat_widget = self.query_one("#chat", RichLog)
            chat_widget.write(message)
        except Exception:
            pass

    def _add_debug_message(self, message: str) -> None:
        """Add a message to the debug display"""
        try:
            debug_widget = self.query_one("#debug", RichLog)
            import time
            timestamp = time.strftime("%H:%M:%S")
            debug_widget.write(f"[dim]{timestamp}[/dim] {message}")
        except Exception:
            pass
    
    def _update_displays(self):
        """Update both chat and debug displays"""
        try:
            chat_widget = self.query_one("#chat", RichLog)
            debug_widget = self.query_one("#debug", RichLog)

            # Collect all logs from all tiers
            all_logs = []
            for tier in self.tiers.values():
                tier_logs = tier.get_logs()
                all_logs.extend([(tier.name, log) for log in tier_logs])

            # Show new logs only
            new_logs = all_logs[self._last_log_count:]

            for tier_name, log_line in new_logs:
                # Agent responses go to chat
                if any(keyword in log_line for keyword in ["Received:", "Response:", "Interactive agent started"]):
                    chat_widget.write(log_line)
                # System/debug messages go to debug window
                elif any(keyword in log_line for keyword in ["Ready for messages", "DEBUG:", "ERROR:", "process ended", "crashed"]):
                    debug_widget.write(log_line)
                # Everything else goes to debug
                else:
                    debug_widget.write(log_line)

            self._last_log_count = len(all_logs)

        except Exception:
            pass
    
    def _update_status_indicators(self):
        """Update all status indicators"""
        for name, panel in self.tier_panels.items():
            panel.update_status()
    
    def on_mount(self) -> None:
        """Called when the app is mounted"""
        self.title = "Agentic System - REAL TIER TESTING"
        self.sub_title = "Launch real tier processes and validate their status"

        # Add welcome message to chat
        try:
            chat_widget = self.query_one("#chat", RichLog)
            chat_widget.write("[bold green]🎯 REAL TIER TESTING[/bold green]")
            chat_widget.write("[cyan]1. Click LAUNCH to start real tier processes[/cyan]")
            chat_widget.write("[yellow]2. Monitor startup logs and status[/yellow]")
            chat_widget.write("[magenta]3. Validate each tier launches successfully[/magenta]")
            chat_widget.write("[dim]Process output and responses will appear here[/dim]")
            chat_widget.write("")
        except Exception:
            pass

        # Add welcome message to debug
        try:
            debug_widget = self.query_one("#debug", RichLog)
            debug_widget.write("[bold blue]🔧 TIER VALIDATION DEBUG[/bold blue]")
            debug_widget.write("[dim]Process status, PIDs, exit codes, and system logs[/dim]")
            debug_widget.write("")
        except Exception:
            pass

        # Start update timers
        self.set_interval(0.5, self._update_displays)
        self.set_interval(1.0, self._update_status_indicators)
    
    def action_quit(self) -> None:
        """Quit and cleanup"""
        # Kill all running tiers
        for tier in self.tiers.values():
            if tier.is_running():
                tier.kill()
        
        self.exit()


def main():
    """Main entry point"""
    print("🎯 TEST MODE - Minimal TUI with Demo Processes")
    print("=" * 50)
    print("This will launch simple Python processes that you can see working")
    print("• NODE: Heartbeat every 2 seconds")
    print("• LINK: Processing every 1.5 seconds") 
    print("• MESH: Network sync every 3 seconds")
    print("• GRID: Computing every 2.5 seconds")
    print()
    print("Click LAUNCH to start, KILL to stop, watch the logs!")
    print("Press Ctrl+C to exit")
    print()
    
    app = TestMinimalTUI()
    app.run()


if __name__ == "__main__":
    main()
