import logging

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from config import constants as const
from api.api_extract_feeds import blueprint as api_text
from utils.loggers import config_logging


app = Flask(__name__)

swagger_url = const.ENDPOINT_SWAGGER
swagger_ui_api_text = get_swaggerui_blueprint(base_url=swagger_url,
                                              api_url=f"{const.ENDPOINT_API}/swagger.json",
                                              blueprint_name=const.NAME_BLUEPRINT)

app.register_blueprint(api_text)
app.register_blueprint(swagger_ui_api_text, url_prefix=swagger_url)

config_logging()
logger = logging.getLogger('main')

if __name__ == '__main__':
	app.run()
