"""
Wrapper for retrieving configurations and safely logging their retrieval
"""
import json
import os
import re
from typing import Callable, Any

from logging42 import logger


class Required:
    pass


class ConfigurationValue(str):
    """

    """

    def __init__(self, value):
        super().__init__()
        self.value = value

    def json(self, **kwargs):
        return json.loads(str(self), **kwargs)

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


class ConfigurationRetriever:
    """

    """

    def __init__(
        self,
        retriever: Callable[[str, Any], str] = os.environ.get,
        secrets: tuple = ("password", "pass", "secret", "token"),
    ):
        self.retriever = retriever
        self.secrets = secrets
        self.configs = {}

    def __call__(self, key, default=Required) -> ConfigurationValue:
        value = self._retrieve_configuration(key, default)
        self.configs = {**self.configs, key: value}
        return ConfigurationValue(value)

    def _retrieve_configuration(self, k, default) -> Any:
        value = self.retriever(k, default)
        if value is Required:
            raise ValueError(f"Configuration value for {k} is required.")
        is_default = value == default
        logger.debug(f"Retrieved value for {k}. is_default={is_default}")
        return value

    def is_secret(self, k: str):
        pattern = "|".join([f"({s.upper()})" for s in self.secrets])
        return bool(re.findall(pattern, k.upper()))

    def __str__(self):
        s = ", ".join(
            [
                f"{k}: <CENSORED>" if self.is_secret(k) else f"{k}: {v}"
                for k, v in self.configs.items()
            ]
        )
        return s

    def log_configs(self):
        logger.info(f"Retrieved configurations: {str(self)}")
