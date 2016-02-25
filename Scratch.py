from osgeo import ogr, osr
import pyproj
import os.path
from ShapefileUtils import *

path = r'C:\Users\mickle\Google Drive\College\RepositoryDataDump\IrelandShapeFiles'

sf = shapefile_loader(os.path.join(path, 'places.shp'))
sr = get_layer_spatialref(sf)
print('1: ', sr)
new_sf = reproj_shapefile(sf, 2157)
print('ok')
print('2: ',get_layer_spatialref(new_sf))