import pandas as pd

class DataFrameUtils:
    @staticmethod
    def define_result_wanted(df, column_name):
        return df[[c for c in df if c not in [column_name]] + [column_name]]

    @staticmethod
    def date_column_to_epoch(df, column_name):
        df[column_name] = pd.to_datetime(df[column_name], format='%Y-%m-%d')
        df[column_name] = df[column_name].astype('int64')
        return df
