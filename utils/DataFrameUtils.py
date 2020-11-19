import pandas as pd
from datetime import datetime


def define_result_wanted(df, column_name):
    return df[[c for c in df if c not in [column_name]] + [column_name]]

def date_column_to_epoch(df, column_name):
    df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%d')
    df[column_name] = df[column_name].astype('int64')
    return df

def convert_data_to_week_day(df, column_name):
    df[column_name] = df[column_name].map(lambda date:  date_string_to_datetime(date).weekday())

def date_string_to_datetime(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")
