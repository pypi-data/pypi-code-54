#!/usr/bin/env python

__author__ = 'Dan Conger <dconger2@gmail.com>'
__version__ = '0.1.0'

from airflow.plugins_manager import AirflowPlugin
from dan_airflow_plugins.operators.dan_operator import (
    DanOperator
)

__all__ = [
    'DanPlugin',
    'DanOperator'
]

# Plugin
class DanPlugin(AirflowPlugin):
    name = 'dan_airflow_plugins'
    operators = [
        DanOperator
    ]
    flask_blueprints = []
    hooks = []
    executors = []
    admin_views = []
    menu_links = []
    appbuilder_views = []
