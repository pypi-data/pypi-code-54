import dateutil.parser
from .base_datatype_mapper import BaseDatatypeMapper
from datetime import datetime, timezone

class DatetimeMapper(BaseDatatypeMapper):
    def resolve(self, value):
        """Convert the datetime into an ISO 8601 string

        All DynamoDB datetimes must be shifted to UTC
        https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.DataTypes.html
        """
        return value.replace(tzinfo=timezone.utc).isoformat()

    def parse(self, value):
        """Parse the datetime string

        Since it uses dateutil.parser, this should handle both
        ISO 8601 strings and timezone agnostic values, however
        if the record was creating using the resolve() method, a
        utc timezone should automatically be included
        """
        return dateutil.parser.parse(value)
