from geo_utils import shape_maker
import json

with open("cso_counties.txt",'r') as f1:
        cty_str = f1.read()

with open("geonames_pop.txt",'r') as f2:
    pop_str = f2.read()

cty_polygons = json.loads(cty_str)
places_pts = json.loads(pop_str)

counties = shape_maker(cty_polygons)
towns = shape_maker(places_pts)



plot_shapes(counties)