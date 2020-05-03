import logging
import re

from connexion import App as ConnexionApp
from flask import Flask
from ultra_config import GlobalConfig

__all__ = ["FlaskConnexionExtension"]
LOG = logging.getLogger(__name__)
UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


class FlaskConnexionExtension:
    app: Flask
    connexion_app: ConnexionApp

    def init_app(self, connexion_app: ConnexionApp) -> Flask:
        self.connexion_app = connexion_app
        self.app = self.connexion_app.app
        return self.app

    @GlobalConfig.inject(
        strict_validation="SCHEMA_VALIDATION_STRICT",
        validate_responses="SCHEMA_VALIDATION_VALIDATE_RESPONSES",
    )
    def add_api(
        self,
        swagger_file: str,
        strict_validation: bool = True,
        validate_responses: bool = False,
        **kwargs
    ):
        return self.connexion_app.add_api(
            swagger_file,
            strict_validation=strict_validation,
            validate_responses=validate_responses,
            **kwargs
        )
