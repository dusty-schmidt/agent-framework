#!/usr/bin/env python3
"""
Agentic Framework - Backend API Server

Provides HTTP API endpoints for the web interface to communicate with the agents.
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from datetime import datetime
import traceback
import time

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from scripts.simple_env import setup_simple_env

# Setup environment
setup_simple_env()

# Setup logging
from core.config.logging_config import AgenticLogger, api_logger
AgenticLogger.setup_logging()

from core.brain.central_brain import CentralBrain
from scripts.config_loader import get_model_config, get_openrouter_headers, create_model_request_payload

try:
    import aiohttp
    from aiohttp import web, web_request
    from aiohttp.web import middleware
except ImportError:
    print("Installing aiohttp...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "aiohttp"])
    import aiohttp
    from aiohttp import web, web_request
    from aiohttp.web import middleware

class AgenticAPI:
    """Backend API for the Agentic Framework."""

    def __init__(self):
        self.logger = api_logger
        self.central_brain = CentralBrain()
        self.current_tier = "node"
        self.conversation_history = {}
        self.system_logs = []
        self.message_count = 0
        self.start_time = datetime.now()

        self.logger.info("Initializing Agentic API server")
        self.initialize_agents()

    def initialize_agents(self):
        """Initialize all tier agents."""
        tiers = ["node", "link", "mesh", "grid"]
        for tier in tiers:
            try:
                config = get_model_config(tier)
                self.central_brain.register_tier(tier, {
                    "agent_type": f"{tier}_agent",
                    "version": "1.0.0",
                    "capabilities": ["chat", "memory"],
                    "model_config": config
                })
                self.add_log("info", f"{tier} agent initialized")
                AgenticLogger.log_tier_operation(self.logger, tier, "initialize", "success")
            except Exception as e:
                self.add_log("error", f"Failed to initialize {tier} agent: {str(e)}")
                AgenticLogger.log_error(self.logger, e, f"Initializing {tier} agent")

        self.add_log("info", "All agents initialized successfully")
        self.logger.info("Agent initialization complete")

    def add_log(self, level, message):
        """Add a log entry to both in-memory and file logs."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self.system_logs.append(log_entry)

        # Also log to file system
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(f"API_LOG - {message}")

        # Keep only last 100 logs in memory
        if len(self.system_logs) > 100:
            self.system_logs = self.system_logs[-100:]

    async def _demo_response(self, message: str, conversation_id: str, start_time: float):
        """Generate a demo response when API key is not configured."""
        import random

        # Demo responses by tier
        demo_responses = {
            "node": [
                f"Hello! I'm the NODE tier agent. You said: '{message}'. This is a demo response since no API key is configured.",
                f"NODE tier responding to: '{message}'. To get real AI responses, please configure your OpenRouter API key.",
                f"Demo mode active. NODE tier received: '{message}'. Set up your API key to enable real AI responses."
            ],
            "link": [
                f"Greetings! I'm the LINK tier agent. I received your message: '{message}'. This is a demonstration response because the OpenRouter API key isn't configured yet.",
                f"LINK tier demo response for: '{message}'. To unlock full AI capabilities, please set up your OpenRouter API key following the setup instructions.",
                f"Hello from LINK tier! Your message '{message}' was received. This is a demo - configure your API key for real AI responses."
            ],
            "mesh": [
                f"MESH tier agent here. Processing your input: '{message}'. Currently in demo mode - please configure your OpenRouter API key for full functionality.",
                f"Systematic response from MESH tier regarding: '{message}'. This is a demonstration. Set up your API key to enable real AI processing.",
                f"MESH tier coordination active. Message received: '{message}'. Demo mode - configure OpenRouter API key for actual AI responses."
            ],
            "grid": [
                f"GRID tier analytical response: Your message '{message}' has been processed in demo mode. Configure your OpenRouter API key to access real AI insights.",
                f"Deep analysis from GRID tier: '{message}' - This is a demonstration response. Set up your API key for genuine AI-powered analysis.",
                f"GRID tier processing complete for: '{message}'. Demo mode active - please configure your OpenRouter API key for full AI capabilities."
            ]
        }

        # Get conversation history
        if conversation_id not in self.conversation_history:
            self.conversation_history[conversation_id] = []

        history = self.conversation_history[conversation_id]

        # Select a random demo response
        response_text = random.choice(demo_responses[self.current_tier])

        # Update conversation history
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response_text})

        # Keep history manageable
        if len(history) > 20:
            history = history[-20:]

        self.conversation_history[conversation_id] = history
        self.message_count += 1

        response_time = time.time() - start_time

        self.add_log("info", f"Demo response generated by {self.current_tier} tier")
        AgenticLogger.log_tier_operation(self.logger, self.current_tier, "send_message", "demo", f"Response length: {len(response_text)}")

        return {
            "success": True,
            "response": response_text,
            "tier": self.current_tier,
            "message_count": self.message_count,
            "demo_mode": True
        }
    
    async def send_message_to_agent(self, message: str, conversation_id: str = "default"):
        """Send message to current tier agent."""
        start_time = time.time()

        try:
            if self.current_tier not in self.central_brain.connected_tiers:
                raise Exception(f"{self.current_tier} agent not available")

            # Check if we're in demo mode (API key not properly configured)
            try:
                from scripts.config_loader import load_config
                config = load_config()
                api_key = config.get('api', {}).get('api_key')

                # Fallback to environment if not in config
                if not api_key or api_key == "PUT_YOUR_OPENROUTER_API_KEY_HERE":
                    api_key = os.getenv('OPENROUTER_API_KEY')

                if not api_key or api_key == "your_key_here" or api_key == "PUT_YOUR_OPENROUTER_API_KEY_HERE":
                    return await self._demo_response(message, conversation_id, start_time)
            except Exception:
                # If config loading fails, fall back to environment check
                api_key = os.getenv('OPENROUTER_API_KEY')
                if not api_key or api_key == "your_key_here":
                    return await self._demo_response(message, conversation_id, start_time)

            # Get tier config
            tier_info = self.central_brain.connected_tiers[self.current_tier]
            config = tier_info['config']['model_config']

            # Build messages with system prompt
            system_prompts = {
                "node": "You are a Node tier agent. Be direct and concise. Provide helpful, straightforward responses.",
                "link": "You are a Link tier agent. Be versatile and helpful. Provide comprehensive, well-structured responses.",
                "mesh": "You are a Mesh tier agent. Focus on coordination and organization. Provide systematic, organized responses.",
                "grid": "You are a Grid tier agent. Provide analytical, thoughtful responses with deep insights."
            }

            # Get conversation history
            if conversation_id not in self.conversation_history:
                self.conversation_history[conversation_id] = []

            history = self.conversation_history[conversation_id]

            # Build message array
            messages = [{"role": "system", "content": system_prompts[self.current_tier]}]

            # Add recent conversation context (last 6 messages)
            if len(history) > 0:
                recent = history[-6:]
                messages.extend(recent)

            # Add current message
            messages.append({"role": "user", "content": message})

            payload = create_model_request_payload(messages, self.current_tier)
            headers = get_openrouter_headers()

            self.add_log("info", f"Sending message to {self.current_tier} tier")
            AgenticLogger.log_tier_operation(self.logger, self.current_tier, "send_message", "started", f"Message: {message[:50]}...")

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    config["base_url"] + "/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:

                    response_time = time.time() - start_time
                    AgenticLogger.log_api_call(self.logger, "/chat/completions", "POST", response.status, response_time)

                    if response.status == 200:
                        data = await response.json()
                        if 'choices' in data and len(data['choices']) > 0:
                            response_text = data['choices'][0]['message']['content']

                            # Update conversation history
                            history.append({"role": "user", "content": message})
                            history.append({"role": "assistant", "content": response_text})

                            # Keep history manageable
                            if len(history) > 20:
                                history = history[-20:]

                            self.conversation_history[conversation_id] = history
                            self.message_count += 1

                            self.add_log("info", f"Response generated by {self.current_tier} tier")
                            AgenticLogger.log_tier_operation(self.logger, self.current_tier, "send_message", "success", f"Response length: {len(response_text)}")

                            return {
                                "success": True,
                                "response": response_text,
                                "tier": self.current_tier,
                                "message_count": self.message_count
                            }
                        else:
                            raise Exception("No response from agent - empty choices array")
                    else:
                        response_text = await response.text()
                        raise Exception(f"API returned {response.status}: {response_text}")

        except Exception as e:
            response_time = time.time() - start_time
            self.add_log("error", f"Error in {self.current_tier} tier: {str(e)}")
            AgenticLogger.log_error(self.logger, e, f"Sending message to {self.current_tier} tier")
            AgenticLogger.log_tier_operation(self.logger, self.current_tier, "send_message", "failed", str(e))

            return {
                "success": False,
                "error": str(e),
                "tier": self.current_tier
            }

    async def setup_api_key(self, api_key: str):
        """Setup and validate API key."""
        try:
            if not api_key or not api_key.strip():
                return {"success": False, "error": "API key is required"}

            api_key = api_key.strip()

            if not api_key.startswith('sk-or-'):
                return {"success": False, "error": "Invalid API key format. Should start with 'sk-or-'"}

            # Test the API key with OpenRouter
            test_headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(
                        "https://openrouter.ai/api/v1/models",
                        headers=test_headers,
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:

                        if response.status == 200:
                            # API key is valid, store it
                            os.environ['OPENROUTER_API_KEY'] = api_key

                            self.add_log("info", "API key validated and configured successfully")
                            self.logger.info(f"API key configured successfully (length: {len(api_key)})")

                            return {
                                "success": True,
                                "message": "API key validated and configured successfully"
                            }
                        elif response.status == 401:
                            return {
                                "success": False,
                                "error": "Invalid API key - authentication failed"
                            }
                        else:
                            return {
                                "success": False,
                                "error": f"API validation failed with status {response.status}"
                            }

                except asyncio.TimeoutError:
                    return {
                        "success": False,
                        "error": "Timeout while validating API key"
                    }
                except Exception as e:
                    return {
                        "success": False,
                        "error": f"Network error: {str(e)}"
                    }

        except Exception as e:
            self.logger.error(f"API key setup error: {str(e)}")
            return {
                "success": False,
                "error": f"Setup failed: {str(e)}"
            }

# Global API instance
api = AgenticAPI()

@middleware
async def cors_handler(request, handler):
    """Handle CORS for web interface."""
    response = await handler(request)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

async def handle_chat(request):
    """Handle chat messages."""
    try:
        data = await request.json()
        message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', 'default')
        
        if not message:
            return web.json_response({
                "success": False,
                "error": "Empty message"
            }, status=400)
        
        result = await api.send_message_to_agent(message, conversation_id)
        return web.json_response(result)
        
    except Exception as e:
        api.add_log("error", f"Chat handler error: {str(e)}")
        return web.json_response({
            "success": False,
            "error": str(e)
        }, status=500)

async def handle_switch_tier(request):
    """Handle tier switching."""
    try:
        data = await request.json()
        new_tier = data.get('tier', '').lower()
        
        if new_tier not in api.central_brain.connected_tiers:
            return web.json_response({
                "success": False,
                "error": f"Unknown tier: {new_tier}"
            }, status=400)
        
        api.current_tier = new_tier
        api.add_log("info", f"Switched to {new_tier} tier")
        
        return web.json_response({
            "success": True,
            "tier": new_tier,
            "message": f"Switched to {new_tier.upper()} tier"
        })
        
    except Exception as e:
        api.add_log("error", f"Tier switch error: {str(e)}")
        return web.json_response({
            "success": False,
            "error": str(e)
        }, status=500)

async def handle_status(request):
    """Handle status requests."""
    try:
        uptime = (datetime.now() - api.start_time).total_seconds()
        
        return web.json_response({
            "success": True,
            "status": {
                "current_tier": api.current_tier,
                "message_count": api.message_count,
                "uptime": int(uptime),
                "available_tiers": list(api.central_brain.connected_tiers.keys()),
                "api_status": "ready"
            }
        })
        
    except Exception as e:
        return web.json_response({
            "success": False,
            "error": str(e)
        }, status=500)

async def handle_logs(request):
    """Handle log requests."""
    try:
        limit = int(request.query.get('limit', 50))
        logs = api.system_logs[-limit:] if limit > 0 else api.system_logs
        
        return web.json_response({
            "success": True,
            "logs": logs
        })
        
    except Exception as e:
        return web.json_response({
            "success": False,
            "error": str(e)
        }, status=500)

async def handle_clear_chat(request):
    """Handle clear chat requests."""
    try:
        data = await request.json()
        conversation_id = data.get('conversation_id', 'default')
        
        if conversation_id in api.conversation_history:
            del api.conversation_history[conversation_id]
        
        api.add_log("info", f"Chat history cleared for {conversation_id}")
        
        return web.json_response({
            "success": True,
            "message": "Chat history cleared"
        })
        
    except Exception as e:
        return web.json_response({
            "success": False,
            "error": str(e)
        }, status=500)

async def handle_setup_key(request):
    """Handle API key setup request."""
    try:
        data = await request.json()
        api_key = data.get('api_key', '').strip()

        # Get the global API instance
        global api
        result = await api.setup_api_key(api_key)

        if result["success"]:
            return web.json_response(result)
        else:
            return web.json_response(result, status=400)

    except Exception as e:
        return web.json_response({
            "success": False,
            "error": f"Setup failed: {str(e)}"
        }, status=500)

def create_app():
    """Create the web application."""
    app = web.Application(middlewares=[cors_handler])
    
    # API routes
    app.router.add_post('/api/chat', handle_chat)
    app.router.add_post('/api/switch_tier', handle_switch_tier)
    app.router.add_get('/api/status', handle_status)
    app.router.add_get('/api/logs', handle_logs)
    app.router.add_post('/api/clear_chat', handle_clear_chat)
    app.router.add_post('/api/setup_key', handle_setup_key)
    
    # Handle OPTIONS requests for CORS
    app.router.add_options('/api/{path:.*}', lambda r: web.Response())
    
    return app

async def main():
    """Main entry point."""
    app = create_app()
    
    print(">> AGENTIC FRAMEWORK - BACKEND API SERVER")
    print("=" * 50)
    print(">> API server starting...")
    print(">> Available endpoints:")
    print("   POST /api/chat - Send messages to agents")
    print("   POST /api/switch_tier - Switch agent tiers")
    print("   GET  /api/status - Get system status")
    print("   GET  /api/logs - Get system logs")
    print("   POST /api/clear_chat - Clear chat history")
    print(">> Server ready on http://localhost:8081")
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8081)
    await site.start()
    
    try:
        await asyncio.Future()  # Run forever
    except KeyboardInterrupt:
        print("\n>> API server stopped")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n>> Goodbye!")
        sys.exit(0)
