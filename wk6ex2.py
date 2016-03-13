import geo_utils
from fiona import collection
from shapely import wkt, geometry
import csv
import os

"""
Create new shapefiles using Shapely and Fiona

This exercise is designed to combine basic programming skills with a first attempt at processing geospatial data using the libraries, Shapely and Fiona. Remember, Shapely encapsulates the functionality of GEOS so it's useful in manipulating spatial objects, and Fiona reads and writes various vector formats including shapefiles.

The task

Take an existing CSV (comma-separated values) text file which contains data which can be represented as points. I suggest using one of the CSVs created by Alain for his tutorial.
Create a new schema which takes some or all of the elements in each row and creates a new shapefile with polygon geometries representing a buffer around each point.
Create yet another shapefile to merge the buffers into a single multipolygon geometry.
"""

csv.field_size_limit(500 * 1024 * 1024)
town = {}
shapes = {}

with open("ltgeom.csv",'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        geom = row['geom']
        id = row['FID']
        t_name = row['name']
        t_males = row['male2011']
        t_females = row['female2011']
        t_total = t_females + t_males
        town[id] =  (t_name, geometry.MultiPolygon(wkt.loads(geom)), t_females, t_males, t_total)

path = r"C:\Users\admin\Google Drive\College\RepositoryDataDump\IrelandShapeFiles"
with collection(os.path.join(path, 'natural.shp'),'r') as ip:
    with collection('rivers.shp','w') as op:
        for feature in ip:
            if (feature['properties']['type']) == "water":

                output.write({feature['properties']['name']: },'geometry': mapping(shape)})

















