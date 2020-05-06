from http import HTTPStatus
from typing import List, Dict

import requests
from shuttlis.serialization import serialize

from ats_sdk.error import ClientError
from ats_sdk.translation import fetch_translatable_strings, translate


class AlternateTextService:
    def __init__(self, url: str):
        self._url = url

    def translate_and_serialize(self, resource: Dict, locale: str):
        translatable_strings = set(fetch_translatable_strings(resource=resource))

        translated_strings = self.get_static_translation(
            locale=locale, keys=list(translatable_strings)
        )

        return serialize(
            translate(resource=resource, translated_strings=translated_strings)
        )

    def get_static_translation(self, locale: str, keys: List[str]):
        response = requests.get(
            f"{self._url}/api/v1/translate/static",
            params={"locale": locale, "keys": ",".join(keys)},
        )
        if response.status_code != HTTPStatus.OK:
            raise ClientError(response.text)

        return response.json()["data"]
