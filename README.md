# Binance Futures Trading Bot (Testnet)

A Python-based CLI trading bot for placing orders on the Binance Futures Testnet. Designed as a robust, production-ready implementation for a coding challenge.

## Features
- **Market Orders**: Instant execution at current price.
- **Limit Orders**: Precision entry at specific price targets.
- **TWAP Orders (Bonus)**: Time-Weighted Average Price. Splits large orders into smaller chunks over time to minimize market impact.
- **Robust Validation**: Checks symbols, quantities (LOT_SIZE), and price precision (PRICE_FILTER) before API calls.
- **Structured Logging**: All activities and errors tracked in `bot.log`.
- **Beautiful CLI**: Rich-formatted output for clear visibility.

## Setup

1. **Clone & Navigate**:
   ```bash
   cd trading_bot
   ```

2. **Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **API Credentials**:
   - Go to [Binance Futures Testnet](https://testnet.binancefuture.com).
   - Log in and generate your API Key and Secret Key.
   - Create a `.env` file in the root directory:
     ```env
     BINANCE_API_KEY=your_key_here
     BINANCE_SECRET_KEY=your_secret_here
     ```

## Usage

### Market Order
```bash
python cli.py market BTCUSDT BUY 0.001
```

### Limit Order
```bash
python cli.py limit BTCUSDT SELL 0.001 45000.50
```

### TWAP Order (Bonus)
```bash
# Buy 0.1 BTC over 5 minutes in 10 chunks
python cli.py twap BTCUSDT BUY 0.1 5 10
```

## Logging
All API interactions and errors are logged to `bot.log` with timestamps and structured levels (INFO/ERROR).

## Project Structure
```
trading_bot/
├── src/
│   ├── client.py          # API Initialization
│   ├── orders.py          # Execution Logic
│   ├── validators.py      # Input/Exchange Validation
│   ├── logging_config.py  # Logger Setup
│   └── advanced/
│       └── stop_limit.py  # Bonus Feature
├── cli.py                 # Typer/Rich Entry Point
├── bot.log               # Activity Logs
├── requirements.txt
└── README.md
```
