import finnhub
finnhub_client = finnhub.Client(api_key="c9324kiad3ic89vi6cmg")

print(finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249))