import aiohttp
import logging
from typing import List, Dict, Protocol
from dataclasses import dataclass
from loaders.prompt_builder import build_prompt

# Configure logging for chatbot operations
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('GeminiChatbot')

class ChatProvider(Protocol):
    async def chat(self, message: str, context: List[Dict] = None) -> str: ...

@dataclass
class ChatConfig:
    api_key: str
    model: str = "gemini-1.5-flash"
    max_history: int = 10
    max_tokens: int = 1000
    system_prompt: str = ""
    user_prompt_prefix: str = ""

class GeminiProvider:
    def __init__(self, api_key, model="gemini-1.5-flash", system_prompt="", user_prompt_prefix=""):
        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.user_prompt_prefix = user_prompt_prefix
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    async def chat(self, message: str, context: List[Dict] = None) -> str:
        full_prompt = build_prompt(
            message, context, self.system_prompt, self.user_prompt_prefix
        )
        headers = { "Content-Type": "application/json" }
        payload = {
            "contents": [ { "parts": [ { "text": full_prompt } ] } ],
            "generationConfig": { "maxOutputTokens": 1000, "temperature": 0.7 }
        }
        url = f"{self.base_url}?key={self.api_key}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._extract_response(data)
                    else:
                        error_text = await response.text()
                        return f"Error: {response.status} - {error_text}"
        except Exception as e:
            return f"Connection error: {str(e)}"

    def _extract_response(self, data: dict) -> str:
        try:
            candidates = data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "No response generated")
            return "No response generated"
        except Exception as e:
            return f"Error parsing response: {str(e)}"

class SimpleChatbot:
    def __init__(
        self,
        config: ChatConfig,
        provider: ChatProvider,
        memory = None,
        tools = None
    ):
        self.config = config
        self.provider = provider
        self.memory = memory
        self.tools = tools
        self.history = self.memory.load() if self.memory else []

    async def chat(self, user_input: str) -> str:
        logger.info(f"Received user input: '{user_input[:100]}...'")
        print(f"User: {user_input}")
        
        # Handle tool commands
        if self.tools and user_input.startswith("/"):
            logger.info("Processing tool command")
            try:
                cmd, arg = user_input[1:].split(" ", 1)
                logger.info(f"Executing tool: {cmd} with arg: {arg}")
                result = self.tools.run(cmd, arg)
                print(f"Bot: {result}")
                logger.info(f"Tool result: {result[:100]}...")
                return result
            except Exception as e:
                logger.error(f"Tool command failed: {e}")
                print("Bot: Invalid tool command.")
                return "Invalid tool command."
        
        # Add user message to history
        logger.info(f"Adding user message to history. Current history length: {len(self.history)}")
        self.history.append({"role": "user", "content": user_input})
        
        # Get recent history for context
        recent_history = self.history[-self.config.max_history:]
        logger.info(f"Using {len(recent_history)} messages for context")
        
        # Check if memory has semantic search capability
        if hasattr(self.memory, 'semantic_search'):
            logger.info("Memory supports semantic search, retrieving relevant context")
            relevant_memories = self.memory.semantic_search(user_input, top_k=3)
            logger.info(f"Found {len(relevant_memories)} relevant memories")
            if relevant_memories:
                # Add relevant memories to context
                for i, memory in enumerate(relevant_memories):
                    logger.debug(f"Relevant memory {i+1}: '{memory[:100]}...'")
        
        # Get response from provider
        logger.info("Requesting response from Gemini API")
        response = await self.provider.chat(user_input, recent_history)
        logger.info(f"Received response: '{response[:100]}...'")
        
        # Add assistant response to history
        self.history.append({"role": "assistant", "content": response})
        logger.info(f"Added assistant response to history. New history length: {len(self.history)}")
        
        # Save to memory
        if self.memory:
            logger.info("Saving conversation to memory")
            self.memory.save(self.history)
            logger.info("Memory save completed")
        
        print(f"Bot: {response}")
        return response

    def get_history(self) -> List[Dict]:
        return self.history.copy()

    def clear_history(self) -> None:
        self.history.clear()
        if self.memory:
            self.memory.save(self.history)
        print("Conversation history cleared!")

async def interactive_chat(chatbot: SimpleChatbot):
    print("🤖 Chatbot with Google Gemini! Now with memory & tools.")
    print("Type 'quit' to exit, 'clear' to clear history, 'history' to see conversation")
    print("Type 'search <query>' to test semantic memory search")
    print("Prefix with '/' to use a tool, e.g. /echo hello or /calc 5*4")
    print("-" * 50)
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == 'quit':
                print("Goodbye! 👋")
                break
            elif user_input.lower() == 'clear':
                chatbot.clear_history()
                continue
            elif user_input.lower() == 'history':
                history = chatbot.get_history()
                print(f"\n📚 Conversation History ({len(history)} messages):")
                for i, msg in enumerate(history):
                    role = "You" if msg["role"] == "user" else "Bot"
                    content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                    print(f"  {i+1}. {role}: {content}")
                continue
            elif user_input.lower().startswith('search '):
                query = user_input[7:].strip()  # Remove 'search ' prefix
                if hasattr(chatbot.memory, 'semantic_search'):
                    print(f"\n🔍 Searching for: '{query}'")
                    results = chatbot.memory.semantic_search(query, top_k=5)
                    if results:
                        print(f"Found {len(results)} relevant memories:")
                        for i, result in enumerate(results):
                            print(f"  {i+1}. {result[:150]}...")
                    else:
                        print("No relevant memories found.")
                else:
                    print("Semantic search not available with current memory system.")
                continue
            elif not user_input:
                print("Please enter a message!")
                continue
            await chatbot.chat(user_input)
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")
