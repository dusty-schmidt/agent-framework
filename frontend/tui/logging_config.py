#!/usr/bin/env python3
"""
Centralized Logging Configuration for Agentic System
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path


class AgenticSystemLogger:
    """Centralized logger for the agentic system"""
    
    def __init__(self, logs_dir: str = "logs"):
        # Ensure logs directory is relative to agentic system root
        root_dir = Path(__file__).parent.parent.parent
        self.logs_dir = root_dir / logs_dir
        self.logs_dir.mkdir(exist_ok=True)
        
        # Create log files for different components
        self.log_files = {
            'tui': self.logs_dir / 'tui.log',
            'node': self.logs_dir / 'node_tier.log',
            'link': self.logs_dir / 'link_tier.log', 
            'mesh': self.logs_dir / 'mesh_tier.log',
            'grid': self.logs_dir / 'grid_tier.log',
            'system': self.logs_dir / 'system.log'
        }
        
        # Setup loggers
        self.loggers = {}
        self._setup_loggers()
    
    def _setup_loggers(self):
        """Setup individual loggers for each component"""
        
        # Common formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        for component, log_file in self.log_files.items():
            logger = logging.getLogger(f'agentic.{component}')
            logger.setLevel(logging.INFO)
            
            # Remove existing handlers to avoid duplicates
            logger.handlers.clear()
            
            # File handler with rotation
            file_handler = logging.handlers.RotatingFileHandler(
                log_file, 
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            # Console handler for TUI logger only
            if component == 'tui':
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)
            
            self.loggers[component] = logger
    
    def get_logger(self, component: str) -> logging.Logger:
        """Get logger for a specific component"""
        return self.loggers.get(component, self.loggers['system'])
    
    def log_tier_start(self, tier_name: str, command: str, cwd: str):
        """Log tier startup"""
        logger = self.get_logger(tier_name)
        logger.info(f"Starting {tier_name} tier")
        logger.info(f"Command: {command}")
        logger.info(f"Working directory: {cwd}")
    
    def log_tier_stop(self, tier_name: str):
        """Log tier shutdown"""
        logger = self.get_logger(tier_name)
        logger.info(f"Stopping {tier_name} tier")
    
    def log_tier_output(self, tier_name: str, output: str):
        """Log tier output"""
        logger = self.get_logger(tier_name)
        logger.info(f"Output: {output}")
    
    def log_tier_error(self, tier_name: str, error: str):
        """Log tier error"""
        logger = self.get_logger(tier_name)
        logger.error(f"Error: {error}")
    
    def get_recent_logs(self, component: str, lines: int = 50) -> list:
        """Get recent log lines for a component"""
        log_file = self.log_files.get(component)
        if not log_file or not log_file.exists():
            return []
        
        try:
            with open(log_file, 'r') as f:
                return f.readlines()[-lines:]
        except Exception:
            return []
    
    def create_session_log(self) -> str:
        """Create a session-specific log file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_log = self.logs_dir / f"session_{timestamp}.log"
        
        # Log session start
        system_logger = self.get_logger('system')
        system_logger.info(f"New TUI session started: {session_log}")
        
        return str(session_log)


# Global logger instance
_logger_instance = None

def get_agentic_logger() -> AgenticSystemLogger:
    """Get the global logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = AgenticSystemLogger()
    return _logger_instance


def setup_logging():
    """Setup logging for the agentic system"""
    return get_agentic_logger()


if __name__ == "__main__":
    # Test the logging system
    logger_system = setup_logging()
    
    tui_logger = logger_system.get_logger('tui')
    tui_logger.info("Logging system test - TUI component")
    
    node_logger = logger_system.get_logger('node')
    node_logger.info("Logging system test - Node tier")
    
    print("Logging system test completed. Check logs/ directory.")
