import tweepy

class MakeUp:

    def __init__(self, api: tweepy.API):
        self.api = api

    def change_banner_picture(self, filepath):
        self.api.update_profile_banner(filepath)
