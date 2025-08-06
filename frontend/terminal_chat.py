#!/usr/bin/env python3
"""
Terminal-Style Chatbot Interface

Minimalistic, monitor-style chat interface for the Agentic Framework.
Clean terminal aesthetics with simple, functional design.
"""

import asyncio
import sys
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.simple_env import setup_simple_env

# Setup environment
setup_simple_env()

from core.brain.central_brain import CentralBrain
from scripts.config_loader import get_model_config, get_openrouter_headers, create_model_request_payload

try:
    import aiohttp
except ImportError:
    print("Installing aiohttp...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
    import aiohttp

class TerminalChatbot:
    """Minimalistic terminal-style chatbot interface."""
    
    def __init__(self):
        self.central_brain = CentralBrain()
        self.current_tier = "node"
        self.conversation_history = []
        self.session_start = time.time()
        self.message_count = 0
        
        # Terminal styling
        self.colors = {
            'header': '\033[96m',      # Cyan
            'tier': '\033[93m',        # Yellow
            'user': '\033[92m',        # Green
            'agent': '\033[94m',       # Blue
            'system': '\033[90m',      # Gray
            'error': '\033[91m',       # Red
            'reset': '\033[0m',        # Reset
            'bold': '\033[1m',         # Bold
            'dim': '\033[2m'           # Dim
        }
        
        self.initialize_agents()
    
    def print_header(self):
        """Print the terminal header."""
        c = self.colors
        print(f"{c['header']}{c['bold']}================================================================{c['reset']}")
        print(f"{c['header']}{c['bold']}                    AGENTIC FRAMEWORK                         {c['reset']}")
        print(f"{c['header']}{c['bold']}                  TERMINAL CHAT INTERFACE                     {c['reset']}")
        print(f"{c['header']}{c['bold']}================================================================{c['reset']}")
        print()
    
    def print_status_bar(self):
        """Print current status bar."""
        c = self.colors
        uptime = int(time.time() - self.session_start)
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"{c['system']}{c['dim']}>> STATUS: Tier: {c['tier']}{self.current_tier:6}{c['system']}{c['dim']} | Messages: {self.message_count:3} | Uptime: {uptime:3}s | {timestamp}{c['reset']}")
        print()
    
    def initialize_agents(self):
        """Initialize all tier agents."""
        c = self.colors
        print(f"{c['system']}>> Initializing agents...{c['reset']}")

        tiers = ["node", "link", "mesh", "grid"]
        for tier in tiers:
            config = get_model_config(tier)
            self.central_brain.register_tier(tier, {
                "agent_type": f"{tier}_agent",
                "version": "1.0.0",
                "capabilities": ["chat", "memory"],
                "model_config": config
            })
            print(f"{c['system']}>> {tier} agent ready{c['reset']}")

        print(f"{c['system']}>> All agents initialized{c['reset']}")
        print()
    
    async def send_message(self, message: str):
        """Send message to current tier and get response."""
        c = self.colors
        
        if self.current_tier not in self.central_brain.connected_tiers:
            return f"{c['error']}ERROR: {self.current_tier} agent not available{c['reset']}"
        
        try:
            # Get tier config
            tier_info = self.central_brain.connected_tiers[self.current_tier]
            config = tier_info['config']['model_config']
            
            # Build messages with system prompt
            system_prompts = {
                "node": "You are a Node tier agent. Be direct and concise.",
                "link": "You are a Link tier agent. Be versatile and helpful.",
                "mesh": "You are a Mesh tier agent. Focus on coordination and organization.",
                "grid": "You are a Grid tier agent. Provide analytical, thoughtful responses."
            }
            
            messages = [
                {"role": "system", "content": system_prompts[self.current_tier]},
                {"role": "user", "content": message}
            ]
            
            # Add recent conversation context (last 4 messages)
            if len(self.conversation_history) > 0:
                recent = self.conversation_history[-4:]
                messages = [messages[0]] + recent + [messages[1]]
            
            payload = create_model_request_payload(messages, self.current_tier)
            headers = get_openrouter_headers()
            
            # Show thinking indicator
            print(f"{c['system']}{c['dim']}>> [{self.current_tier.upper()}] Processing...{c['reset']}", end="", flush=True)
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config["base_url"] + "/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    # Clear thinking indicator
                    print(f"\r{' ' * 30}\r", end="", flush=True)
                    
                    if response.status == 200:
                        data = await response.json()
                        if 'choices' in data and len(data['choices']) > 0:
                            response_text = data['choices'][0]['message']['content']
                            
                            # Update conversation history
                            self.conversation_history.append({"role": "user", "content": message})
                            self.conversation_history.append({"role": "assistant", "content": response_text})
                            
                            # Keep history manageable
                            if len(self.conversation_history) > 20:
                                self.conversation_history = self.conversation_history[-20:]
                            
                            return response_text
                        else:
                            return f"{c['error']}[ERROR] No response from agent{c['reset']}"
                    else:
                        return f"{c['error']}[ERROR] API returned {response.status}{c['reset']}"
                        
        except Exception as e:
            print(f"\r{' ' * 30}\r", end="", flush=True)
            return f"{c['error']}[ERROR] {e}{c['reset']}"
    
    def handle_command(self, command: str):
        """Handle system commands."""
        c = self.colors
        parts = command[1:].split()
        
        if not parts:
            return
        
        cmd = parts[0].lower()
        
        if cmd == "tier" and len(parts) > 1:
            new_tier = parts[1].lower()
            if new_tier in self.central_brain.connected_tiers:
                self.current_tier = new_tier
                print(f"{c['system']}>> Switched to {new_tier} tier{c['reset']}")
            else:
                print(f"{c['error']}>> [ERROR] Unknown tier: {new_tier}{c['reset']}")
                print(f"{c['system']}>> Available: {', '.join(self.central_brain.connected_tiers.keys())}{c['reset']}")

        elif cmd == "clear":
            self.conversation_history = []
            print(f"{c['system']}>> Conversation history cleared{c['reset']}")

        elif cmd == "status":
            print(f"{c['system']}>> Current tier: {self.current_tier}{c['reset']}")
            print(f"{c['system']}>> Messages: {self.message_count}{c['reset']}")
            print(f"{c['system']}>> History: {len(self.conversation_history)} entries{c['reset']}")

        elif cmd == "help":
            print(f"{c['system']}>> Available commands:{c['reset']}")
            print(f"{c['system']}  /tier <name>  - Switch tier (node, link, mesh, grid){c['reset']}")
            print(f"{c['system']}  /clear        - Clear conversation history{c['reset']}")
            print(f"{c['system']}  /status       - Show current status{c['reset']}")
            print(f"{c['system']}  /help         - Show this help{c['reset']}")
            print(f"{c['system']}  /quit         - Exit chat{c['reset']}")

        elif cmd == "quit" or cmd == "exit":
            return "quit"

        else:
            print(f"{c['error']}>> [ERROR] Unknown command: {cmd}{c['reset']}")
            print(f"{c['system']}>> Type /help for available commands{c['reset']}")
    
    async def run_chat(self):
        """Run the terminal chat interface."""
        c = self.colors
        
        # Clear screen and show header
        print("\033[2J\033[H", end="")  # Clear screen, move cursor to top
        self.print_header()
        self.print_status_bar()
        
        print(f"{c['system']}>> Terminal chat ready. Type /help for commands.{c['reset']}")
        print(f"{c['system']}>> Current tier: {c['tier']}{self.current_tier}{c['reset']}")
        print()
        
        while True:
            try:
                # Show prompt
                prompt = f"{c['user']}{c['bold']}[{self.current_tier.upper()}] You:{c['reset']} "
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    result = self.handle_command(user_input)
                    if result == "quit":
                        break
                    continue
                
                # Send message to agent
                self.message_count += 1
                print(f"{c['agent']}{c['bold']}[{self.current_tier.upper()}] Agent:{c['reset']} ", end="", flush=True)
                
                response = await self.send_message(user_input)
                print(response)
                print()  # Add spacing
                
            except KeyboardInterrupt:
                print(f"\n{c['system']}>> Chat interrupted. Goodbye!{c['reset']}")
                break
            except EOFError:
                print(f"\n{c['system']}>> Goodbye!{c['reset']}")
                break

        # Show session summary
        session_time = int(time.time() - self.session_start)
        print(f"{c['system']}{c['dim']}>> Session ended. Duration: {session_time}s, Messages: {self.message_count}{c['reset']}")

async def main():
    """Main entry point."""
    chatbot = TerminalChatbot()
    await chatbot.run_chat()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
