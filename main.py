import sys
import json

import pandas as pd

from StockML.data.IEXCloudInterface import IEXCloudInterface
from StockML.data.RedditInterface import RedditInterface
from StockML.data.DataFileInterface import DataFileInterface
from StockML.models.StockPriceModel import StockPriceModel
from StockML.models.SubmissionSentimentModel import SubmissionSentimentModel
from StockML.utils.Utils import relative_path

def __get_news_data_for_all_tech_companies(companies):
    for company in companies:
        company_news_collection = IEXCloudInterface.get_news(company, 'last-week')
        DataFileInterface.write_to_file(relative_path('data/files/news.csv'), company_news_collection)

def __get_stats_for_all_tech_companies(companies):
    for company in companies:
        print(f"getting stat data for company: {company}")
        company_stat_data_collection = IEXCloudInterface.get_stats(company)
        DataFileInterface.write_to_file(relative_path('data/files/stock_stats.csv'), company_stat_data_collection)

def __get_historical_data_for_all_tech_companies(companies):
    for company in companies:
        print(f"getting historical data for company: {company}")
        company_historical_data_collection = IEXCloudInterface.get_historical_data(company, '1m')
        DataFileInterface.write_to_file(relative_path('data/files/stock_data.csv'), company_historical_data_collection)

def __get_companies():
    return DataFileInterface.get_company_symbols()

def __get_companies_related_reddit_submissions(companies):
    for company in companies:
        submission_dict_collection = RedditInterface.get_all_submissions_for(company)
        DataFileInterface.write_to_file(relative_path('data/files/stock_submissions.csv'), submission_dict_collection)

def __retrieve_data(companies):
    __get_historical_data_for_all_tech_companies(companies)
    __get_stats_for_all_tech_companies(companies)
    __get_companies_related_reddit_submissions(companies)

def __get_reddit_df(path):
    with open(relative_path(path)) as f:
        data = json.load(f)
        dict_collection = []
        for company in data['companies'].keys():
            for date in data['companies'][company].keys():
                row = data['companies'][company][date].copy()
                row['company'] = company
                row['date'] = date
            
            dict_collection.append(row)



        return pd.DataFrame(dict_collection)

if __name__ == '__main__':
    if '--get-data' in  sys.argv:
        companies = __get_companies()
        __retrieve_data(companies)

    if '--analyze-text' in sys.argv:
        reddit_submissions = pd.read_csv(relative_path('data/files/stock_submissions.csv'))
        ssm = SubmissionSentimentModel(reddit_submissions)
        ssm.analyze(relative_path('data/files/reddit_submissions_analyzed.json'))

    if '--train' in sys.argv:
        prediction_column_names = ['high', 'low', 'close']

        stock_stats_df = pd.read_csv(relative_path('data/files/stock_stats.csv'))

        spm = StockPriceModel()

        for prediction_column_name in prediction_column_names:
            stock_price_movement_df = pd.read_csv(relative_path('data/files/stock_data.csv'))
            stock_price_movement_df = stock_price_movement_df[['company', 'date', 'open', prediction_column_name]].copy()
            reddit_df = __get_reddit_df('data/files/reddit_submissions_analyzed.json')

            stock_df = pd.merge(stock_price_movement_df, stock_stats_df, on = 'company', how = 'inner')
            stock_df = pd.merge(stock_df, reddit_df, how = 'left', left_on = ['company', 'date'], right_on = ['company', 'date'])
            stock_df.to_csv(relative_path('data/files/stock_compiled.csv'), encoding = 'utf-8')

            columns_to_zero = ['negative_count', 'positive_count', 'neutral_count', 'sentiment']

            stock_df[columns_to_zero] = stock_df[columns_to_zero].fillna(value=0)

            spm.initialize_data(stock_df, prediction_column_name)
            spm.train('clf')

    if '--predict' in sys.argv:
        prediction_column_names = ['high', 'low', 'close']

        stock_stats_df = pd.read_csv(relative_path('data/files/stock_stats.csv'))

        for prediction_column_name in prediction_column_names:
            print(f'Predicting [{prediction_column_name}] column')
            prediction_entries = pd.read_csv(relative_path('data/files/prediction_entries.csv'))

            prediction_entries = prediction_entries[['company', 'date', 'open']].copy()
            stock_df = pd.merge(prediction_entries, stock_stats_df, on = 'company', how = 'inner')

            stock_df = StockPriceModel.prepare_df(stock_df)

            StockPriceModel.predict(stock_df, relative_path(f'models/files/predict_{prediction_column_name}.pkl'), False)
