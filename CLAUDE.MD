# Binance API Data Extractor - Project Documentation

## Project Overview
POC to collect Binance market data using Python and Poetry. The project extracts ticker information from Binance and saves it to CSV files for analysis.

## Tech Stack
- **Language**: Python 3.14+
- **Package Manager**: Poetry
- **Main Dependencies**:
  - `python-binance` (1.0.34+) - Binance API wrapper
  - `python-dotenv` (1.2.1+) - Environment variable management
  - `pandas` (2.3.3+) - Data manipulation and CSV export
- **Dev Dependencies**:
  - `pytest` (9.0.2+) - Testing framework
  - `black` (25.12.0+) - Code formatting
  - `flake8` (7.3.0+) - Linting

## Project Structure
```
binance-api/
├── binance_api/
│   ├── __init__.py
│   ├── main.py              # Entry point - extracts all tickers and USDT pairs
│   └── src/
│       ├── client.py        # Singleton Binance client manager
│       └── market_data.py   # Market data operations (prices, tickers, klines)
├── pyproject.toml           # Poetry dependencies and project metadata
└── README.md
```

## Key Components

### 1. Client Management (binance_api/src/client.py)
- **BinanceClientSingleton**: Ensures single connection to Binance API
- **Environment Variables**:
  - `BINANCE_API_KEY` - Your Binance API key
  - `BINANCE_API_SECRET` - Your Binance API secret
  - `TESTNET` - Set to 'True' for testnet, 'False' for production (defaults to True)
- **Factory Function**: `get_binance_client()` - Returns singleton client instance

### 2. Market Data Operations (binance_api/src/market_data.py)
Methods available:
- `get_server_time()` - Fetch Binance server timestamp
- `get_current_price(symbol)` - Get current price for a trading pair
- `get_24h_ticker(symbol)` - Get 24-hour statistics (price, volume, change)
- `get_klines_dataframe(symbol, interval, limit)` - Get OHLCV candlestick data as DataFrame

### 3. Main Script (binance_api/main.py)
Current functionality:
- Extracts all available tickers (method `get_all_tickers_complete()` referenced but not found in market_data.py)
- Filters USDT trading pairs
- Saves data to timestamped CSV files

## Setup & Installation

1. Install dependencies:
```bash
poetry install
```

2. Create `.env` file with your API credentials:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
TESTNET=True
```

3. Run the extractor:
```bash
poetry run python main.py
```

## Output Files
The script generates CSV files with timestamps:
- `all_tickers_complete_YYYYMMDD_HHMMSS.csv` - All tickers
- `usdt_tickers_complete_YYYYMMDD_HHMMSS.csv` - Filtered USDT pairs only

## Known Issues
- `main.py:10` references `market.get_all_tickers_complete()` which doesn't exist in `market_data.py:1-104`
- Imports in `main.py:2-3` reference `TradingOperations` and `WebSocketStreams` modules that don't exist

## Development Notes
- Uses singleton pattern for Binance client to avoid multiple connections
- Defaults to testnet for safety (set `TESTNET=False` for production)
- All market data methods return structured data (dicts or DataFrames)
- Timestamps are automatically converted to readable datetime format
- OHLCV data includes comprehensive fields (open, high, low, close, volume, trades, etc.)

## Recent Changes
- Latest commit (8b4d932): Refactored main.py for improved logging and consistency; enhanced client.py with detailed docstrings; removed unused trading and websocket_streams modules
- Previous commit (3d25e50): Initial commit

## Author
Oscar Cortez (oscarkortez@gmail.com)
