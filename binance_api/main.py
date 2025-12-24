from src.market_data import MarketData
from src.trading import TradingOperations
from src.websocket_streams import WebSocketStreams
import time
from datetime import datetime

def main():
    market = MarketData()
    print("\n=== Todos los tickers (completo) ===")
    all_tickers_complete = market.get_all_tickers_complete()
    
    all_tickers_complete['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Guardar CSV completo
    filename_complete = f"all_tickers_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    all_tickers_complete.to_csv(filename_complete, index=False)
    print(f"✅ Guardado {len(all_tickers_complete)} tickers completos en: {filename_complete}")
    
    # Filtrar USDT con columna 'lastPrice'
    usdt_pairs_complete = all_tickers_complete[
        all_tickers_complete['symbol'].str.endswith('USDT')
    ].sort_values('symbol')
    
    print(f"Total de pares USDT (completo): {len(usdt_pairs_complete)}")
    
    # Guardar USDT filtrado
    usdt_filename = f"usdt_tickers_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    usdt_pairs_complete.to_csv(usdt_filename, index=False)
    print(f"✅ Guardado {len(usdt_pairs_complete)} pares USDT en: {usdt_filename}")

if __name__ == '__main__':
    main()