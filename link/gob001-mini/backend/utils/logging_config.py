# Filename: logging_config.py
# Location: backend/utils/logging_config.py

"""
Centralized logging configuration for the application
Keeps logs organized and structured during development and production
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

class StructuredLogger:
    """Structured logging utility for the application"""
    
    @staticmethod
    def setup_logging(log_level: str = "INFO", log_to_file: bool = True):
        """Setup application logging with proper structure"""
        
        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, log_level.upper()))
        
        # Clear existing handlers
        root_logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        if log_to_file:
            # File handler for general logs
            file_handler = logging.handlers.RotatingFileHandler(
                log_dir / "application.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
            # Separate handler for errors
            error_handler = logging.handlers.RotatingFileHandler(
                log_dir / "errors.log",
                maxBytes=5*1024*1024,  # 5MB
                backupCount=3
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            root_logger.addHandler(error_handler)
        
        return root_logger
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get a logger instance for a specific module"""
        return logging.getLogger(name)
    
    @staticmethod
    def log_api_call(logger: logging.Logger, endpoint: str, method: str, 
                    status_code: int, response_time: float):
        """Log API call information in structured format"""
        logger.info(
            f"API_CALL - {method} {endpoint} - "
            f"Status: {status_code} - "
            f"Time: {response_time:.3f}s"
        )
    
    @staticmethod
    def log_model_usage(logger: logging.Logger, model: str, provider: str,
                       tokens_used: int, cost: float = None):
        """Log model usage for cost tracking"""
        cost_info = f" - Cost: ${cost:.4f}" if cost else ""
        logger.info(
            f"MODEL_USAGE - {provider}/{model} - "
            f"Tokens: {tokens_used}{cost_info}"
        )
    
    @staticmethod
    def log_agent_routing(logger: logging.Logger, message: str, agent: str,
                         confidence: float):
        """Log agent routing decisions"""
        logger.debug(
            f"AGENT_ROUTING - Message: '{message[:50]}...' - "
            f"Agent: {agent} - Confidence: {confidence:.3f}"
        )

# Global logger instance
app_logger = StructuredLogger.get_logger("gob-001-mini")
