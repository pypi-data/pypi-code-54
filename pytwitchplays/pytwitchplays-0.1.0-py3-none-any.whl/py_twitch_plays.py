from datetime import datetime, timedelta

from pytwitchchat import TwitchChatClient


class TwitchPlays:
    def __init__(self, password, username, channel, actions):
        self.TWITCH_CHAT_CLIENT = TwitchChatClient(password, username, channel, self.handle)
        self.ACTIONS = actions
        self.active_chatters = {}

    def run(self):
        self.TWITCH_CHAT_CLIENT.connect()
        self.TWITCH_CHAT_CLIENT.run()

    def handle(self, message, user, is_mod):
        self.active_chatters = {
            k: v for k, v in self.active_chatters.items() if v > (datetime.now() - timedelta(minutes=1))
        }
        self.active_chatters[user] = datetime.now()
        if message.lower() in self.ACTIONS:
            self.ACTIONS[message.lower()].run(user, self)
