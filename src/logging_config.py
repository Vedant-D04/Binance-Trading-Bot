import logging
import os

def setup_logging():
    """Sets up logging to bot.log and console."""
    log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'bot.log')
    
    # Create logger
    logger = logging.getLogger('trading_bot')
    logger.setLevel(logging.INFO)
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)  # Errors only to console, INFO to log
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()
