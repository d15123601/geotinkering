"""Take a data set of "populated places" from the PostgreSQL/PostGIS server on mf2.dit.ie and the geometry of Cork
from the "ctygeom" shapefile and return a list of settlements in Cork sorted by pouation size. Also, find the
postal address of the centroid of Cork County."""

import os
import pyproj
import gdal
import fiona
import psycopg2
import psycopg2.extras
from ShapefileUtils import *

"""Get the populated places data from dit geoserver"""
try:
    connection = psycopg2.connect("dbname=geonames user=stduser password=stduser host=mf2.dit.ie port=5432")
    cursor = connection.cursor(cursor_factory = psycopg2.extras.DictCursor) # each row as a dictionary

    try:
        cursor.execute("SELECT * FROM geonames_populated")
        places_pop = cursor.fetchall()
        cursor.close()
    except psycopg2.Error as e:
        print(e)


except psycopg2.OperationalError as e:
    print(e)

path = r'C:\Users\mickle\Google Drive\College\RepositoryDataDump\IrelandShapeFiles'
fn = os.path.join(path, 'counties.shp')

with fiona.open(fn,'r') as source:
    print(source.crs)



def main():
    pass

if __name__ == '__main__':
    main()





