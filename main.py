#!/usr/bin/env python3
"""
Agentic Framework - Main Entry Point

Primary startup script for the Agentic Framework.
Launches the web-based chatbot interface with optional test mode.
"""

import argparse
import asyncio
import sys
import webbrowser
import time
from pathlib import Path
from threading import Thread
import subprocess

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from scripts.simple_env import setup_simple_env

# Setup logging
from core.config.logging_config import AgenticLogger, main_logger
AgenticLogger.setup_logging()

def launch_web_server(test_mode=False):
    """Launch both the web server and API server."""
    try:
        import http.server
        import socketserver
        import os
        import threading
        import subprocess

        # Start the backend API server in a separate process
        print(">> Starting backend API server...")
        api_process = subprocess.Popen([
            sys.executable, "backend_api.py"
        ], cwd=Path(__file__).parent)

        # Give API server time to start
        time.sleep(2)

        # Change to frontend directory
        os.chdir(Path(__file__).parent / "frontend")

        PORT = 8080

        # Custom handler to redirect to setup page if no API key
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    # Check if API key is configured
                    api_key = os.getenv('OPENROUTER_API_KEY')
                    if not api_key or api_key == "your_key_here":
                        # Redirect to setup page if no valid API key
                        self.send_response(302)
                        self.send_header('Location', '/setup/api_key_setup.html')
                        self.end_headers()
                        return
                    elif test_mode:
                        self.send_response(302)
                        self.send_header('Location', '/chatbots/chatbot_test.html')
                        self.end_headers()
                        return
                    else:
                        self.send_response(302)
                        self.send_header('Location', '/chatbots/chatbot_ui.html')
                        self.end_headers()
                        return

                super().do_GET()

        Handler = CustomHandler

        print(f">> Web server running at http://localhost:{PORT}")
        print(f">> API server running at http://localhost:8081")

        if test_mode:
            print(f">> Test mode enabled - enhanced interface with logs")
            # Open test version
            webbrowser.open(f"http://localhost:{PORT}/chatbots/chatbot_test.html")
        else:
            print(f">> Standard interface")
            # Open standard version
            webbrowser.open(f"http://localhost:{PORT}/chatbots/chatbot_ui.html")

        print(f">> Press Ctrl+C to stop both servers")

        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n>> Stopping servers...")
                api_process.terminate()
                api_process.wait()
                print(f">> Servers stopped")

    except KeyboardInterrupt:
        print(f"\n>> Servers stopped")
    except Exception as e:
        print(f">> Error starting servers: {e}")
        sys.exit(1)

def launch_terminal_interface():
    """Launch the terminal chat interface."""
    try:
        # Import and run terminal chat
        from frontend.terminal_chat import main as terminal_main
        asyncio.run(terminal_main())
    except Exception as e:
        print(f">> Error launching terminal interface: {e}")
        sys.exit(1)

def check_dependencies():
    """Check if all dependencies are available."""
    try:
        setup_simple_env()
        print(">> Environment setup complete")
        return True
    except Exception as e:
        print(f">> Environment setup failed: {e}")
        print(f">> Run: python scripts/setup_project.py")
        return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Agentic Framework - Multi-tier AI Agent System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Launch web interface
  python main.py --test            # Launch web interface with test panels
  python main.py --terminal        # Launch terminal interface
  python main.py --validate       # Validate configuration only
        """
    )
    
    parser.add_argument(
        "--test", 
        action="store_true",
        help="Launch web interface with live logs and status panels"
    )
    
    parser.add_argument(
        "--terminal", 
        action="store_true",
        help="Launch terminal chat interface instead of web interface"
    )
    
    parser.add_argument(
        "--validate", 
        action="store_true",
        help="Validate configuration and exit"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=8080,
        help="Port for web server (default: 8080)"
    )
    
    args = parser.parse_args()
    
    print("AGENTIC FRAMEWORK - MULTI-TIER AI AGENT SYSTEM")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Validate only mode
    if args.validate:
        print(">> Running validation...")
        try:
            result = subprocess.run([
                sys.executable, "scripts/validate_config.py"
            ], capture_output=True, text=True)
            
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
            
            sys.exit(result.returncode)
        except Exception as e:
            print(f">> Validation failed: {e}")
            sys.exit(1)
    
    # Terminal interface mode
    if args.terminal:
        print(">> Launching terminal chat interface...")
        launch_terminal_interface()
        return
    
    # Web interface mode (default)
    print(">> Launching web-based chatbot interface...")
    launch_web_server(test_mode=args.test)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n>> Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f">> Fatal error: {e}")
        sys.exit(1)
