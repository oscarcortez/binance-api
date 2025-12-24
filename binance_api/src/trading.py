from binance.client import Client
from binance.enums import *
from .client import get_binance_client

class TradingOperations:
    def __init__(self):
        self.client: Client = get_binance_client()
    
    def get_account_info(self) -> dict:
        """Información de la cuenta"""
        account = self.client.get_account()
        
        balances = [
            {
                'asset': balance['asset'],
                'free': float(balance['free']),
                'locked': float(balance['locked'])
            }
            for balance in account['balances']
            if float(balance['free']) > 0 or float(balance['locked']) > 0
        ]
        
        return {
            'can_trade': account['canTrade'],
            'can_withdraw': account['canWithdraw'],
            'can_deposit': account['canDeposit'],
            'balances': balances
        }
    
    def get_asset_balance(self, asset: str = 'USDT') -> dict:
        """Balance de un activo específico"""
        balance = self.client.get_asset_balance(asset=asset)
        return {
            'asset': balance['asset'],
            'free': float(balance['free']),
            'locked': float(balance['locked']),
            'total': float(balance['free']) + float(balance['locked'])
        }
    
    def create_market_order(
        self,
        symbol: str,
        side: str,  # 'BUY' o 'SELL'
        quantity: float
    ) -> dict:
        """
        Crear orden de mercado (ejecución inmediata)
        ⚠️ CUIDADO: Esta orden se ejecutará inmediatamente
        """
        order = self.client.create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return order
    
    def create_limit_order(
        self,
        symbol: str,
        side: str,  # 'BUY' o 'SELL'
        quantity: float,
        price: float
    ) -> dict:
        """
        Crear orden limitada (se ejecuta al precio especificado)
        """
        order = self.client.create_order(
            symbol=symbol,
            side=side,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,  # Good Till Cancelled
            quantity=quantity,
            price=price
        )
        return order
    
    def create_test_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float = None
    ) -> dict:
        """
        Orden de prueba (no se ejecuta realmente)
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        
        if order_type == ORDER_TYPE_LIMIT:
            params['timeInForce'] = TIME_IN_FORCE_GTC
            params['price'] = price
        
        result = self.client.create_test_order(**params)
        return {'success': True, 'message': 'Test order validated'}
    
    def cancel_order(self, symbol: str, order_id: int) -> dict:
        """Cancelar una orden"""
        return self.client.cancel_order(symbol=symbol, orderId=order_id)
    
    def get_open_orders(self, symbol: str = None) -> list:
        """Órdenes abiertas"""
        if symbol:
            return self.client.get_open_orders(symbol=symbol)
        return self.client.get_open_orders()
    
    def get_order_status(self, symbol: str, order_id: int) -> dict:
        """Estado de una orden"""
        return self.client.get_order(symbol=symbol, orderId=order_id)