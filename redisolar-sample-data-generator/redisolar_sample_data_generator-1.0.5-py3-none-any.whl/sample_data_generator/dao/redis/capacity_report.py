from sample_data_generator.dao.base import CapacityDaoBase
from sample_data_generator.dao.redis import key_schema
from sample_data_generator.dao.redis.base import RedisDaoBase
from sample_data_generator.models import CapacityReport
from sample_data_generator.models import MeterReading
from sample_data_generator.models import SiteCapacityTuple


class CapacityReportDaoRedis(CapacityDaoBase, RedisDaoBase):
    """
    CapacityReportDaoRedis persists CapacityReport models to Redis.

    This class is a pluggable service that allows persisting (and
    querying for) CapacityReports in Redis.
    """
    def update(self, meter_reading: MeterReading, **kwargs) -> None:
        capacity_ranking_key = self.key_schema.capacity_ranking_key()
        pipeline = kwargs.get('pipeline')
        client = pipeline if pipeline is not None else self.redis
        client.zadd(capacity_ranking_key,
                    {meter_reading.site_id: meter_reading.current_capacity})

    def get_report(self, limit: int, **kwargs) -> CapacityReport:
        capacity_ranking_key = self.key_schema.capacity_ranking_key()
        with self.redis.pipeline() as p:
            p.zrange(capacity_ranking_key, 0, limit - 1, withscores=True)
            p.zrevrange(capacity_ranking_key, 0, limit - 1, withscores=True)
            low_capacity, high_capacity = p.execute()

        low_capacity_list = [
            SiteCapacityTuple(capacity=v[0], site_id=v[1])
            for v in low_capacity
        ]
        high_capacity_list = [
            SiteCapacityTuple(capacity=v[0], site_id=v[1])
            for v in high_capacity
        ]

        return CapacityReport(high_capacity_list, low_capacity_list)

    # Challenge 6
    def get_rank(self, site_id: int, **kwargs) -> float:
        capacity_ranking_key = self.key_schema.capacity_ranking_key()
        return self.redis.zrevrank(capacity_ranking_key, site_id)
