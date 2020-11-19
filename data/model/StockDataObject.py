class StockDataObject:
	def __init__(self, symbol, payload):
		self.company = symbol
		self.date = payload['date']
		self.open = payload['open']
		self.high = payload['high']
		self.low = payload['low']
		self.close = payload['close']
