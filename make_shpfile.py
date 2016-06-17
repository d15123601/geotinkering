"""
This is for taking a json file and putting it into a shapefile.
It uses the generic functions written by mfoley.
"""

from geo_utils import get_data_from_geoserver
import json
import six
from fiona import collection
import pyproj
from shapely.geometry import Point, mapping


op_file = "museums.shp"

server = "mf2.dit.ie:8080"
dbase = "dit:dublin_museums"

crs_from = pyproj.Proj("+init=EPSG:4326")
crs_to = pyproj.Proj("+init=EPSG:2157")

museums = get_data_from_geoserver(server, dbase)
pts = {}

for place in museums['features']:
    pts[place['properties']['name']] = (place['geometry']['coordinates'])

schema = { 'geometry': 'Point', 'properties': { 'name': 'str' } }
with collection(
    op_file, "w", "ESRI Shapefile", schema) as output:
    for k, v in pts.items():
        x, y = pyproj.transform(crs_from, crs_to, v[0], v[1])
        point = Point(x, y)
        output.write({'properties': {'name': k},'geometry': mapping(point)})


def make_a_shapefile(source, *dest):
    if isinstance(source, dict) and source["type"] == "FeatureCollection":
        print('This is a FC')

    if len(source["features"]):
        print('There is gj_stack')

    if isinstance(source, list):
        pass










