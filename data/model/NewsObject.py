class NewsObject:
	def __init__(self, symbol, payload):
		self.company = symbol
		self.url = payload['url']
		self.title = payload['headline']
		self.summary = payload['summary']
		self.time_stamp = payload['datetime']

	def print_obj(self):
		print(f'url: {self.url}\ntitle: {self.title}\nsummary: {self.summary}\ntime_stamp: {self.time_stamp}')
