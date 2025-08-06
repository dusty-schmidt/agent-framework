#!/usr/bin/env python3
"""
Simple Chat Interface for Testing Agents

A basic command-line chat interface to test agents directly.
Perfect for development before implementing the full frontend.
"""

import asyncio
import sys
from pathlib import Path

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

class SimpleChatInterface:
    """Simple chat interface for testing agents."""
    
    def __init__(self):
        self.central_brain = CentralBrain()
        self.current_tier = "node"
        self.conversation_history = []
        self.session_id = "dev_session"
        
        # Initialize agents
        self.initialize_agents()
    
    def initialize_agents(self):
        """Initialize all tier agents."""
        print("🚀 Initializing agents...")
        
        tiers = ["node", "link", "mesh", "grid"]
        for tier in tiers:
            config = get_model_config(tier)
            self.central_brain.register_tier(tier, {
                "agent_type": f"{tier}_agent",
                "version": "1.0.0",
                "capabilities": ["chat", "memory"],
                "model_config": config
            })
            print(f"✅ {tier} agent ready")
        
        print(f"🎯 Default tier: {self.current_tier}")
    
    async def send_message(self, message: str, tier: str = None):
        """Send a message to an agent and get response."""
        if tier is None:
            tier = self.current_tier
        
        if tier not in self.central_brain.connected_tiers:
            return f"❌ {tier} agent not available"
        
        try:
            # Get tier config
            tier_info = self.central_brain.connected_tiers[tier]
            config = tier_info['config']['model_config']
            
            # Build conversation context
            messages = []
            
            # Add tier-specific system prompt
            system_prompts = {
                "node": "You are a Node tier agent - focused on simple, direct tasks. Be concise and helpful.",
                "link": "You are a Link tier agent - capable of multi-persona interactions. Be versatile and adaptive.",
                "mesh": "You are a Mesh tier agent - specialized in coordination and multi-agent tasks. Think systematically.",
                "grid": "You are a Grid tier agent - advanced and self-improving. Provide thoughtful, analytical responses."
            }

            messages.append({
                "role": "system",
                "content": system_prompts.get(tier, f"You are a {tier} tier agent in the Agentic Framework. Be helpful and concise.")
            })
            
            # Add recent conversation history (last 6 messages)
            recent_history = self.conversation_history[-6:] if self.conversation_history else []
            messages.extend(recent_history)
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Create API payload
            payload = create_model_request_payload(messages, tier)
            headers = get_openrouter_headers()
            
            # Make API call
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config["base_url"] + "/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
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
                            return "❌ No response from agent"
                    else:
                        error_text = await response.text()
                        return f"❌ API Error ({response.status}): {error_text}"
                        
        except Exception as e:
            return f"❌ Error: {e}"
    
    def show_help(self):
        """Show available commands."""
        print("\n📖 Available Commands:")
        print("  /tier <name>     - Switch to tier (node, link, mesh, grid)")
        print("  /status          - Show current status")
        print("  /history         - Show conversation history")
        print("  /clear           - Clear conversation history")
        print("  /help            - Show this help")
        print("  /quit            - Exit chat")
        print("  <message>        - Send message to current tier")
    
    def show_status(self):
        """Show current status."""
        print(f"\n📊 Status:")
        print(f"  Current tier: {self.current_tier}")
        print(f"  Session ID: {self.session_id}")
        print(f"  History length: {len(self.conversation_history)} messages")
        print(f"  Available tiers: {', '.join(self.central_brain.connected_tiers.keys())}")
    
    def show_history(self):
        """Show conversation history."""
        if not self.conversation_history:
            print("\n📝 No conversation history yet.")
            return
        
        print(f"\n📝 Conversation History ({len(self.conversation_history)} messages):")
        for i, msg in enumerate(self.conversation_history[-10:], 1):  # Show last 10
            role = "You" if msg["role"] == "user" else "Agent"
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            print(f"  {i:2}. {role}: {content}")
    
    async def run_chat(self):
        """Run the interactive chat interface."""
        print("💬 Agentic Framework - Simple Chat Interface")
        print("=" * 55)
        print("Chat directly with your agents for testing and development.")
        print("Type '/help' for commands or just start chatting!\n")
        
        while True:
            try:
                # Show current tier in prompt
                user_input = input(f"[{self.current_tier}] You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    command = user_input[1:].lower().split()
                    
                    if command[0] == 'quit' or command[0] == 'exit':
                        print("👋 Goodbye!")
                        break
                    
                    elif command[0] == 'help':
                        self.show_help()
                    
                    elif command[0] == 'status':
                        self.show_status()
                    
                    elif command[0] == 'history':
                        self.show_history()
                    
                    elif command[0] == 'clear':
                        self.conversation_history = []
                        print("🗑️  Conversation history cleared.")
                    
                    elif command[0] == 'tier' and len(command) > 1:
                        new_tier = command[1]
                        if new_tier in self.central_brain.connected_tiers:
                            self.current_tier = new_tier
                            print(f"🔄 Switched to {new_tier} tier")
                        else:
                            print(f"❌ Unknown tier: {new_tier}")
                            print(f"Available: {', '.join(self.central_brain.connected_tiers.keys())}")
                    
                    else:
                        print(f"❌ Unknown command: {command[0]}")
                        print("Type '/help' for available commands.")
                
                else:
                    # Send message to current tier
                    print(f"[{self.current_tier}] Agent: ", end="", flush=True)
                    response = await self.send_message(user_input)
                    print(response)
                
            except KeyboardInterrupt:
                print("\n👋 Chat interrupted. Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break

async def main():
    """Main entry point."""
    chat = SimpleChatInterface()
    await chat.run_chat()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Chat stopped.")
        sys.exit(0)
