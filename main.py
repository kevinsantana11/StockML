import sys 
import pandas as pd

sys.path.append('..\StockPredictor')


from StockML.data.IEXCloudInterface import IEXCloudInterface
from StockML.data.DataFileInterface import DataFileInterface
from StockML.models.StockPriceModel import StockPriceModel

def __get_news_data_for_all_tech_companies(companies):
    for company in companies:
        company_news_collection = IEXCloudInterface.get_news(company, 'last-week')
        DataFileInterface.write_to_file('.\\data\\files\\news.csv', company_news_collection)

def __get_stats_for_all_tech_companies(companies):
    for company in companies:
        print(f"getting stat data for company: {company}")
        company_stat_data_collection = IEXCloudInterface.get_stats(company)
        DataFileInterface.write_to_file('.\\data\\files\\stock_stats.csv', company_stat_data_collection)

def __get_historical_data_for_all_tech_companies(companies):
    for company in companies:
        print(f"getting historical data for company: {company}")
        company_historical_data_collection = IEXCloudInterface.get_historical_data(company, '1m')
        DataFileInterface.write_to_file('.\\data\\files\\stock_data.csv', company_historical_data_collection)

def __get_companies():
    return DataFileInterface.get_company_symbols()

def __retrieve_data(companies):
    __get_historical_data_for_all_tech_companies(companies)
    __get_stats_for_all_tech_companies(companies)

if __name__ == '__main__':
    if '--get-data' in  sys.argv:
        companies = __get_companies()
        __retrieve_data(companies)

    if '--train' in sys.argv:
        prediction_column_names = ['high', 'low', 'close']

        stock_stats_df = pd.read_csv('.\\data\\files\\stock_stats.csv')

        spm = StockPriceModel()

        for prediction_column_name in prediction_column_names:
            stock_price_movement_df = pd.read_csv('.\\data\\files\\stock_data.csv') 
            stock_price_movement_df = stock_price_movement_df[['company', 'date', 'open', prediction_column_name]].copy()
            stock_df = pd.merge(stock_price_movement_df, stock_stats_df, on = 'company', how = 'inner')

            spm.initialize_data(stock_df, prediction_column_name)
            spm.train('clf')

    if '--predict' in sys.argv:
        prediction_column_names = ['high', 'low', 'close']

        stock_stats_df = pd.read_csv('.\\data\\files\\stock_stats.csv')

        for prediction_column_name in prediction_column_names:
            prediction_entries = pd.read_csv('.\\data\\files\\prediction_entries.csv') 

            prediction_entries = prediction_entries[['company', 'date', 'open', prediction_column_name]].copy()
            stock_df = pd.merge(prediction_entries, stock_stats_df, on = 'company', how = 'inner')

            stock_df = StockPriceModel.prepare_df(stock_df, prediction_column_name)

            StockPriceModel.predict(stock_df, f'.\\models\\files\\predict_{prediction_column_name}.pkl', True)
        