class StatObject:
	def __init__(self, symbol, payload):
		self.company = symbol
		self.week_52_high = payload['week52high']
		self.week_52_low = payload['week52low']
		self.week_52_change = payload['week52change']
		self.avg_10_volume = payload['avg10Volume']
		self.avg_30_volume = payload['avg30Volume']
		self.day_50_moving_avg = payload['day50MovingAvg']
		self.ttm_EPS = payload['ttmEPS']
		self.pe_ratio = payload['peRatio']
		self.beta = payload['beta']
		self.year_1_change_percent = payload['year1ChangePercent']
		self.month_6_change_percent = payload['month6ChangePercent']
		self.month_1_change_percent = payload['month1ChangePercent']
		self.day_30_change_percent = payload['day30ChangePercent']
		self.day_5_change_percent = payload['day5ChangePercent']