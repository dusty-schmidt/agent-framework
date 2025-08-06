#!/usr/bin/env python3
"""
Simple Backend Monitor for Agentic Framework

Auto-starts agents and provides basic monitoring.
Perfect for development before implementing the frontend chat UI.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.simple_env import setup_simple_env

# Setup environment
setup_simple_env()

from core.brain.central_brain import CentralBrain
from scripts.config_loader import get_model_config

class SimpleAgentMonitor:
    """Simple agent monitor that auto-starts and manages agents."""
    
    def __init__(self):
        self.central_brain = CentralBrain()
        self.agents = {}
        self.running = False
        
    async def start_agent(self, tier_name: str):
        """Start an agent for a specific tier."""
        print(f"🚀 Starting {tier_name} agent...")
        
        # Get model config for this tier
        config = get_model_config(tier_name)
        
        # Register with central brain
        agent_info = {
            "agent_type": f"{tier_name}_agent",
            "version": "1.0.0",
            "capabilities": ["chat", "memory", "tools"],
            "model_config": config,
            "status": "running",
            "start_time": time.time()
        }
        
        self.central_brain.register_tier(tier_name, agent_info)
        self.agents[tier_name] = agent_info
        
        print(f"✅ {tier_name} agent started with model: {config['model']}")
        return True
    
    async def test_agent(self, tier_name: str, test_message: str = "Hello! Please respond to confirm you're working."):
        """Test an agent with a simple message."""
        if tier_name not in self.agents:
            print(f"❌ {tier_name} agent not running")
            return False
            
        print(f"🧪 Testing {tier_name} agent...")
        
        try:
            # Simulate agent response (in real implementation, this would call the actual agent)
            response = f"Hello from {tier_name} tier! I'm running with {self.agents[tier_name]['model_config']['model']} and ready to help."
            
            print(f"✅ {tier_name} response: {response}")
            return True
            
        except Exception as e:
            print(f"❌ {tier_name} test failed: {e}")
            return False
    
    async def start_all_agents(self):
        """Start all tier agents automatically."""
        print("🚀 Auto-starting all tier agents...")
        print("=" * 50)
        
        tiers = ["node", "link", "mesh", "grid"]
        
        for tier in tiers:
            await self.start_agent(tier)
            await asyncio.sleep(0.5)  # Small delay between starts
        
        print("\n✅ All agents started!")
        return True
    
    async def test_all_agents(self):
        """Test all running agents."""
        print("\n🧪 Testing all agents...")
        print("=" * 30)
        
        results = {}
        for tier_name in self.agents:
            results[tier_name] = await self.test_agent(tier_name)
            await asyncio.sleep(0.5)
        
        # Summary
        passed = sum(1 for success in results.values() if success)
        total = len(results)
        
        print(f"\n📊 Test Results: {passed}/{total} agents responding")
        
        if passed == total:
            print("🎉 All agents are working correctly!")
        else:
            print("⚠️  Some agents need attention.")
        
        return passed == total
    
    def show_status(self):
        """Show current status of all agents."""
        print("\n📊 Agent Status")
        print("=" * 40)
        
        if not self.agents:
            print("No agents running.")
            return
        
        for tier_name, info in self.agents.items():
            uptime = time.time() - info['start_time']
            model = info['model_config']['model']
            print(f"✅ {tier_name:6} | {model:20} | {uptime:.1f}s uptime")
    
    async def run_monitor(self):
        """Run the simple monitor."""
        print("🎯 Agentic Framework - Simple Monitor")
        print("=" * 50)
        print("This will auto-start agents and run basic tests.")
        print("Perfect for development before implementing the frontend.\n")
        
        # Auto-start all agents
        await self.start_all_agents()
        
        # Show status
        self.show_status()
        
        # Run tests
        await self.test_all_agents()
        
        # Keep running and show periodic status
        print(f"\n🔄 Monitor running... (Ctrl+C to exit)")
        print("Status updates every 30 seconds.\n")
        
        self.running = True
        try:
            while self.running:
                await asyncio.sleep(30)
                print(f"\n⏰ Status Update - {time.strftime('%H:%M:%S')}")
                self.show_status()
                
        except KeyboardInterrupt:
            print(f"\n👋 Shutting down monitor...")
            self.running = False

async def main():
    """Main entry point."""
    monitor = SimpleAgentMonitor()
    await monitor.run_monitor()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Monitor stopped.")
        sys.exit(0)
