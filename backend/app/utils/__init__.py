"""Utility functions"""
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_logger(name: str):
    """Get logger instance"""
    return logging.getLogger(name)
