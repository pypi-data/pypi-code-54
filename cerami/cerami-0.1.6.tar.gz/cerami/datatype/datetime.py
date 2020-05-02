import dateutil.parser
from datetime import datetime, timezone
from .base_string import BaseString
from .mapper import DatetimeMapper

class Datetime(BaseString):
    def __init__(self, mapper_cls=DatetimeMapper, **kwargs):
        super(Datetime, self).__init__(mapper_cls=mapper_cls, **kwargs)
