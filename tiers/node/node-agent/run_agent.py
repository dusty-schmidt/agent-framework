# File: run_agent.py
# Main entry point for Gemini chatbot with config file support

import asyncio
import logging
from agents.simple_gemini_bot import SimpleChatbot, ChatConfig, GeminiProvider, interactive_chat
from loaders.tool_loader import tools
from loaders.config_loader import load_config
from tools.embed_memory import VectorMemory, JSONFileMemory

# Configure main application logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('MainApp')

def main():
    logger.info("Starting Gemini Chatbot application")
    
    # Load config
    logger.info("Loading configuration")
    config_dict = load_config("config/config.json")
    api_key = config_dict["api_key"]
    model = config_dict.get("model", "gemini-1.5-flash")
    system_prompt = config_dict.get("system_prompt", "You are a helpful, concise AI assistant.")
    user_prompt_prefix = config_dict.get("user_prompt_prefix", "")
    
    logger.info(f"Configuration loaded - Model: {model}")

    # Set up memory system
    logger.info("Initializing memory system")
    # Use VectorMemory for semantic search capabilities
    memory = VectorMemory(
        embedding_model="all-MiniLM-L6-v2",
        persist_path="memory/vector_memory.json"
    )
    # Also keep JSON backup
    json_memory = JSONFileMemory("memory/chat_history.json")
    
    # Load existing JSON history into vector memory if it exists and vector memory is empty
    if len(memory.texts) == 0:
        logger.info("Vector memory is empty, checking for existing JSON history")
        existing_history = json_memory.load()
        if existing_history:
            logger.info(f"Found existing JSON history with {len(existing_history)} messages, migrating to vector memory")
            memory.save(existing_history)

    # Set up Gemini provider and chatbot
    logger.info("Initializing Gemini provider and chatbot")
    provider = GeminiProvider(
        api_key,
        model=model,
        system_prompt=system_prompt,
        user_prompt_prefix=user_prompt_prefix
    )
    chat_config = ChatConfig(api_key=api_key, model=model)
    chatbot = SimpleChatbot(
        chat_config,
        provider,
        memory=memory,
        tools=tools
    )
    
    logger.info("Chatbot initialization complete")

    print(f"\n🤖 Gemini Chatbot (Model: {model})")
    print(f"System prompt: {system_prompt}\n")
    asyncio.run(interactive_chat(chatbot))

if __name__ == "__main__":
    main()
