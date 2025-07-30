"""
Simple logging utility.
"""
import logging
from . import config

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with file and stream handlers.

    Args:
        name: Logger name.

    Returns:
        Configured logger.

    >>> logger = setup_logger("test_logger")
    >>> logger.info("test")  # Should log to file and stdout
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        fh = logging.FileHandler(config.LOG_FILE)
        sh = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger