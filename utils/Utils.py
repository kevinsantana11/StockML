from pandas import date_range
from pathlib import Path

def get_date_ranges(start, end):
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


def relative_path(path):
	return (Path.cwd() / path).resolve()