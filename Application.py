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
def main():

    import cartopy
    import matplotlib.pyplot as plt
    from geo_utils import get_data_from_geoserver, geocode_item
    from geo_utils import shape_maker
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
    from descartes import PolygonPatch

    #   Variable assignment or initialisation
    countycents = collections.defaultdict(str)
    poly_geoms = []
    pt_geoms = []


    with open("cso_counties.txt",'r') as f1:
        cty_str = f1.read()

    with open("geonames_pop.txt",'r') as f2:
        pop_str = f2.read()

    cty_polygons = json.loads(cty_str)
    places_pts = json.loads(pop_str)

    counties = shape_maker(cty_polygons)
    towns = shape_maker(places_pts)
    geoms = [towns['features'][0], counties['features'][0]]

    print(len(counties['features']))
    print(counties['crs'])
    print(len(towns['features']))
    print(towns['crs'])

    #map_crs = cartopy.crs.TransverseMercator()
    #data_crs = cartopy.crs.TransverseMercator()
    ax = plt.axes([counties['bbox']])
    patch1 = PolygonPatch(geoms[1][0])
    ax.add_patch(patch1)
    plt.show()


    # c_counties = cartopy.feature.ShapelyFeature(geoms[1], data_crs)
    # c_towns = cartopy.feature.ShapelyFeature(geoms[0], data_crs)
    # ax.set_extent([-13, -5, 49, 56])
    # ax.add_feature(cartopy.feature.OCEAN)
    # ax.add_geometries(c_counties)
    # plt.show()


#
# def display_geometry(obj):
#     """
#     :param obj: a collection of shapely geometries to be displayed
#                 with the following data in the object
#     name: the name of the collection of geometries
#     crs: the crs of the input geometries
#     features: geom and properties of each shape
#     """
#     from cartopy import feature, crs
#     import pyproj
#     import matplotlib.pyplot as plot
#
#     bbox = obj['bbox']
#     patches = []
#     irish_grid = pyproj.Proj("+init=EPSG:29902")
#     for f in obj['features']:
#         patch = feature.ShapelyFeature(f[0], irish_grid)
#         patches.append(patch)
#     ax = plot.axes(projection = crs.TransverseMercator)
#     ax.coastlines()
#
#     for p in patches:
#         plot.plot(p)






if __name__ == '__main__':
    main()