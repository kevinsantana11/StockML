import csv
from pathlib import Path


class DataFileInterface:
	@staticmethod
	def get_company_symbols():
		company_symbols = []

		with open('.\\data\\files\\stock_symbols.csv', encoding = 'utf-8') as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')

			for row in readCSV:
				company_symbols.append(row[0])

		return company_symbols

	@staticmethod
	def write_to_file(file_name, collection):
		file_exist = Path(file_name).exists()

		with open(file_name, 'a', newline = '', encoding = 'utf-8') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames = collection[0].__dict__.keys())

			if not file_exist:
				writer.writeheader()

			writer.writerows([item.__dict__ for item in collection])
