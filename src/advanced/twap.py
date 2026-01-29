import time
from ..logging_config import logger
from ..orders import place_market_order
from binance.exceptions import BinanceAPIException

def execute_twap(client, symbol: str, side: str, total_quantity: float, duration_minutes: float, num_intervals: int):
    """
    Executes a TWAP (Time-Weighted Average Price) strategy by splitting a large order
    into smaller market orders over a specified duration.
    
    :param client: Binance API client
    :param symbol: Trading symbol (e.g., BTCUSDT)
    :param side: BUY or SELL
    :param total_quantity: Total amount to trade
    :param duration_minutes: Total time for the strategy
    :param num_intervals: Number of chunks to split the order into
    """
    if num_intervals <= 0:
        raise ValueError("Number of intervals must be greater than 0.")
    
    interval_quantity = total_quantity / num_intervals
    interval_seconds = (duration_minutes * 60) / num_intervals
    
    logger.info(f"Starting TWAP: {total_quantity} {symbol} over {duration_minutes}m ({num_intervals} chunks of {interval_quantity})")
    
    executed_total = 0
    orders = []
    
    for i in range(num_intervals):
        logger.info(f"TWAP Interval {i+1}/{num_intervals}: Placing Market Order for {interval_quantity}")
        try:
            response = place_market_order(client, symbol, side, interval_quantity)
            # Use origQty since executedQty might be 0 if the order is still "NEW" in the response
            qty_placed = float(response.get('origQty', interval_quantity))
            executed_total += qty_placed
            orders.append(response)
            logger.info(f"TWAP Interval {i+1} placed. Total progress: {executed_total}/{total_quantity}")
        except Exception as e:
            logger.error(f"TWAP Interval {i+1} failed: {str(e)}")
            # For a challenge, we might continue or stop. Let's log and keep going if possible.
        
        if i < num_intervals - 1:
            logger.info(f"TWAP waiting {interval_seconds} seconds for next interval...")
            time.sleep(interval_seconds)
            
    logger.info(f"TWAP strategy completed. Total executed: {executed_total}")
    return {
        "symbol": symbol,
        "side": side,
        "totalQty": total_quantity,
        "executedQty": executed_total,
        "numOrders": len(orders),
        "status": "COMPLETED" if len(orders) == num_intervals else "PARTIAL"
    }
