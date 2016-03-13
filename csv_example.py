"""
Basic examples of
(i) pyproj in action - convert simple lat/lon pair to Irish  Grid
(ii) create shapefiles from csv
(iii) create create new geoometriies especially a set of disolved buffers around points using 'shapely'
"""

import csv
from shapely.geometry import Point, mapping, shape
from shapely.ops import cascaded_union
import fiona
from fiona.crs import from_epsg
from os import path
import pyproj

# pyproj in action
irish_grid=pyproj.Proj(init='epsg:29902')
wgs84=pyproj.Proj(init='epsg:4326')
lat = 53.5
lon = -8.5
easting, northing = pyproj.transform(wgs84, irish_grid, lon, lat)

# 'constants' - variable names where the values don't change for the run of the program
OUTPUT_DIR = ".cache"
CSV_FILE = "geoname_pop5000.csv"
POINT_SHP = path.join(OUTPUT_DIR,"geoname_pop5000.shp")
BUFFER_SHP = path.join(OUTPUT_DIR,"geoname_pop5000_buffer.shp")
UNION_SHP = path.join(OUTPUT_DIR,"geoname_pop5000_union.shp")


# Create new shapefile from csv input

schema = {'geometry': 'Point', 'properties': {'name': 'str', 'population': 'int'}}
with fiona.open(POINT_SHP, "w", "ESRI Shapefile", schema, crs=from_epsg(4326)) as output:
    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            point = Point(float(row['longitude']), float(row['latitude']))
            output.write({
                'properties': {
                    'name': row['name'],
                    'population': row['population']
                },
                'geometry': mapping(point)
            })

# Create new shapefile - buffer around last file created

with fiona.open(POINT_SHP, "r") as input:
    schema = input.schema.copy()
    schema['geometry'] = 'Polygon'

    with fiona.open(BUFFER_SHP, "w", driver=input.driver, schema=schema, crs=input.crs) as output:
        for point in input:
            output.write({
                'properties': {
                    'name': point['properties']['name'],
                    'population': point['properties']['population']
                },
                'geometry': mapping(shape(point['geometry']).buffer(0.1))
            })

# Create union of buffers created above

with fiona.open(BUFFER_SHP, "r") as input:
    schema = input.schema.copy()
    del schema['properties']['population']

    with fiona.open(UNION_SHP, "w", driver=input.driver, schema=schema, crs=input.crs) as output:
        shapes = []

        for feature in input:
            shapes.append(shape(feature['geometry']))

        merged = cascaded_union(shapes)

        output.write({
            'properties': {
                'name': 'Buffer Area'
            },
            'geometry': mapping(merged)
        })