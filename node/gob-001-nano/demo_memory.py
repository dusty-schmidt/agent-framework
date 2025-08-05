#!/usr/bin/env python3
"""Demo script to show memory system with simulated conversation"""

import asyncio
import logging
from agents.simple_gemini_bot import SimpleChatbot, ChatConfig, GeminiProvider
from loaders.tool_loader import tools
from loaders.config_loader import load_config
from tools.embed_memory import VectorMemory

# Set up logging to show what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def demo_conversation():
    print("🚀 Memory System Demo")
    print("=" * 50)
    
    # Load config
    config_dict = load_config("config/config.json")
    
    # Set up components
    provider = GeminiProvider(
        config_dict["api_key"],
        model=config_dict.get("model", "gemini-1.5-flash"),
        system_prompt=config_dict.get("system_prompt", "You are a helpful AI assistant."),
        user_prompt_prefix=config_dict.get("user_prompt_prefix", "")
    )
    
    memory = VectorMemory(
        embedding_model="all-MiniLM-L6-v2",
        persist_path="memory/vector_memory.json"
    )
    
    chat_config = ChatConfig(api_key=config_dict["api_key"])
    chatbot = SimpleChatbot(chat_config, provider, memory=memory, tools=tools)
    
    print(f"📚 Loaded memory with {len(memory.texts)} existing conversations")
    
    # Demo queries
    demo_queries = [
        "Tell me about Python programming",
        "What do you know about whales?",
    ]
    
    for query in demo_queries:
        print(f"\n🔥 Demo Query: '{query}'")
        print("-" * 30)
        
        # Show semantic search in action
        print("🔍 Searching relevant memories...")
        relevant = memory.semantic_search(query, top_k=3)
        if relevant:
            print(f"Found {len(relevant)} relevant memories:")
            for i, mem in enumerate(relevant, 1):
                print(f"  {i}. {mem[:80]}...")
        
        # Get AI response
        print("\n🤖 Getting AI response...")
        response = await chatbot.chat(query)
        print()

if __name__ == "__main__":
    asyncio.run(demo_conversation())
