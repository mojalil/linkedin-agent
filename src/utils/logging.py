import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logging(
    log_file: Optional[str] = "linkedin_agent.log",
    level: int = logging.INFO
) -> logging.Logger:
    """Set up logging configuration.
    
    Args:
        log_file: Path to log file. If None, logs only to console.
        level: Logging level.
    
    Returns:
        Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger("linkedin_agent")
    logger.setLevel(level)
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if log_file is specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create default logger instance
logger = setup_logging() 