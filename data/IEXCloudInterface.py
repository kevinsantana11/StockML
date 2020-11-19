import requests

from StockML.data.model.NewsObject import NewsObject
from StockML.data.model.StockDataObject import StockDataObject
from StockML.data.model.StatObject import StatObject

SECRET_IEX_API_KEY = 'sk_a616a94c96104ebca0bbcf5ff9c30562'
PUBLIC_IEX_API_KEY = ''
IEX_CLOUD_URL = 'https://cloud.iexapis.com/stable'


class IEXCloudInterface:
	@staticmethod
	def get_historical_data(symbol, range):
		api_call_url = f'{IEX_CLOUD_URL}/stock/{symbol}/chart/{range}?token={SECRET_IEX_API_KEY}'
		headers = {"Accept": "application/json"}
		response = requests.get(api_call_url, headers=headers)
		return [StockDataObject(symbol, item) for item in response.json()]

	@staticmethod
	def get_news(symbol, range):
		api_call_url = f'{IEX_CLOUD_URL}/time-series/news/{symbol}/range={range}&token={SECRET_IEX_API_KEY}'
		headers = {"Accept": "application/json"}

		response = requests.get(api_call_url, headers=headers)
		return [NewsObject(symbol, item) for item in response.json()]

	@staticmethod
	def get_stats(symbol):
		api_call_url = f'{IEX_CLOUD_URL}/stock/{symbol}/stats?token={SECRET_IEX_API_KEY}'
		headers = {"Accept": "application/json"}

		response = requests.get(api_call_url, headers=headers)
		return [StatObject(symbol, response.json())]

