import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn import metrics 
from sklearn import linear_model
from sklearn import svm

import joblib

from StockML.utils.DataFrameUtils import define_result_wanted, convert_data_to_week_day
from StockML.utils.Utils import relative_path


class StockPriceModel:
    lowest_accuracy_wanted = .70

    @staticmethod
    def predict(df, model_file, has_actual):
        classifier = StockPriceModel.load_model(model_file)
        if has_actual:
            X = df[df.columns[:-1]] 
        else:
            X = df

        predictions = classifier.predict(X)

        print("Predictions:")
        print(predictions)

        if has_actual:
            print('Actual:')
            y = df[df.columns[-1]] 
            print(y)

    @staticmethod
    def load_model(file_name):
            return joblib.load(file_name)

    @staticmethod
    def prepare_df(df, prediction_column_name = None):
        if prediction_column_name:
            df = define_result_wanted(df, prediction_column_name)

        convert_data_to_week_day(df, 'date')

        df = StockPriceModel.map_company_names(df)
        return df

    @staticmethod
    def map_company_names(df):
        company_names = ['AAPL', 'MSFT', 'AMZN', 'GOOG', 'GOOGL', 'FB', 'BABA', \
         'NVDA', 'DIS', 'CRM', 'ADBE', 'NFLX', 'INTC', 'CSCO', 'ORCL', 'QCOM', \
          'ACN', 'TXN', 'SAP', 'ZM', 'SHOP', 'SNE', 'IBM', 'NOW', 'AMD', 'INTU', 'INFY', 'MU', 'NTDOY']

        company_dict = {}

        for idx, item in enumerate(company_names):
            company_dict[item] = idx
        
        df['company'] = df['company'].map(company_dict)
        return df

    def __init__(self, df = pd.DataFrame(), prediction_column_name = None):
        self.initialize_data(df, prediction_column_name)

    def initialize_data(self, df = pd.DataFrame(), prediction_column_name = None):
        if not df.empty and prediction_column_name:
            self.stock_df = StockPriceModel.prepare_df(df, prediction_column_name)
            self.prediction_column_name = prediction_column_name
            print("Data loaded...")
            print(self.stock_df.head())
        else:
            print("dataframe passed through is either invalid or prediction column name is invalid")

    def train(self, algorithm):
        X = self.stock_df[self.stock_df.columns[:-1]] 
        y = self.stock_df[self.stock_df.columns[-1]] 

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=1) 

        if algorithm == 'clf':
            self.train_classifier(X_train, X_test, y_train, y_test)

    def train_classifier(self, X_train, X_test, y_train, y_test):
        classifiers = [
            svm.SVR(),
            linear_model.SGDRegressor(),
            linear_model.BayesianRidge(),
            linear_model.LassoLars(),
            linear_model.ARDRegression(),
            linear_model.PassiveAggressiveRegressor(),
            linear_model.TheilSenRegressor(),
            linear_model.LinearRegression()
        ]

        best_accuracy = self.lowest_accuracy_wanted
        best_classifier = None

        for classifier in classifiers:
            classifier.fit(X_train, y_train)

            prediction_score = classifier.score(X_test, y_test)
            if prediction_score > best_accuracy:
                best_accuracy = prediction_score
                best_classifier = classifier

        if best_classifier:
            print(f"{classifier} performed the best with an accuracy of: {best_accuracy}")
            joblib.dump(classifier, relative_path(f'models/files/predict_{self.prediction_column_name}.pkl'))
