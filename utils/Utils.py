from pandas import date_range

class Utils:
	@staticmethod
	def __get_date_ranges(start, end):
		date_list = date_range(start, periods=end).to_pydatetime().tolist()

		date_strings = []

		for date in date_list:
			month = None
			day = None

			if date.month < 10:
				month = f'0{date.month}'
			else:
				month = date.month

			if date.day < 10:
				day = f'0{date.day}'
			else:
				day = date.day

			date_string = f'{date.year}{month}{day}'
			date_strings.append(date_string)

		return date_strings