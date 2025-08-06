#!/usr/bin/env python3
"""
Centralized logging configuration for the Agentic Framework.
Provides structured logging with file rotation and proper error tracking.
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path
import sys

class AgenticLogger:
    """Centralized logging utility for the Agentic Framework."""
    
    _initialized = False
    _loggers = {}
    
    @classmethod
    def setup_logging(cls, log_level: str = "INFO", log_to_file: bool = True):
        """Setup application logging with proper structure."""
        
        if cls._initialized:
            return
            
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
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        if log_to_file:
            # Main application log
            app_handler = logging.handlers.RotatingFileHandler(
                log_dir / "application.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            app_handler.setLevel(logging.INFO)
            app_handler.setFormatter(formatter)
            root_logger.addHandler(app_handler)
            
            # Error log
            error_handler = logging.handlers.RotatingFileHandler(
                log_dir / "errors.log",
                maxBytes=5*1024*1024,  # 5MB
                backupCount=3
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            root_logger.addHandler(error_handler)
            
            # System log
            system_handler = logging.handlers.RotatingFileHandler(
                log_dir / "system.log",
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            system_handler.setLevel(logging.INFO)
            system_handler.setFormatter(formatter)
            root_logger.addHandler(system_handler)
        
        cls._initialized = True
        logging.info("Agentic Framework logging system initialized")
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get a logger instance for a specific module."""
        if not cls._initialized:
            cls.setup_logging()
        
        if name not in cls._loggers:
            cls._loggers[name] = logging.getLogger(name)
        
        return cls._loggers[name]
    
    @classmethod
    def log_api_call(cls, logger: logging.Logger, endpoint: str, method: str, 
                    status_code: int, response_time: float = None):
        """Log API call information in structured format."""
        time_info = f" - Time: {response_time:.3f}s" if response_time else ""
        logger.info(
            f"API_CALL - {method} {endpoint} - "
            f"Status: {status_code}{time_info}"
        )
    
    @classmethod
    def log_tier_operation(cls, logger: logging.Logger, tier: str, operation: str, 
                          status: str, details: str = None):
        """Log tier-specific operations."""
        detail_info = f" - {details}" if details else ""
        logger.info(
            f"TIER_OP - {tier.upper()} - {operation} - "
            f"Status: {status}{detail_info}"
        )
    
    @classmethod
    def log_error(cls, logger: logging.Logger, error: Exception, context: str = None):
        """Log errors with context."""
        context_info = f" - Context: {context}" if context else ""
        logger.error(
            f"ERROR - {type(error).__name__}: {str(error)}{context_info}",
            exc_info=True
        )
    
    @classmethod
    def create_session_log(cls, session_id: str):
        """Create a session-specific log file."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        session_logger = logging.getLogger(f"session.{session_id}")
        
        # Session-specific file handler
        session_handler = logging.handlers.RotatingFileHandler(
            log_dir / f"session_{session_id}.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=2
        )
        session_handler.setLevel(logging.INFO)
        session_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        session_logger.addHandler(session_handler)
        
        return session_logger

# Global logger instances
main_logger = AgenticLogger.get_logger("agentic.main")
api_logger = AgenticLogger.get_logger("agentic.api")
brain_logger = AgenticLogger.get_logger("agentic.brain")
