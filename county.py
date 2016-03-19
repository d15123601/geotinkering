"""
This code creates a dict for each county of the populated towns in each county, using shapely function 'contains'
to establish the relationship.
It then finds the centroid of the county and determines which of the towns is nearest to it, and stores it in a dictionary.
"""

from geo_utils import get_data_from_geoserver, proj_point
from fiona import collection
from fiona.crs import from_epsg
import fiona
from shapely import geometry
import pyproj
import geopy
from shapely.geometry import asShape
import collections
import os

SERVER = "mf2.dit.ie:8080"
DBASE1 = 'geonames_pop_5000'
DBASE2 = "cso:ctygeom"
OUTPUT_DIR = '.cache'
countytowns = collections.defaultdict(list)
countycents = collections.defaultdict(str)
county_town ={}

places = get_data_from_geoserver(SERVER, DBASE1)
places_list = []

for feature in places['features']:
    point = geometry.Point(float(feature['geometry']['coordinates'][0]), float(feature['geometry']['coordinates'][1]))
    place_name = feature['properties']['name']
    pop = feature['properties']['population']
    places_list.append([point, place_name, pop])


counties = get_data_from_geoserver(SERVER, DBASE2)
for county in counties['features']:
    geom = geometry.MultiPolygon(asShape(county['geometry']))
    name = county['properties']['countyname']
    c = (geom.centroid)
    countycents[name] = c
    for town in places_list:
        if geom.contains(town[0]):
            countytowns[county['properties']['countyname']].append([town[1],town[0]])

for k, v in countytowns.items():
        dist = {t[0]: t[1].distance(countycents[k]) for t in v}
        if len(dist) != 1:
            county_town[k] = min(zip(dist.values(), dist.keys()))[1]
        else: county_town[k] = v[0][0]

crs_from = pyproj.Proj("+init=EPSG:4326")
crs_to = pyproj.Proj("+init=EPSG:")

for k, v in countycents.items():
    proj_point()

