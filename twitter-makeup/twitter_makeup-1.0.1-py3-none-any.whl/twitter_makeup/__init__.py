import tweepy


class MakeUp:

    def __init__(self, api: tweepy.API):
        self.api = api

    def change_banner_picture(self, filepath):
        self.api.update_profile_banner(filepath)

    def change_profile_picture(self, filepath):
        self.api.update_profile_image(filepath)

    def change_profile_name(self, display_name):
        self.api.update_profile(name=display_name)

    def change_profile_location(self, location):
        self.api.update_profile(location=location)

    def change_profile_description(self, description):
        self.api.update_profile(description=description)
