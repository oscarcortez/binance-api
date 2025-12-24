# Binance API Data Extractor

A Python-based proof of concept for collecting and analyzing cryptocurrency market data from Binance. This project extracts real-time ticker information, filters trading pairs, and exports data to CSV files for further analysis.

## Features

- Real-time market data extraction from Binance
- Support for both testnet and production environments
- Automatic filtering of USDT trading pairs
- CSV export with timestamps for historical tracking
- Singleton pattern for efficient API connection management
- Comprehensive market data operations (prices, tickers, candlesticks)

## Tech Stack

- **Python**: 3.14+
- **Package Manager**: Poetry
- **Key Libraries**:
  - `python-binance` - Official Binance API wrapper
  - `pandas` - Data manipulation and analysis
  - `python-dotenv` - Environment configuration

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd binance-api
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the project root with your Binance API credentials:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
TESTNET=True
```

> **Note**: Set `TESTNET=True` for testing with fake funds, or `TESTNET=False` for production trading (use with caution).

## Usage

Run the data extractor:
```bash
poetry run python main.py
```

This will:
1. Connect to Binance API (testnet or production based on your `.env` settings)
2. Extract all available ticker data
3. Filter USDT trading pairs
4. Save data to timestamped CSV files:
   - `all_tickers_complete_YYYYMMDD_HHMMSS.csv`
   - `usdt_tickers_complete_YYYYMMDD_HHMMSS.csv`

## Project Structure

```
binance-api/
├── binance_api/
│   ├── __init__.py
│   ├── main.py              # Main entry point
│   └── src/
│       ├── client.py        # Binance client singleton
│       └── market_data.py   # Market data operations
├── pyproject.toml           # Project dependencies
├── .env                     # API credentials (create this)
└── README.md
```

## API Methods Available

The `MarketData` class provides:

- `get_server_time()` - Get Binance server timestamp
- `get_current_price(symbol)` - Current price for a trading pair
- `get_24h_ticker(symbol)` - 24-hour statistics (price, volume, change%)
- `get_klines_dataframe(symbol, interval, limit)` - OHLCV candlestick data

## Development

Format code with Black:
```bash
poetry run black .
```

Run linting with Flake8:
```bash
poetry run flake8 .
```

Run tests:
```bash
poetry run pytest
```

## Getting Binance API Keys

1. Create a Binance account at [binance.com](https://www.binance.com)
2. Enable Two-Factor Authentication (2FA)
3. Go to API Management in your account settings
4. Create a new API key
5. Copy the API Key and Secret to your `.env` file

For testnet API keys, visit [testnet.binance.vision](https://testnet.binance.vision/)

## Security Notes

- Never commit your `.env` file or expose API keys
- Use testnet for development and testing
- Restrict API key permissions (enable only what you need)
- Consider using IP restrictions on your API keys

## Author

**Oscar Cortez**
- Email: oscarkortez@gmail.com
- GitHub: [@oscarkortez](https://github.com/oscarkortez)

## License

This project is a proof of concept for educational and development purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This software is for educational purposes only. Use at your own risk. The author is not responsible for any financial losses incurred through the use of this software.