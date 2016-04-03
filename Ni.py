from geo_utils import *

from fiona import collection
from fiona.crs import from_epsg
import fiona
from shapely import geometry
import pyproj
import geopy
from shapely.geometry import asShape
import collections
import os

PARAMS1 = {
    "host": "mf2.dit.ie:8080",
    "layer": "cso:ctygeom",
    "srs_code": 29902,
    "properties": ["countyname", ],
    "geom_field": "geom",
    "filter_property": "countyname",
    "filter_values": []
}

PARAMS2 = {
    "host": "mf2.dit.ie:8080",
    "layer": "dit:geonames_populated",
    "srs_code": 29902,
    "properties": [],
    "geom_field": "geom",
    "filter_property": "countyname",
    "filter_values": []
}

polygons = get_geojson(PARAMS1)
points = get_geojson(PARAMS2)


