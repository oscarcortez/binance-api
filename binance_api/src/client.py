import os
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv

load_dotenv()

class BinanceClientSingleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        testnet = os.getenv('TESTNET', 'True').lower() == 'true'
        
        if testnet:
            self.client = Client(api_key, api_secret, testnet=True)
            print("🧪 Conectado a Binance TESTNET")
        else:
            self.client = Client(api_key, api_secret)
            print("💰 Conectado a Binance PRODUCCIÓN")
    
    def get_client(self):
        return self.client

def get_binance_client() -> Client:
    """Factory function para obtener el cliente de Binance"""
    singleton = BinanceClientSingleton()
    return singleton.get_client()