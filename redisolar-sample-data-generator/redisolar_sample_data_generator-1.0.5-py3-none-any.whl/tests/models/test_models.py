from dataclasses import dataclass

from sample_data_generator.schema import FlatSiteSchema
from sample_data_generator.models.models import Coordinate
from sample_data_generator.models.models import Site


def test_site_schema_loads_coordinate():
    site = Site(id=1,
                capacity=1,
                panels=1,
                address="Somewhere",
                city="Portland",
                state="OR",
                postal_code="97201",
                coordinate=Coordinate(lat=1.0, lng=1.1))
    json = {
        "id": 1,
        "capacity": 1,
        "panels": 1,
        "address": "Somewhere",
        "city": "Portland",
        "state": "OR",
        "postal_code": "97201",
        "lat": 1,
        "lng": 1.1
    }
    assert FlatSiteSchema().load(json) == site


def test_site_schema_dumps_coordinate():
    site = Site(id=1,
                capacity=1,
                panels=1,
                address="Somewhere",
                city="Portland",
                state="OR",
                postal_code="97201",
                coordinate=Coordinate(lat=1.0, lng=1.1))
    json = {
        "id": 1,
        "capacity": 1,
        "panels": 1,
        "address": "Somewhere",
        "city": "Portland",
        "state": "OR",
        "postal_code": "97201",
        "lat": 1,
        "lng": 1.1
    }
    assert FlatSiteSchema().dump(site) == json
