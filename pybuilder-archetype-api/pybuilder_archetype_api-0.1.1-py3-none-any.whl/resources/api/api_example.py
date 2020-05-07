# -*- coding: utf-8 -*-
from flask import Blueprint
from flask_restplus import Api

from config import constants as const


blueprint = Blueprint(name=const.NAME_API, import_name=__name__, url_prefix=const.ENDPOINT_API)
api = Api(blueprint,
          title=const.TITLE_API,
          version=const.VERSION_API,
          description=const.DESCRIPTION_API)

# TODO import namespace implementation
# api.add_namespace(namespace, path=const.END_POINT_PATH)
