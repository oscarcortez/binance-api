from binance import ThreadedWebsocketManager
from .client import get_binance_client
import json

class WebSocketStreams:
    def __init__(self):
        self.client = get_binance_client()
        self.twm = ThreadedWebsocketManager(
            api_key=self.client.API_KEY,
            api_secret=self.client.API_SECRET,
            testnet=self.client.testnet
        )
        self.twm.start()
    
    def start_kline_socket(self, symbol: str, interval: str, callback):
        """
        Stream de velas en tiempo real
        """
        def handle_message(msg):
            if msg['e'] == 'kline':
                kline = msg['k']
                data = {
                    'symbol': kline['s'],
                    'timestamp': kline['t'],
                    'open': float(kline['o']),
                    'high': float(kline['h']),
                    'low': float(kline['l']),
                    'close': float(kline['c']),
                    'volume': float(kline['v']),
                    'is_closed': kline['x']
                }
                callback(data)
        
        self.twm.start_kline_socket(
            callback=handle_message,
            symbol=symbol,
            interval=interval
        )
    
    def start_trade_socket(self, symbol: str, callback):
        """Stream de trades en tiempo real"""
        def handle_message(msg):
            if msg['e'] == 'trade':
                data = {
                    'symbol': msg['s'],
                    'price': float(msg['p']),
                    'quantity': float(msg['q']),
                    'timestamp': msg['T'],
                    'is_buyer_maker': msg['m']
                }
                callback(data)
        
        self.twm.start_trade_socket(callback=handle_message, symbol=symbol)
    
    def stop(self):
        """Detener todos los streams"""
        self.twm.stop()