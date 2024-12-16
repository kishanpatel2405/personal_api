import ccxt

exchange = ccxt.binance()
markets = exchange.load_markets()
print(markets.keys())
