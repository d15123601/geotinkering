""" Here we access geojson held in a textfile - it is then used to perform the
    following tasks reqd for the GIS programming assignment.....

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
from tkinter import *
from tkinter import ttk
from collections import defaultdict
from tkinter import messagebox
from shapely.ops import cascaded_union
import shapely.geometry as geometry
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import fiona
from fiona.crs import from_epsg
import json
import os
import geopy
from geopy.geocoders import GeoNames, Nominatim
import pyproj

def main():
    scriptDir = os.path.dirname(__file__)
    op_data = os.path.normpath(os.path.join(scriptDir, "op_data"))
    if not os.path.exists(op_data):
        os.mkdir(op_data)
    cty_params = {'host': "mf2.dit.ie:8080",
                  'layer': "cso:ctygeom",
                  'srs_code': 29902,
                  'properties': "",
                  'geom_field': "",
                  'filter_property': "",
                  'filter_values': ""}
    town_params = {'host': "mf2.dit.ie:8080",
                  'layer': "dit:geonames_pop_5000",
                  'srs_code': 29902,
                  'properties': "",
                  'geom_field': "",
                  'filter_property': "",
                  'filter_values': ""}
    cty_polys = get_geojson(cty_params)
    town_pts = get_geojson(town_params)

    # MyShape takes a value which identifies the best identifier for each feature:
    # in the case of the cty_polys data, it is 'countyname', for town_pts it is 'asciiname'

    ctys = MyShape(cty_polys, 'countyname')
    towns = MyShape(town_pts, 'asciiname')

    # Let's pick some counties to merge, say 'South Tipperary','North Tipperary','Waterford County'
    # and 'Cork County'

    merge_list = ['South Tipperary','North Tipperary','Waterford County','Cork County']
    merge_targets = {k:v[0] for k,v in ctys.features.items() if k in merge_list}

    merged_geom_name = "-".join(list(merge_targets.keys()))
    merged_geom = cascaded_union(list(merge_targets.values()))
    # Use our function to create a shapefile with this merged geometry
    make_shapefile(merged_geom, 'merged_geom')

    # Let's make the centroid now...
    mg_centroid = merged_geom.centroid
    print(mg_centroid)

    # we need to extract the points that lie within the centroid:
    contained_points = {k:v[0] for k, v in towns.features.items()
                        if merged_geom.contains(v[0])}

    # compute the convex hull for the points
    # first make a multipoint geometry
    mp = geometry.MultiPoint(list(contained_points.values()))
    # make a shapefile of the multipoints
    make_shapefile(mp, 'multipoints')
    #get the convex hull
    convex_hull = mp.convex_hull
    # let's make a shapefile...
    make_shapefile(convex_hull, 'convex_hull')
    # get the centroid of the convex hull
    ch_centroid = convex_hull.centroid

    centroid_difference = ch_centroid.distance(mg_centroid)
    print("The distance between the centroids is: " + str(centroid_difference))

    # create the line between the two centroids
    line = geometry.LineString([ch_centroid, mg_centroid])
    # Make shapefile
    make_shapefile(line, 'Connector')

    # geocode the centroids
    mg_cent_location = geocode(mg_centroid)
    ch_cent_location = geocode(ch_centroid)
    print(mg_cent_location)
    print(ch_cent_location)

    # Store the points with their location
    cent_dict = {}
    cent_dict[mg_cent_location] = mg_centroid
    cent_dict[ch_cent_location] = ch_centroid
    make_shapefile(cent_dict, 'centroids')



def geocode(pt):
    # first transform the points to wgs84
    try:
        crs_from = pyproj.Proj("+init=EPSG:29902")
        crs_to = pyproj.Proj("+init=EPSG:4326")
        x, y = pt.x, pt.y
        x1, y1 = pyproj.transform(crs_from, crs_to, x, y)
        long = str(x1)
        lat = str(y1)
        geolocator = Nominatim(timeout=10)
        location = geolocator.reverse((lat, long))
        return location.address
    except geopy.exc.GeopyError as e:
        print(str(e))
        return None

def make_shapefile(data, name):
    path = os.path.join('op_data',name + '.shp')
    crs = crs = from_epsg('29902')
    if type(data) == dict:
        a_schema = {'geometry': 'Point',
                            'properties': {'name':'str', 'address':'str'}
                    }
        with fiona.open(path, "w",
                        driver= 'ESRI Shapefile',
                        crs= crs,
                        schema= a_schema) as output:
            for k, v in data.items():
                parts = k.split(',')
                name = parts[0]
                output.write({
                            'properties':{'name':name, 'address':k},
                              'geometry':geometry.mapping(v)})
    else:
        geom_type = data.geom_type

        a_schema = {'geometry': geom_type,
                            'properties': {'name':'str'}
                           }
        with fiona.open(path, "w",
                        driver= 'ESRI Shapefile',
                        crs= crs,
                        schema= a_schema) as output:
            output.write({
                        'properties':{'name':name},
                          'geometry':geometry.mapping(data)})


def get_geojson(params):
    """
    This function accepts a dictionary of parameters and returns a GeoJSON representation of the requested layer. This
    takes a format similar to the following example:

    {
        "host": "mf2.dit.ie:8080",
        "layer": "cso:ctygeom",
        "srs_code": 29902,
        "properties": ["countyname", ],
        "geom_field": "geom",
        "filter_property": "countyname",
        "filter_values": ["Cork", "Kerry"]
    }

    You can filter the set of features returned by adjusting "filter_values". This is a list of values that must
    be present in "filter_property". In the above example you'd get the counties of Cork and Kerry plus Cork City.
    Similarly, you can filter the properties returned to reduce their number. If you use this feature, you'll need to
    set "geom_field" to the name of the geometry field. Geoserver can give you this.

    All values in the dictionary are optional except "host" and "layer".

    :param Dictionary as above:
    :return: Parsed GeoJSON or exception as appropriate
    """

    import urllib.parse
    import httplib2
    import os, os.path
    import json
    import xml.etree.ElementTree as etree

    #
    # Check that the parameters exist and/or sensible. Because the filter can contain some 'odd' characters such as '%'
    # and single quotes the filter text needs to be url encoded so that text like "countyname LIKE '%Cork%'" becomes
    # "countyname%20LIKE%20%27%25Cork%25%27" which is safer for URLs
    #
    if "host" not in params:
        raise ValueError("Value for 'host' required")
    if "layer" not in params:
        raise ValueError("Value for 'layer' required")
    if "srs_code" in params and params["srs_code"]:
        srs_text = "&srsName=epsg:{}".format(params["srs_code"])
    else:
        srs_text = ""
    if "properties" in params and params["properties"]:
        item_string = ""
        for item in params["properties"]:
            item_string += str(item) + ","
        if "geom_field" in params and params["geom_field"]:
            item_string += str(params["geom_field"])
        property_text = "&PROPERTYNAME={}".format(item_string)
    else:
        property_text = ""
    if "filter_property" in params and params["filter_property"] and params["filter_values"]:
        filter_text = "{filter_property} LIKE '%{filter_values}%'".format(filter_property=params["filter_property"], filter_values=params["filter_values"][0])
        for item in range(1, len(params["filter_values"])):
            filter_text += "OR {filter_property} LIKE '%{filter_values}%'".format(filter_property=params["filter_property"], filter_values=params["filter_values"][item])
        filter_text = urllib.parse.quote(filter_text)
        filter_text = "&CQL_FILTER=" + filter_text
    else:
        filter_text = ""

    url = "http://{host}/geoserver/ows?" \
          "service=WFS&version=1.0.0&" \
          "request=GetFeature&" \
          "typeName={layer}&" \
          "outputFormat=json".format(host=params["host"], layer=params["layer"])
    url += srs_text
    url += property_text
    url += filter_text

    #
    # Make a directory to hold downloads so that we don't have to repeatedly download them later, i.e. they already
    # exist so we get them from a local directory. This directory is called .httpcache".
    #
    scriptDir = 'C:\\Python34'
    cacheDir = os.path.join(scriptDir, ".httpcache")
    if not os.path.exists(cacheDir):
        os.mkdir(cacheDir)

    #
    # Go to the web and attempt to get the resource
    #
    try:
        h = httplib2.Http(cacheDir)
        response_headers, response = h.request(url)
        response = response.decode()

        #
        # Geoserver only sends valid gj_stack in the requested format, in our case GeoJSON, so if we get a response back in
        # XML format we know that we have an error. We do minimal parsing on the xml to extract the error text and raise
        # an exception based on it.
        #
        if response[:5] == "<?xml":
            response = etree.fromstring(response)
            xml_error = ""
            for element in response:
                xml_error += element.text
            raise Exception(xml_error)
        else:
            return json.loads(response)

    except httplib2.HttpLib2Error as e:
        print(e)

class MyShape:
    #todo add methods to reproject, perform geometric functions etc.
    def __init__(self, geojson_obj, feature_id):
        from shapely import geometry
        self.crs = geojson_obj['crs']
        self.type = geojson_obj['type']
        self.bbox = geojson_obj['bbox']
        # create a dict of {name: (geom, properties)} for each feature in the dataset
        self.features = {f['properties'][feature_id]:(geometry.asShape(f['geometry']),f['properties'])
                          for f in geojson_obj['features']}

if __name__ == main():
    main()