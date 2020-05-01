import geohash as gh
import shapely.geometry
import geopandas
from polygon_geohasher.polygon_geohasher import geohashes_to_polygon
import json

def geohash_to_geojson(geohashes):
	geojson = []
	for i in range(0,len(geohashes)):
		geojson.append(geopandas.GeoSeries([geohashes_to_polygon([geohashes[i]])]).to_json())
	d = json.loads(geojson[0])
	for i in range(1,len(geojson)):
		data=json.loads(geojson[i])
		feature = {}
		feature["type"] = "Feature"
		feature["properties"] = {"id":geohashes[i]}
		feature["geometry"] = {"type": "Polygon","coordinates":data['features'][0]['geometry']['coordinates'] ,}
		d['features'].append(feature)
	y = json.dumps(d)
	return y
