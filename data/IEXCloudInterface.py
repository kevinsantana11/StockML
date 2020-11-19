import requests

import StockML.data.config
from StockML.data.model.NewsObject import NewsObject
from StockML.data.model.StockDataObject import StockDataObject
from StockML.data.model.StatObject import StatObject


class IEXCloudInterface:
	@staticmethod
	def get_historical_data(symbol, range):
		api_call_url = f'{config.iexcloud_url}/stock/{symbol}/chart/{range}?token={config.iexcloud_key}'
		headers = {"Accept": "application/json"}
		response = requests.get(api_call_url, headers=headers)
		return [StockDataObject(symbol, item) for item in response.json()]

	@staticmethod
	def get_news(symbol, range):
		api_call_url = f'{config.iexcloud_url}/time-series/news/{symbol}/range={range}&token={config.iexcloud_key}'
		headers = {"Accept": "application/json"}

		response = requests.get(api_call_url, headers=headers)
		return [NewsObject(symbol, item) for item in response.json()]

	@staticmethod
	def get_stats(symbol):
		api_call_url = f'{config.iexcloud_url}/stock/{symbol}/stats?token={config.iexcloud_key}'
		headers = {"Accept": "application/json"}

		response = requests.get(api_call_url, headers=headers)
		return [StatObject(symbol, response.json())]

