from typing import Set

from sample_data_generator.models import Site
from sample_data_generator.dao.base import SiteDaoBase
from sample_data_generator.dao.redis.base import RedisDaoBase
from sample_data_generator.schema import FlatSiteSchema


class SiteDaoRedis(SiteDaoBase, RedisDaoBase):
    """SiteDaoRedis persists Site models to Redis.

    This class is a pluggable service that allows persisting (and
    querying for) Sites in Redis.
    """
    def insert(self, site: Site, **kwargs):
        """Insert a Site into Redis."""
        hash_key = self.key_schema.site_hash_key(site.id)
        site_ids_key = self.key_schema.site_ids_key()
        pipeline = kwargs.get('pipeline')
        client = pipeline if pipeline is not None else self.redis
        client.hset(hash_key, mapping=FlatSiteSchema().dump(site))
        client.sadd(site_ids_key, hash_key)

    def insert_many(self, *sites: Site, **kwargs) -> None:
        for site in sites:
            self.insert(site, **kwargs)

    def find_by_id(self, site_id: int, **kwargs) -> Site:
        """Find a Site by ID in Redis."""
        hash_key = self.key_schema.site_hash_key(site_id)
        site_hash = self.redis.hgetall(hash_key)
        return FlatSiteSchema().load(site_hash)

    def find_all(self, **kwargs) -> Set[Site]:
        """Find all Sites in Redis."""
        site_ids_key = self.key_schema.site_ids_key()
        site_keys = self.redis.smembers(site_ids_key)
        sites = set()

        for site_key in site_keys:
            site_hash = self.redis.hgetall(site_key)
            site_model = FlatSiteSchema().load(site_hash)
            sites.add(site_model)

        return sites
