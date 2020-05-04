import logging
from typing import Iterable, Tuple

import aiohttp
from asgiref.sync import async_to_sync

from appel_crises.settings import MTCAPTCHA_PRIVATE_KEY, DEBUG

MTCAPTCHA_URL = "https://service.mtcaptcha.com/mtcv1/api/checktoken"

_logger = logging.getLogger(__name__)


@async_to_sync
async def verify_captcha(token: str) -> Tuple[bool, Iterable[str]]:
    """
    Validate the token against MTCaptcha API.

    :param token: the token sent by the user
    :return: if the token is valid, and if not, a list of reasons why
    """
    if len(token) == 0:
        return False, ("No token provided",)

    if DEBUG:
        _logger.info("Don't check captcha in debug mode. ('%s' is ok for now)", token)
        return True, ()

    params = dict(privatekey=MTCAPTCHA_PRIVATE_KEY, token=token)

    async with aiohttp.ClientSession() as session:
        async with session.get(MTCAPTCHA_URL, params=params) as resp:
            if resp.status < 400:
                data = await resp.json()
                success = data["success"]
                if success:
                    return True, ()
                else:
                    return False, data["fail_codes"]
            else:
                _logger.error(
                    "Error while validating captcha token", resp.status, resp.text()
                )
                return True, ()
