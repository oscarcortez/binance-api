import pandas as pd
from datetime import datetime
from binance.client import Client
from .client import get_binance_client


class MarketData:
    """
    Class to handle Binance market data operations.
    Provides methods to fetch prices, tickers, candlesticks, and order books.
    """

    def __init__(self):
        """Initialize MarketData with a Binance client instance."""
        self.client: Client = get_binance_client()

    def get_server_time(self) -> dict:
        """
        Get Binance server time.

        Returns:
            dict: Dictionary containing timestamp, datetime object, and formatted string
        """
        server_time = self.client.get_server_time()
        timestamp = server_time["serverTime"]
        readable_time = datetime.fromtimestamp(timestamp / 1000)

        return {
            "timestamp": timestamp,
            "datetime": readable_time,
            "formatted": readable_time.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def get_current_price(self, symbol: str = "BTCUSDT") -> float:
        """
        Get current price for a trading pair.

        Args:
            symbol: Trading pair symbol (default: 'BTCUSDT')

        Returns:
            float: Current price
        """
        ticker = self.client.get_symbol_ticker(symbol=symbol)
        return float(ticker["price"])

    def get_24h_ticker(self, symbol: str = "BTCUSDT") -> dict:
        """
        Get 24-hour ticker statistics for a trading pair.

        Args:
            symbol: Trading pair symbol (default: 'BTCUSDT')

        Returns:
            dict: Dictionary with price, change, volume, and other 24h statistics
        """
        ticker = self.client.get_ticker(symbol=symbol)

        return {
            "symbol": ticker["symbol"],
            "price": float(ticker["lastPrice"]),
            "change": float(ticker["priceChange"]),
            "change_percent": float(ticker["priceChangePercent"]),
            "high": float(ticker["highPrice"]),
            "low": float(ticker["lowPrice"]),
            "volume": float(ticker["volume"]),
            "quote_volume": float(ticker["quoteVolume"]),
        }

    def get_klines_dataframe(
        self,
        symbol: str = "BTCUSDT",
        interval: str = Client.KLINE_INTERVAL_1HOUR,
        limit: int = 100,
    ) -> pd.DataFrame:
        """
        Get candlestick/kline data as a pandas DataFrame.

        Args:
            symbol: Trading pair symbol (default: 'BTCUSDT')
            interval: Time interval (default: 1 hour)
            limit: Number of candles to retrieve (default: 100)

        Returns:
            pd.DataFrame: DataFrame with OHLCV data indexed by timestamp
        """
        klines = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)

        df = pd.DataFrame(
            klines,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_asset_volume",
                "trades",
                "taker_buy_base",
                "taker_buy_quote",
                "ignore",
            ],
        )

        # Convert data types
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")

        numeric_columns = [
            "open",
            "high",
            "low",
            "close",
            "volume",
            "quote_asset_volume",
            "taker_buy_base",
            "taker_buy_quote",
        ]
        df[numeric_columns] = df[numeric_columns].astype(float)
        df["trades"] = df["trades"].astype(int)

        
    def get_all_tickers(self) -> pd.DataFrame:
        """Todos los tickers en un DataFrame"""
        tickers = self.client.get_all_tickers()
        df = pd.DataFrame(tickers)
        df['price'] = df['price'].astype(float)
        df['symbol'] = df['symbol'].astype(str)
        
        return df

    def get_all_tickers_complete(self) -> pd.DataFrame:
        """Todos los tickers con información completa de 24h"""
        tickers = self.client.get_ticker()
        df = pd.DataFrame(tickers)
        
        # Columnas de tipo string
        string_columns = ['symbol']
        for col in string_columns:
            if col in df.columns:
                df[col] = df[col].astype(str)
        
        # Columnas numéricas (float)
        float_columns = [
            'priceChange', 'priceChangePercent', 'weightedAvgPrice',
            'prevClosePrice', 'lastPrice', 'lastQty', 'bidPrice', 
            'bidQty', 'askPrice', 'askQty', 'openPrice', 'highPrice', 
            'lowPrice', 'volume', 'quoteVolume'
        ]
        
        for col in float_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    print(f"⚠️ Error convirtiendo {col} a float: {e}")
        
        # Columnas numéricas (integer)
        int_columns = ['firstId', 'lastId', 'count']
        
        for col in int_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
                except Exception as e:
                    print(f"⚠️ Error convirtiendo {col} a int: {e}")
        
        # Columnas de timestamp (convertir a datetime)
        timestamp_columns = ['openTime', 'closeTime']
        
        for col in timestamp_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], unit='ms')
                except Exception as e:
                    print(f"⚠️ Error convirtiendo {col} a datetime: {e}")
        
        return df