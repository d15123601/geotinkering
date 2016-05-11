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

def main():
    cty_params = {'host': "mf2.dit.ie:8080",
                  'layer': "cso:ctygeom",
                  'srs_code': 29902,
                  'properties': "",
                  'geom_field': "",
                  'filter_property': "",
                  'filter_values': ""}
    town_params = {'host': "mf2.dit.ie:8080",
                  'layer': "'dit:geonames_populated'",
                  'srs_code': 29902,
                  'properties': "",
                  'geom_field': "",
                  'filter_property': "",
                  'filter_values': ""}
    cty_polys = get_geojson(cty_params)
    town_pts = get_geojson(town_params)





 def get_geojson(self, params):
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