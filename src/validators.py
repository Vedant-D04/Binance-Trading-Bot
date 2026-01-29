from .logging_config import logger
from binance.exceptions import BinanceAPIException

def validate_symbol(client, symbol: str):
    """
    Validates if the symbol exists on the exchange and returns its filters/rules.
    """
    try:
        exchange_info = client.futures_exchange_info()
        for s in exchange_info['symbols']:
            if s['symbol'] == symbol:
                return s
        raise ValueError(f"Symbol '{symbol}' not found on exchange.")
    except BinanceAPIException as e:
        logger.error(f"Error fetching exchange info: {e}")
        raise

def validate_side(side: str):
    """Validates if the side is BUY or SELL."""
    if side.upper() not in ['BUY', 'SELL']:
        raise ValueError("Side must be 'BUY' or 'SELL'.")
    return side.upper()

def validate_quantity(symbol_info, quantity: float):
    """
    Validates quantity against LOT_SIZE filter.
    """
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
        
    lot_size_filter = next(f for f in symbol_info['filters'] if f['filterType'] == 'LOT_SIZE')
    min_qty = float(lot_size_filter['minQty'])
    max_qty = float(lot_size_filter['maxQty'])
    step_size = float(lot_size_filter['stepSize'])
    
    if quantity < min_qty:
        raise ValueError(f"Quantity {quantity} is less than minimum {min_qty}.")
    if quantity > max_qty:
        raise ValueError(f"Quantity {quantity} is greater than maximum {max_qty}.")
    
    # Check precision/step size
    # Use round to handle floating point math issues
    precision_len = 0
    if '.' in str(step_size).rstrip('0'):
        precision_len = len(str(step_size).split('.')[-1])
    
    if round(quantity % step_size, 10) not in [0, round(step_size, 10)]:
        raise ValueError(f"Quantity {quantity} does not match step size {step_size}. Max precision: {precision_len} decimals.")
    
    return round(quantity, precision_len)

def validate_price(symbol_info, price: float):
    """
    Validates price against PRICE_FILTER.
    """
    if price <= 0:
        raise ValueError("Price must be greater than 0.")
        
    price_filter = next(f for f in symbol_info['filters'] if f['filterType'] == 'PRICE_FILTER')
    min_price = float(price_filter['minPrice'])
    max_price = float(price_filter['maxPrice'])
    tick_size = float(price_filter['tickSize'])
    
    if price < min_price:
        raise ValueError(f"Price {price} is less than minimum {min_price}.")
    if price > max_price:
        raise ValueError(f"Price {price} is greater than maximum {max_price}.")
        
    precision_len = 0
    if '.' in str(tick_size).rstrip('0'):
        precision_len = len(str(tick_size).split('.')[-1])

    if round(price % tick_size, 10) not in [0, round(tick_size, 10)]:
        raise ValueError(f"Price {price} does not match tick size {tick_size}. Max precision: {precision_len} decimals.")
        
    return round(price, precision_len)
