# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypika_gis']

package_data = \
{'': ['*'], 'pypika_gis': ['.pytest_cache/*', '.pytest_cache/v/cache/*']}

install_requires = \
['PyPika<1.0.0']

setup_kwargs = {
    'name': 'pypika-gis',
    'version': '1.3.0',
    'description': 'SpatialTypes functions for extend PyPika with GIS',
    'long_description': '# pypika-gis\n\nSpatialTypes functions for extend [PyPika](https://github.com/kayak/pypika) with GIS.\n\n## Install\n\n```bash\npip install pypika-gis\n```\n\n## Example\n\n```python\nfrom pypika import Query\nfrom pypika_gis import spatialtypes as st\n\nquery = Query.from_(\'field\').select(\'id\', st.AsGeoJSON(\'geom\'))\nprint(str(query))\n# SELECT "id",ST_AsGeoJSON(\'geom\') FROM "field"\n\nquery = Query.from_(\'crop\').select(\'id\').where(st.Intersects(\'geom\', st.SetSRID(st.MakePoint(10, 5), 4326)))\nprint(str(query))\n# SELECT "id" FROM "crop" WHERE ST_Intersects(\'geom\',ST_SRID(ST_MakePoint(10,5),4326))\n```\n\n## Available functions\n\n- Area(ST_Area)\n- AsBinary(ST_AsBinary)\n- AsGeoJSON(ST_AsGeoJSON)\n- AsMVT(ST_AsMVT)\n- AsText(ST_AsText)\n- Boundary(ST_Boundary)\n- Buffer(ST_Buffer)\n- Centroid(ST_Centroid)\n- ClosestPoint(ST_ClosestPoint)\n- Contains(ST_Contains)\n- CoveredBy(ST_CoveredBy)\n- Covers(ST_Covers)\n- Difference(ST_Difference)\n- Dimension(ST_Dimension)\n- Disjoint(ST_Disjoint)\n- Distance(ST_Distance)\n- DWithin(ST_DWithin)\n- Equals(ST_Equals)\n- Envelope(ST_Envelope)\n- Extent(ST_Extent)\n- GeoHash(ST_GeoHash)\n- GeogFromGeoJSON(ST_GeogFromGeoJSON)\n- GeogFromText(ST_GeogFromText)\n- GeogFromWKB(ST_GeogFromWKB)\n- GeogPoint(ST_GeogPoint)\n- GeogPointFromGeoHash(ST_GeogPointFromGeoHash)\n- GeomFromGeoJSON(ST_GeomFromGeoJSON)\n- Intersections(ST_Intersection)\n- Intersects(ST_Intersects)\n- IsCollection(ST_IsCollection)\n- IsEmpty(ST_IsEmpty)\n- IsValid(ST_IsValid)\n- Length(ST_Length)\n- MakeLine(ST_MakeLine)\n- MakePoint(ST_MakePoint)\n- MakePolygon(ST_MakePolygon)\n- NumPoints(ST_NumPoints)\n- Perimeter(ST_Perimeter)\n- Point(ST_Point)\n- SetSRID(ST_SetSRID)\n- Touches(ST_Touches)\n- Union(ST_Union)\n- Within(ST_Within)\n- X(ST_X)\n- Y(ST_Y)\n- Z(ST_Z)\n\n## Development\n\n### Dependencies\n\n- [Python](https://www.python.org/downloads/)\n- [poetry](https://poetry.eustace.io/)\n\n### Setup\n\n```bash\npoetry install\n```\n\n### Tests\n\nFull tests and coverage\n\n```bash\npoetry run pytest\n```\n\n### Publish\n\n```bash\npoetry build\npoetry publish\n```\n\n## Credits\n\npypika-gis is based on [PyPika](https://github.com/kayak/pypika). Check their page for further query buider instructions, examples and more details about PyPika core.\n',
    'author': 'Eduardo G. S. Pereira',
    'author_email': 'edu_vcd@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eduardogspereira/pypika-gis',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
