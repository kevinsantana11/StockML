import praw

import StockML.data.config
from StockML.data.model.RedditSubmissionObject import RedditSubmissionObject
from StockML.data.DataFileInterface import DataFileInterface


class RedditInterface:
    reddit = praw.Reddit(client_id = config.reddit_id,
                         client_secret = config.client_secret,
                         password = config.reddit_pass,
                         user_agent = config.reddit_user_agent,
                         username = config.reddit_user)

    @staticmethod
    def verify():
        reddit = RedditInterface.reddit
        print(reddit.user.me())

    @staticmethod
    def get_all_submissions_for(company):
        submission_dict_collection = []
        for submission in RedditInterface.reddit.subreddit("stock+wallstreetbets+investing").search(company, time_filter = 'month'):
            submission_obj = RedditSubmissionObject(company, {"title": submission.title, "date_created": submission.created_utc, "text": submission.selftext})
            submission_dict_collection.append(submission_obj)

        return submission_dict_collection

            



if __name__ == '__main__':
    RedditInterface.get_all_submissions_for('AAPL')
    