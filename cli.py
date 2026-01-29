import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.client import get_binance_client
from src.orders import place_market_order, place_limit_order
from src.advanced.twap import execute_twap
from src.logging_config import logger

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

def format_success(order):
    """Prints a beautiful success panel."""
    table = Table(show_header=False, box=None)
    table.add_row("Order ID", str(order.get('orderId')))
    table.add_row("Symbol", order.get('symbol'))
    table.add_row("Side", order.get('side'))
    table.add_row("Type", order.get('type'))
    table.add_row("Quantity", str(order.get('origQty')))
    table.add_row("Status", order.get('status'))
    
    avg_price = order.get('avgPrice', '0.00')
    if float(avg_price) == 0 and order.get('price'):
        avg_price = order.get('price')
        
    table.add_row("Price", f"${float(avg_price):,.2f}")
    
    console.print(Panel(
        table,
        title="[bold green]✓ Order Placed Successfully![/bold green]",
        border_style="green",
        expand=False
    ))

def format_twap_success(result):
    """Prints a beautiful TWAP success panel."""
    table = Table(show_header=False, box=None)
    table.add_row("Symbol", result['symbol'])
    table.add_row("Side", result['side'])
    table.add_row("Target Qty", str(result['totalQty']))
    table.add_row("Executed Qty", str(result['executedQty']))
    table.add_row("Intervals", str(result['numOrders']))
    table.add_row("Status", result['status'])
    
    console.print(Panel(
        table,
        title="[bold green]✓ TWAP Completed![/bold green]",
        border_style="cyan",
        expand=False
    ))

def format_error(error_msg, details=""):
    """Prints a beautiful error panel."""
    error_content = f"[bold red]Error:[/bold red] {error_msg}"
    if details:
        error_content += f"\n[bold yellow]Details:[/bold yellow] {details}"
        
    console.print(Panel(
        error_content,
        title="[bold red]✗ Order Failed[/bold red]",
        border_style="red",
        expand=False
    ))

@app.command()
def market(
    symbol: str = typer.Argument(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side (BUY or SELL)"),
    quantity: float = typer.Argument(..., help="Order quantity")
):
    """Place a MARKET order."""
    try:
        client = get_binance_client()
        response = place_market_order(client, symbol, side, quantity)
        format_success(response)
    except Exception as e:
        format_error(str(e))
        raise typer.Exit(code=1)

@app.command()
def limit(
    symbol: str = typer.Argument(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side (BUY or SELL)"),
    quantity: float = typer.Argument(..., help="Order quantity"),
    price: float = typer.Argument(..., help="Limit price")
):
    """Place a LIMIT order."""
    try:
        client = get_binance_client()
        response = place_limit_order(client, symbol, side, quantity, price)
        format_success(response)
    except Exception as e:
        format_error(str(e))
        raise typer.Exit(code=1)

@app.command()
def twap(
    symbol: str = typer.Argument(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Argument(..., help="Order side (BUY or SELL)"),
    quantity: float = typer.Argument(..., help="Total quantity"),
    duration: float = typer.Argument(..., help="Duration in minutes"),
    intervals: int = typer.Argument(..., help="Number of intervals")
):
    """Place a TWAP order (Bonus: splits large order into chunks)."""
    try:
        client = get_binance_client()
        response = execute_twap(client, symbol, side, quantity, duration, intervals)
        format_twap_success(response)
    except Exception as e:
        format_error(str(e))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
