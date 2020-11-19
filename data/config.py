from configparser import ConfigParser

config = ConfigParser()

config.read("config.ini")

reddit_id = config.get('RedditAPI', 'id')
reddit_secret = config.get('RedditAPI', 'secret')
reddit_user = config.get('RedditAPI', 'user')
reddit_pass = config.get('RedditAPI', 'pass')
reddit_user_agent = config.get('RedditAPI', 'user_agent')

iexcloud_url = config.get('IEXCloud', 'url')
iexcloud_key = config.get('IEXCloud', 'key')
