""" Here we access geojson held in a textfile - it is then used to perform the
    following tasks reqd for the GIS programming assignment..... see the 'ni' file
    to use code which accesses the geoserver.

    Specifically, we want to do the following:

    Create a single polygon from the Union of all the polygons.
    Compute the centroid of the single polygon.
    Extract the points that lie within the single polygon.
    Compute a convex hull and centroid for the extracted points
    Compute the distance between the centroid of the single polygon and the centroid of the points that lie within the single polygon.
    Create a representation of the line joining the two centroids
    Geocode both centroids and add their names to the appropriate point as an attribute
    Create shapefiles to store the results of the above. Bear in mind that a shapefile contains a single geometry type and is a set of thematically related features. Therefore you will need to create shapefiles as follows:
    Combined polygon from Union
    Points that lie within Combined Polygon
    Convex hull of the points from above
    Both centroids. Each should have an attribute to hold its name returned from the geocoding process.
    Linestring representing the distance between the centroids

"""


from geo_utils import *

from fiona import collection
from fiona.crs import from_epsg
import fiona
from shapely import geometry
import pyproj
import geopy
from shapely.geometry import asShape
from shapely.ops import cascaded_union
import collections
import os
import json

#   Variable assignment or initialisation
json_fldr = r"C:\Users\mickle\Google Drive\College\Python\MarkFoley"
countycents = collections.defaultdict(str)
poly_geoms = []
pt_geoms = []


with open(os.path.join(json_fldr, "cso_counties.txt"),'r') as f1:
    cty_str = f1.read()

with open(os.path.join(json_fldr, "geonames_pop.txt"),'r') as f2:
    pop_str = f2.read()

cty_polygons = json.loads(cty_str)
places_pts = json.loads(pop_str)

for county in cty_polygons['features']:
    geom = geometry.MultiPolygon(asShape(county['geometry']))
    poly_geoms.append(geom)

merged_counties = cascaded_union(poly_geoms)

#   Filter the point data so that we only pick pts with a population > 8000,
#   add the geoms to a list

for place in places_pts['features']:
    if place['properties']['population'] > 8000:
        geom = geometry.Point(asShape(place['geometry']))
        pt_geoms.append(geom)

#   Find out how many points lie within the unioned polygon



print("The number of places with pops > 8000 is {}".format(len(pt_geoms)))





print(merged_counties.area)
print(merged_counties.centroid)

print('hi')