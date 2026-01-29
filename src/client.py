from binance.client import Client
import os
from dotenv import load_dotenv
from .logging_config import logger

def get_binance_client():
    """
    Initializes and returns the Binance Futures Testnet client.
    Loads API keys from .env file.
    """
    load_dotenv()
    
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_SECRET_KEY')
    
    if not api_key or not api_secret:
        logger.error("API keys missing from .env file.")
        raise ValueError("BINANCE_API_KEY and BINANCE_SECRET_KEY must be set in .env")
        
    try:
        client = Client(
            api_key,
            api_secret,
            testnet=True  # CRITICAL: Keep on testnet!
        )
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Binance client: {str(e)}")
        raise
