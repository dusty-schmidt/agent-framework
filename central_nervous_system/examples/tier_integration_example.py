"""
Example of how tiers integrate with the Central Nervous System.

This demonstrates the simple interface that all tiers use to access
the unified memory, knowledge, tools, and system prompts.
"""

import asyncio
from pathlib import Path
import sys

# Add the parent directories to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from central_nervous_system import CentralBrain, get_central_brain


class ExampleTierAgent:
    """
    Example tier agent showing integration with Central Brain.
    
    This demonstrates the pattern that all tier agents should follow.
    """
    
    def __init__(self, tier_name: str):
        self.tier_name = tier_name
        self.central_brain = get_central_brain()
        
        # Register this tier with the Central Brain
        self.central_brain.register_tier(tier_name, {
            "agent_type": "example",
            "version": "1.0.0",
            "capabilities": ["chat", "memory", "tools"]
        })
        
        print(f"✅ {tier_name} tier connected to Central Brain")
    
    async def process_message(self, user_message: str, session_id: str = "default") -> str:
        """
        Process a user message using the Central Brain.
        
        This is the main pattern all tiers should follow:
        1. Request context from Central Brain
        2. Use the unified system prompt and context
        3. Generate response
        4. Save interaction back to Central Brain
        """
        
        # 1. Get unified context from Central Brain
        context = await self.central_brain.process_request(
            tier_name=self.tier_name,
            user_message=user_message,
            session_id=session_id
        )
        
        # 2. Extract what we need from the context
        system_prompt = context["system_prompt"]
        relevant_memories = context["relevant_memories"]
        available_tools = context["available_tools"]
        user_preferences = context["user_context"]
        
        print(f"\\n🧠 System Prompt Preview (first 200 chars):")
        print(f"   {system_prompt[:200]}...")
        
        print(f"\\n💭 Retrieved {len(relevant_memories)} relevant memories")
        print(f"🔧 Available tools: {len(available_tools)}")
        print(f"👤 User context items: {len(user_preferences)}")
        
        # 3. Generate response (simplified - normally would call LLM here)
        response_parts = [
            f"Hello! I'm the {self.tier_name} tier agent.",
            f"I understand you said: '{user_message}'"
        ]
        
        if relevant_memories:
            response_parts.append(f"I found {len(relevant_memories)} relevant memories from our past conversations.")
        
        if available_tools:
            response_parts.append(f"I have access to {len(available_tools)} tools to help you.")
        
        if user_preferences:
            response_parts.append("I'm considering your personal preferences in my response.")
        
        agent_response = " ".join(response_parts)
        
        # 4. Save the interaction back to Central Brain
        await self.central_brain.save_interaction(
            tier_name=self.tier_name,
            user_message=user_message,
            agent_response=agent_response,
            session_id=session_id,
            metadata={"response_length": len(agent_response)}
        )
        
        return agent_response
    
    async def save_user_preference(self, key: str, value: str):
        """Example of saving user data to shared memory."""
        await self.central_brain.save_user_data(
            key=key,
            value=value,
            category="preferences",
            tier_source=self.tier_name
        )
        print(f"💾 Saved user preference: {key} = {value}")
    
    async def save_successful_solution(self, problem: str, solution: str):
        """Example of saving a solution for reuse across tiers."""
        await self.central_brain.save_solution(
            tier_name=self.tier_name,
            problem_description=problem,
            solution_content=solution,
            solution_type="example",
            success_metrics={"user_satisfaction": "high"}
        )
        print(f"🎯 Saved solution: {problem[:50]}...")


async def main():
    """Demonstrate the Central Nervous System in action."""
    
    print("🚀 Central Nervous System Integration Example")
    print("=" * 50)
    
    # Create example agents for different tiers
    node_agent = ExampleTierAgent("node")
    link_agent = ExampleTierAgent("link")
    mesh_agent = ExampleTierAgent("mesh")
    grid_agent = ExampleTierAgent("grid")
    
    # Simulate some user interactions
    session_id = "demo_session_123"
    
    print("\\n📝 Simulating user interactions...")
    
    # 1. Node tier handles a simple request
    print("\\n--- Node Tier Processing ---")
    response1 = await node_agent.process_message(
        "What's 2 + 2?", 
        session_id
    )
    print(f"Response: {response1}")
    
    # 2. Save some user preferences
    await node_agent.save_user_preference("preferred_language", "Python")
    await node_agent.save_user_preference("communication_style", "concise")
    
    # 3. Link tier handles a more complex request
    print("\\n--- Link Tier Processing ---")
    response2 = await link_agent.process_message(
        "Can you help me write a Python function?", 
        session_id
    )
    print(f"Response: {response2}")
    
    # 4. Save a successful solution
    await link_agent.save_successful_solution(
        "Write a Python function to calculate factorial",
        "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
    )
    
    # 5. Mesh tier processes with more context
    print("\\n--- Mesh Tier Processing ---")
    response3 = await mesh_agent.process_message(
        "I need help with the same kind of function as before", 
        session_id
    )
    print(f"Response: {response3}")
    
    # 6. Grid tier with full context
    print("\\n--- Grid Tier Processing ---")
    response4 = await grid_agent.process_message(
        "Show me my preferences and past solutions", 
        session_id
    )
    print(f"Response: {response4}")
    
    # 7. Show system status
    print("\\n📊 Central Brain System Status:")
    status = await node_agent.central_brain.get_system_status()
    print(f"Connected tiers: {status['central_brain']['connected_tiers']}")
    print(f"Memory items: {status['memory_system'].get('total_items', 'N/A')}")
    
    print("\\n✅ Demo completed!")
    print("\\nKey takeaways:")
    print("- All tiers use the same Central Brain interface")
    print("- Memory, tools, and context are shared across tiers")
    print("- System prompts are unified but tier-customized")
    print("- User preferences persist across all tiers")
    print("- Solutions saved by one tier are available to others")


if __name__ == "__main__":
    asyncio.run(main())
