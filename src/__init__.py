import logging
import sys
from pathlib import Path

# Configure logging
def setup_logging():
    """Configure logging for the application."""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(Path("linkedin_agent.log"))
        ]
    )

# Create logger
logger = logging.getLogger("linkedin_agent")

# Initialize logging when package is imported
setup_logging()
