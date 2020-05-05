import datetime
import random
from typing import List

import redis.client

from sample_data_generator.models import MeterReading
from sample_data_generator.dao.redis import MeterReadingDaoRedis


class SampleDataGenerator:
    """
    Generates historical data for all sites starting from the
    current time and going back in time for the requested number
    of days. The max number of permissible days is 365.
    """
    SEED = 42
    MAX_TEMPERATURE_C = 30.0

    def __init__(self, redis, sites, days, key_schema):
        if days < 0 or days > 365:
            raise ValueError(f"Invalid days {days} for historical request")

        self.redis = redis
        self.sites = sites
        self.minute_days = days * 3 * 60
        self.key_schema = key_schema
        self.readings = self._generate_readings(days)

    def _get_max_minute_wh_generated(self, capacity: float) -> float:
        return capacity * 1000 / 24 / 60

    def _get_initial_minute_wh_used(self, max_capacity: float) -> float:
        if random.uniform(0, 1) > 0.5:
            return max_capacity + 0.1
        return max_capacity - 0.1

    def _get_next_value(self, maximum: float, current: float = None):
        if current is None:
            current = maximum

        step_size = 0.1 * maximum

        if random.choice([True, False]):
            return current + step_size
        if current - step_size < 0.0:
            return 0.0

        return current - step_size

    def _generate_readings(self, days: int) -> List[List[int]]:
        return [[0 for x in range(self.minute_days)] for y in range(len(self.sites))]

    @property
    def size(self):
        """The total number of readings."""
        return self.minute_days * len(self.sites)

    def generate(self, pipeline: redis.client.Pipeline):
        meter_reading_service = MeterReadingDaoRedis(self.redis, self.key_schema)

        for site in self.sites:
            max_capacity = self._get_max_minute_wh_generated(site.capacity)
            current_capacity = self._get_next_value(max_capacity)
            current_temperature = self._get_next_value(self.MAX_TEMPERATURE_C)
            current_usage = self._get_initial_minute_wh_used(max_capacity)
            current_time = datetime.datetime.utcnow() - datetime.timedelta(
                minutes=self.minute_days)

            for i in range(self.minute_days):
                reading = MeterReading(site_id=site.id,
                                       timestamp=current_time,
                                       wh_used=current_usage,
                                       wh_generated=current_capacity,
                                       temp_c=current_temperature)

                self.readings[site.id - 1][i] = reading

                current_time = current_time + datetime.timedelta(minutes=1)
                current_temperature = self._get_next_value(current_temperature)
                current_capacity = self._get_next_value(current_capacity)
                current_usage = self._get_next_value(current_usage)

        for i in range(self.minute_days):
            for j in range(len(self.sites)):
                reading = self.readings[j][i]
                meter_reading_service.add(reading, pipeline=pipeline)
                yield reading
