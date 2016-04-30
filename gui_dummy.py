from geo_utils import shape_maker, plot_shapes
import json
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
from shapely.ops import cascaded_union
from descartes import PolygonPatch

with open("cso_counties.txt",'r') as f1:
        cty_str = f1.read()

with open("geonames_pop.txt",'r') as f2:
    pop_str = f2.read()

cty_polygons = json.loads(cty_str)
places_pts = json.loads(pop_str)

counties = shape_maker(cty_polygons)
towns = shape_maker(places_pts)

cty_features = []
for cf in counties['features']:
    cty_features.append(cf)

patches = []
for cf in cty_features:
    if cf.geom_type == 'Polygon':
        patches.append(PolygonPatch(cf))
    elif cf.geom_type == 'MultiPolygon':
        for poly in cf:
            patches.append(PolygonPatch(poly))


for patch in patches:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    m = Basemap(llcrnrlon=-11.5,llcrnrlat=51.0,urcrnrlon=-5.0,urcrnrlat=56.0,
            resolution='i',projection='tmerc',lon_0=-7.36,lat_0=53.0, epsg = 29902)
    ax.add_patch(patch)
    plt.show()

