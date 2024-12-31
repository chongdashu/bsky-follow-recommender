"""Logging configuration and setup utilities."""

import logging


def setup_logger(name: str) -> logging.Logger:
    """Set up a logger with the specified name.

    Args:
        name: The name for the logger

    Returns:
        A configured logger instance
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
