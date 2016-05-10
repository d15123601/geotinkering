import os
import psycopg2
import fiona
from fiona.crs import from_epsg
import shapely.geometry as sg
from shapely.ops import cascaded_union
from shapely.geometry import asShape, mapping, MultiPoint, LineString
import geopy
from geopy.geocoders import Nominatim
import pyproj
import json
from geo_utils import *


polygons = {
    "host": "mf2.dit.ie:8080",
    "layer": "cso:counties",
    "srs_code": 29902,
    "properties": ["countyname"],
    "geom_field": "geom",
    "filter_property": "countyname",
    "filter_values": ["Laois", "Kildare"]
}

points = {
    "host": "mf2.dit.ie:8080",
    "layer": "dit:geonames_pop_5000",
    "srs_code": 29902,
}

# Converts json (MultiPolygon) file into Shapely geometry
def convert_polygons_json(poly_geojson):
    shapes = []

    for geom in poly_geojson['features']:
        shape = sg.asShape(geom['geometry'])
        shapes.append(shape)
    return shapes

# Converts json (Points) file into Shapely geometry
def convert_points_json(point_geojson):
    points = []

    for geom in point_geojson['features']:
        shape = sg.asShape(geom['geometry'])
        points.append(shape)
    return points

# Spatial operations
def spatial_operations(county_polygons, urban_points):
    combined_polys = [] # ** delete this, it's not used
    combined_polygons = cascaded_union(county_polygons)
    combined_polygons_centroid = combined_polygons.centroid

    combined_points =[]
    for point in urban_points:
        if point.within(combined_polygons):
             combined_points.append(point)

    points = MultiPoint(combined_points)
    convex_hull = points.convex_hull
    convex_hull_centroid = convex_hull.centroid

    dist_between_centroids = convex_hull_centroid.distance(combined_polygons_centroid)
    line_centroids = LineString([convex_hull_centroid,combined_polygons_centroid])

    return [combined_polygons,combined_polygons_centroid,combined_points,convex_hull,convex_hull_centroid,line_centroids]

# Defines schema and with Fiona creates new SHP
def single_polygon_shp(spatial_results):
    # Define a polygon feature geometry with one attribute id
    schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
    }

    # Creates new Shapefile
    with fiona.open('./single_polygon.shp', 'w', 'ESRI Shapefile', schema) as output:
        ## If there are multiple geometries, put the "for" loop here
        output.write({
            'geometry': mapping(spatial_results),
            'properties': {'id': 123},
        })
    return

# Defines schema and with Fiona creates new SHP
def single_polygon_centroid_shp(spatial_results):
    # Define a polygon feature geometry with one attribute id
    schema = {
        'geometry': 'Point',
        'properties': {'id': 'int'},
    }

    # Creates point Shapefile (SHP)
    with fiona.open('./polygon_centroid.shp', 'w', 'ESRI Shapefile', schema) as output:
        ## If there are multiple geometries, put the "for" loop here
        output.write({
            'geometry': mapping(spatial_results),
            'properties': {'id': 1234},
        })
    return

# Defines schema and with Fiona creates new SHP
def urban_points_shp(spatial_results):
    # Define a polygon feature geometry with one attribute id
    schema = {
        'geometry': 'Point',
        'properties': {'id': 'int'},
    }

    # Creates town points Shapefile (SHP)
    with fiona.open('./cities_points.shp', 'w', 'ESRI Shapefile', schema) as output:
        for point in spatial_results:
            output.write({
                'geometry': mapping(point),
                'properties': {'id': 1234},
            })
    return

# Defines schema and with Fiona creates new SHP
def convex_hull_shp(spatial_results):
    # ** my_crs = spatial_results['crs]
    # Define a polygon feature geometry with one attribute
    schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
    }

    # Creates convex hull polygon from town points - Shapefile (SHP)
    with fiona.open('./convex_hull.shp', 'w', 'ESRI Shapefile', schema) as output:
    # ** replace the above, possibly like this
    # ** with fiona.open('./convex_hull.shp', 'w', 'ESRI Shapefile', schema, crs = from_epsg(29902)) as output:
    # ** or like this if you want to dynamically assign the crs from the shape dict
    # ** with fiona.open('./convex_hull.shp', 'w', 'ESRI Shapefile', schema, crs = from_epsg(my_crs)) as output:
        ## If there are multiple geometries, put the "for" loop here
        output.write({
            'geometry': mapping(spatial_results),
            'properties': {'id': 123},
        })
    return

# Defines schema and with Fiona creates new SHP
def convex_hull_centroid_shp(spatial_results):
    # Define a polygon feature geometry with one attribute
    schema = {
        'geometry': 'Point',
        'properties': {'id': 'int'},
    }

    # Creates centroid (point) of convex hull polygon - Shapefile (SHP)
    with fiona.open('./convex_centroid.shp', 'w', 'ESRI Shapefile', schema) as output:
        ## If there are multiple geometries, put the "for" loop here
        output.write({
            'geometry': mapping(spatial_results),
            'properties': {'id': 123},
        })
    return

# Defines schema and with Fiona creates new SHP
def line_between_centroids_shp(spatial_results):
    # Define a polygon feature geometry with one attribute
    schema = {
        'geometry': 'LineString',
        'properties': {'id': 'int'},
    }

    # Creates a line between convex hull centroid and combined polygons centroid - Shapefile (SHP)
    with fiona.open('./line_centroids.shp', 'w', 'ESRI Shapefile', schema) as output:
        ## If there are multiple geometries, put the "for" loop here
        output.write({
            'geometry': mapping(spatial_results),
            'properties': {'id': 123},
        })
    return

def main():
    poly_geojson = get_geojson(polygons)
    point_geojson = get_geojson(points)
    county_poly = convert_polygons_json(poly_geojson) # ** so here you're just returning a list of shape objects, no meta information such as crs etc
    town_points = convert_points_json(point_geojson) # ** ditto
    """
    what i would do is use convert polygons to return a dict which has the following structure:
    {'crs':29902 (or whatever crs the geojson obj is in, 'features':[list of shapes here]}
    so you'd need to propogate that thru all your functions.... or just hardcode it into the shapefile as I've suggested
    above on line 132
    """
    spatial_results = spatial_operations(county_poly,town_points)
    single_polygon_shp(spatial_results[0])
    single_polygon_centroid_shp(spatial_results[1])
    urban_points_shp(spatial_results[2]) # ** so you need to specify the crs in the schema, and then assign it the crs
                                         # ** from the dict
    convex_hull_shp(spatial_results[3])
    convex_hull_centroid_shp(spatial_results[4])
    line_between_centroids_shp(spatial_results[5])

if __name__ == "__main__":
   main()