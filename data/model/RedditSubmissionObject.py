class RedditSubmissionObject:
    def __init__(self, company, payload):
        self.company = company
        self.title = payload['title']
        self.date_created = payload['date_created']
        self.text = payload['text']

