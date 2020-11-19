import time
import json
import pandas as pd

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

class SubmissionSentimentModel:
    def __init__(self, df):
        self.sia = SentimentIntensityAnalyzer()
        self.df = df

    def analyze(self, save_file):
        last_month_company_sentiment = {'companies': {}}
        companies = last_month_company_sentiment['companies']

        for index, row in self.df.iterrows():
            company = row['company']
            title = row['title']
            text = row['text']
            date_created = row['date_created']

            title_sentiment = self.__check_text_sentiment(title)
            text_sentiment = self.__check_text_sentiment(text)

            if not text_sentiment:
                text_sentiment = title_sentiment 

            evaluated_sentiment = (title_sentiment + text_sentiment) / 2

            if evaluated_sentiment > 0:
                positive_sentiment_counter = 1
                neutral_sentiment_counter = 0
                negative_sentiment_counter = 0
            elif evaluated_sentiment < 0:
                positive_sentiment_counter = 0
                neutral_sentiment_counter = 0
                negative_sentiment_counter = 1
            else:
                positive_sentiment_counter = 0
                neutral_sentiment_counter = 1
                negative_sentiment_counter = 0

            date_created_simple = str(time.strftime('%Y-%m-%d', time.localtime(date_created)))

            if companies.get(company):
                company = companies.get(company)

                if company.get(date_created_simple):
                    old_positive_count = company[date_created_simple]['positive_count']
                    old_negative_count = company[date_created_simple]['negative_count']
                    old_neutral_count = company[date_created_simple]['neutral_count']

                    new_sentiment = (company[date_created_simple]['sentiment'] + evaluated_sentiment) / 2
                    new_positive_count = old_positive_count + positive_sentiment_counter
                    new_neutral_count = old_neutral_count + neutral_sentiment_counter
                    new_negative_count = old_negative_count + negative_sentiment_counter

                    company[date_created_simple]['sentiment'] = new_sentiment
                    company[date_created_simple]['positive_count'] =  new_positive_count
                    company[date_created_simple]['neutral_count'] = new_neutral_count
                    company[date_created_simple]['negative_count'] = new_negative_count
                else:
                    company[date_created_simple] = {
                        'sentiment': evaluated_sentiment,
                        'positive_count': positive_sentiment_counter,
                        'neutral_count': neutral_sentiment_counter,
                        'negative_count': negative_sentiment_counter
                    }
            else:
                companies[company] = {
                    date_created_simple: {
                        'sentiment': evaluated_sentiment,
                        'positive_count': positive_sentiment_counter,
                        'neutral_count': neutral_sentiment_counter,
                        'negative_count': negative_sentiment_counter
                    }
                }


        
        with open(save_file, "w") as outfile:  
            json.dump(last_month_company_sentiment, outfile, indent = 4, sort_keys = True) 

    def __check_text_sentiment(self, text):
        if not pd.isnull(text):
            return self.sia.polarity_scores(text)['compound']
        else:
            return None

