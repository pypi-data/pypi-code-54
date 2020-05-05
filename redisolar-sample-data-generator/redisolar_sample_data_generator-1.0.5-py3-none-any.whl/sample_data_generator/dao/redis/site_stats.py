import datetime

import redis.client

from sample_data_generator.dao.base import SiteStatsDaoBase
from sample_data_generator.dao.redis import key_schema
from sample_data_generator.dao.redis.base import RedisDaoBase
from sample_data_generator.models import MeterReading
from sample_data_generator.models import SiteStats
from sample_data_generator.schema import SiteStatsSchema
from sample_data_generator.scripts import CompareAndUpdateScript

WEEK_SECONDS = 60 * 60 * 24 * 7


class SiteStatsNotFound(Exception):
    """A SiteStats model was not found for the given query."""


class SiteStatsDaoRedis(SiteStatsDaoBase, RedisDaoBase):
    """SiteStatsDaoRedis persists SiteStats models to Redis.

    This class is a pluggable service that allows persisting (and
    querying for) SiteStats in Redis.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.compare_and_update_script = CompareAndUpdateScript(self.redis)

    def find_by_id(self,
                   site_id: int,
                   day: datetime.datetime = None,
                   **kwargs) -> SiteStats:
        if day is None:
            day = datetime.datetime.now()

        key = self.key_schema.site_stats_key(site_id, day)
        fields = self.redis.hgetall(key)

        if not fields:
            raise SiteStatsNotFound()

        return SiteStatsSchema().load(fields)

    def update(self, meter_reading: MeterReading, **kwargs) -> None:
        key = self.key_schema.site_stats_key(meter_reading.site_id,
                                        meter_reading.timestamp)
        pipeline = kwargs.get('pipeline')

        if pipeline is not None:
            self._update(key, meter_reading, pipeline)
            return

        with self.redis.pipeline() as p:
            self._update(key, meter_reading, p)
            p.execute()

    def _update(self, key: str, reading: MeterReading,
                pipeline: redis.client.Pipeline) -> None:
        reporting_time = datetime.datetime.utcnow().isoformat()

        pipeline.hset(key, SiteStats.LAST_REPORTING_TIME, reporting_time)
        pipeline.hincrby(key, SiteStats.COUNT, 1)
        pipeline.expire(key, WEEK_SECONDS)

        self.compare_and_update_script.update_if_greater(
            pipeline, key, SiteStats.MAX_WH, reading.wh_generated)
        self.compare_and_update_script.update_if_less(
            pipeline, key, SiteStats.MIN_WH, reading.wh_generated)
        self.compare_and_update_script.update_if_greater(
            pipeline, key, SiteStats.MAX_CAPACITY, reading.current_capacity)

