from sample_data_generator.models import MeterReading
from sample_data_generator.dao.base import MeterReadingDaoBase
from sample_data_generator.dao.redis import CapacityReportDaoRedis
from sample_data_generator.dao.redis import FeedDaoRedis
from sample_data_generator.dao.redis import MetricDaoRedis
from sample_data_generator.dao.redis import SiteStatsDaoRedis
from sample_data_generator.dao.redis.base import RedisDaoBase


class MeterReadingDaoRedis(MeterReadingDaoBase, RedisDaoBase):
    """MeterReadingDaoRedis persists MeterReading models to Redis."""
    def add(self, meter_reading: MeterReading, **kwargs) -> None:
        MetricDaoRedis(self.redis, self.key_schema).insert(meter_reading, **kwargs)
        SiteStatsDaoRedis(self.redis, self.key_schema).update(meter_reading, **kwargs)
        CapacityReportDaoRedis(self.redis, self.key_schema).update(meter_reading, **kwargs)
        FeedDaoRedis(self.redis, self.key_schema).insert(meter_reading, **kwargs)
