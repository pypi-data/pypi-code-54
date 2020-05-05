from typing import List

import redis.client

from sample_data_generator.dao.base import FeedDaoBase
from sample_data_generator.dao.redis import key_schema
from sample_data_generator.dao.redis.base import RedisDaoBase
from sample_data_generator.models import MeterReading
from sample_data_generator.schema import MeterReadingSchema


class FeedDaoRedis(FeedDaoBase, RedisDaoBase):
    def insert(self, meter_reading: MeterReading, **kwargs) -> None:
        pipeline = kwargs.get('pipeline')

        if pipeline is not None:
            self._insert(meter_reading, pipeline)
        else:
            with self.redis.pipeline() as p:
                self._insert(meter_reading, p)
                p.execute()

    def _insert(self, meter_reading: MeterReading,
                pipeline: redis.client.Pipeline) -> None:
        global_key = self.key_schema.global_feed_key()
        site_key = self.key_schema.feed_key(meter_reading.site_id)
        serialized_meter_reading = MeterReadingSchema().dump(meter_reading)
        pipeline.xadd(global_key, serialized_meter_reading)
        pipeline.xadd(site_key, serialized_meter_reading)

    def get_recent_global(self, limit: int, **kwargs) -> List[MeterReading]:
        return self.get_recent(self.key_schema.global_feed_key(), limit)

    def get_recent_for_site(self, site_id: int,
                            limit: int, **kwargs) -> List[MeterReading]:
        return self.get_recent(self.key_schema.feed_key(site_id), limit)

    def get_recent(self, key: str, limit: int) -> List[MeterReading]:
        return [
            MeterReadingSchema().load(entry[1])
            for entry in self.redis.xrevrange(key, count=limit)
        ]
