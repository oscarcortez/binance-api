import os
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv

load_dotenv()


class BinanceClientSingleton:
    """
    Singleton class to manage a single Binance client instance.
    Ensures only one connection to Binance API exists throughout the application.
    """

    _instance = None

    def __new__(cls):
        """
        Create or return the existing singleton instance.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initialize the Binance client with API credentials from environment variables.
        Automatically connects to testnet or production based on TESTNET env variable.
        """
        # Load API credentials from .env file
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        # Check if testnet mode is enabled (defaults to True for safety)
        testnet = os.getenv("TESTNET", "True").lower() == "true"

        if testnet:
            # Connect to Binance testnet (fake money, safe for testing)
            self.client = Client(api_key, api_secret, testnet=True)
            print("🧪 Connected to Binance TESTNET")
        else:
            # Connect to Binance production (real money - be careful!)
            self.client = Client(api_key, api_secret)
            print("💰 Connected to Binance PRODUCTION")

    def get_client(self):
        """
        Returns the Binance client instance.

        Returns:
            Client: Binance API client instance
        """
        return self.client


def get_binance_client() -> Client:
    """
    Factory function to get the Binance client singleton instance.

    Returns:
        Client: Binance API client instance

    Example:
        client = get_binance_client()
        price = client.get_symbol_ticker(symbol='BTCUSDT')
    """
    singleton = BinanceClientSingleton()
    return singleton.get_client()
