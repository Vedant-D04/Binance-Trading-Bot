from .logging_config import logger
from .validators import validate_symbol, validate_side, validate_quantity, validate_price
from binance.exceptions import BinanceAPIException

def place_market_order(client, symbol: str, side: str, quantity: float):
    """
    Places a Market Order on Binance Futures Testnet.
    """
    logger.info(f"Placing MARKET order: {symbol} {side} {quantity}")
    
    try:
        # Validate inputs
        symbol_info = validate_symbol(client, symbol)
        side = validate_side(side)
        quantity = validate_quantity(symbol_info, quantity)
        
        # Execute order
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        
        logger.info(f"Market order placed successfully: {response['orderId']}")
        return response
        
    except (ValueError, BinanceAPIException) as e:
        logger.error(f"Market order failed: {str(e)}")
        raise

def place_limit_order(client, symbol: str, side: str, quantity: float, price: float):
    """
    Places a Limit Order on Binance Futures Testnet.
    """
    logger.info(f"Placing LIMIT order: {symbol} {side} {quantity} @ {price}")
    
    try:
        # Validate inputs
        symbol_info = validate_symbol(client, symbol)
        side = validate_side(side)
        quantity = validate_quantity(symbol_info, quantity)
        price = validate_price(symbol_info, price)
        
        # Execute order
        # GTC (Good Till Cancel) is standard for limit orders
        response = client.futures_create_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=price
        )
        
        logger.info(f"Limit order placed successfully: {response['orderId']}")
        return response
        
    except (ValueError, BinanceAPIException) as e:
        logger.error(f"Limit order failed: {str(e)}")
        raise
