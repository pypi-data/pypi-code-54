from pathlib import Path

from vkbottle import User, Message
import dotenv
from vkbottle.framework import Middleware

nicevk_folder = Path.home().joinpath("nicevk").absolute()

env = dotenv.dotenv_values(str(nicevk_folder.joinpath(".env")))

user = User(env["TOKEN"])

commands = [".help"]


@user.middleware.middleware_handler()
class NoBotMiddleware(Middleware):
    async def middleware(self, message: Message):
        if message.from_id == (await message.api.users.get())[0].id:
            return True
        else:
            return False
