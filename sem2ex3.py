

"""
Create new shapefiles using Shapely and Fiona

This exercise is designed to combine basic programming skills with a first attempt at processing geospatial data using the libraries, Shapely and Fiona. Remember, Shapely encapsulates the functionality of GEOS so it's useful in manipulating spatial objects, and Fiona reads and writes various vector formats including shapefiles.

The task

Take an existing CSV (comma-separated values) text file which contains data which can be represented as points. I suggest using one of the CSVs created by Alain for his tutorial.
Create a new schema which takes some or all of the elements in each row and creates a new shapefile with polygon geometries representing a buffer around each point.
Create yet another shapefile to merge the buffers into a single multipolygon geometry.
"""
from shapely.geometry import MultiPolygon, mapping
from fiona import collection
import os
import csv

csv.field_size_limit(500 * 1024 * 1024)

path = r'C:\Users\admin\Google Drive\College\RepositoryDataDump\csv_files'
file = 'ctygeom.csv'


schema = { 'geometry': 'Point', 'properties': { 'name': 'str' } }

with collection("some.shp", "w", "ESRI Shapefile", schema) as output:
    with open(os.path.join(path,file),'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            county = MultiPolygon(row['geom'])
            output.write({'properties': {'name': row['countyname']},'geometry': mapping(county)})
