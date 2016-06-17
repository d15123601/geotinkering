def plot_shapes(shapes):
    """
    Here we plot shapes passed in our custom geojson object
    The plotting is done with descartes
    :param shapes: dict containing crs, bbox and shapely features
    :return: plots the required shape
    """
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from mpl_toolkits.basemap import Basemap
    from shapely.ops import cascaded_union
    from descartes import PolygonPatch
    ctys = []
    for geom in shapes['features']:
        gtry = cascaded_union(geom[0]) #we need to dissolve any nested rings
        name = geom[1]['countyname']
        ctys.append((gtry,name))

    patches = []
    for cty in ctys:
        if cty[0].geom_type == 'Polygon':
            patches.append(PolygonPatch(cty[0]))
        elif cty[0].geom_type == 'MultiPolygon':
            for poly in cty[0]:
                patches.append(PolygonPatch(poly))

#TODO Investigate the projection and bounding of this map
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # resolution = 'i' means use intermediate resolution coastlines.
    # lon_0, lat_0 are the central longitude and latitude of the projection.
    m = Basemap(llcrnrlon=-11.5,llcrnrlat=51.0,urcrnrlon=-5.0,urcrnrlat=56.0,
                resolution='i',projection='tmerc',lon_0=-7.36,lat_0=53.0, epsg = 29902)
    # can get the identical map this way (by specifying width and
    # height instead of lat/lon corners)
    #m = Basemap(width=894887,height=1116766,\
    #            resolution='i',projection='tmerc',lon_0=-4.36,lat_0=54.7)
    #m.drawcoastlines()
    #m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawmapboundary(fill_color='aqua')
    ax.add_collection(PatchCollection(patches))
    plt.show()


def shape_maker(geojson_obj, id):
    """
    This function takes a geojson object and returns the pertinent gj_stack
    for this application.
    :param geojson_obj:
    :return: dict containing crs, bbox and shapely features
    """
    from shapely import geometry
    crs = geojson_obj['crs']
    bbox = geojson_obj['bbox']
    features = []
    for f in geojson_obj['features']:
        g = geometry.asShape(f['geometry'])
        p = f['properties']
        features.append((g,p))
    op_dict = {'crs':crs, 'bbox':bbox,'features':features}
    return op_dict


def shape_maker2(geojson_obj, feature_name):
    """
    This function takes a geojson object and returns the pertinent gj_stack
    for this application.
    :param geojson_obj:
    :return: dict containing crs, bbox and shapely features
    """
    from shapely import geometry
    from collections import defaultdict

    crs = geojson_obj['crs']
    bbox = geojson_obj['bbox']
    features = defaultdict(set)
    for f in geojson_obj['features']:
        name = f['properties'][feature_name]
        g = geometry.asShape(f['geometry'])
        p = f['properties']
        features[name] = (g, p)
    op_dict = {'crs':crs, 'bbox':bbox,'features':features}
    return op_dict


def pick_geojson(obj, getitem):
    """
    :param geojson_obj: This item is the geojson object for which we want to access
                        the gj_stack for.
    :param getitem: This is the item which we are looking for within the geojson object
    :return: The return will be a list of the object(s) we are looking for.
    """
    try:
        return obj[getitem]
    except KeyError:
        return 'No such item exists'
    except TypeError:
        return 'Data passed is not a dictionary'


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


def get_data_from_postgres(conn, qry):
    """
    A one-line definition of what the function does
    More detail as necessary
    :param conn: The database connection string
    :param qry: The SQL query which gets the gj_stack
    :return: The result set.
    """
    import psycopg2
    import psycopg2.extras
    try:
        my_conn = psycopg2.connect(conn)
        cur = my_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        try:
            cur.execute(qry)
            c = cur.fetchall()
            cur.close()
            # self.result = c
            return c
        except psycopg2.Error as e:
            print(e)
            return False

    except psycopg2.OperationalError as e:
        print(e)
        return False


def get_data_from_geoserver(geo_host, resource):
    """
    Gets a GeoJSON representation of any ressource published by any Geoserver
    :param geo_host: The name of the host geoserver including the port number if necessary
    :param resource: The name of the required resource in the format <workspace>:<resource name> e.g. cso:counties
    :return: The resource in GeoJSON format
    """
    import httplib2
    import json

    url = "http://{}/geoserver/ows?service=WFS&version=1.0.0&request=GetFeature&typeName={}&outputFormat=json" \
          "&srsName=epsg:4326"\
        .format(geo_host, resource)

    try:
        h = httplib2.Http(".cache")
        response_headers, response = h.request(url)
        return json.loads(response.decode())

    except httplib2.HttpLib2Error as e:
        print(e)
        return False
    except Exception as e:
        print(e)
        return False


def proj_point(crs_from, crs_to, x, y):

    from pyproj import transform
    from shapely.geometry import Point

    a, b = pyproj.transform(crs_from, crs_to, x, y)
    point = Point(a, b)
    return point


def transform_coordinates(source_srid, target_srid, source_x, source_y):
    """
    Transforms a coordinate pair from one spatial reference system to another. Inputs are the EPSG reference codes for
    source and target SRIDs in the format "epsg:nnn" where nnn is the numeric code. Examples are 4326 (WGS84) and 29902
    (Irish Grid).
    Source x and y could be lon/lat or easting/northing
    :param source_srid:
    :param target_srid:
    :param source_x:
    :param source_y:
    :return: tuple containing new coordinate pair
    """

    import pyproj

    try:
        source_proj = pyproj.Proj(init=source_srid)
        target_proj = pyproj.Proj(init=target_srid)

        target_x, target_y = pyproj.transform(source_proj, target_proj, source_x, source_y)

        return (target_x, target_y)

    except RuntimeError as e:
        print(str(e))
        return None

def geocode_item(**kwargs):
    """
    Geocode address or reverse geocode coordinate pair using OSM's Nominatim geocoder.
    :param kwargs: Dictionary of key/value pairs which vary depending on specific requirements. To geocode an address
    you need to supply an "address" item. To reverse geocode a coordinate pair, you need to supply a lat/lon pair and
    have the "reverse" item set to true. In either case, the coordinate pair must be in WGS84.
    :return: A dictionary of result key/value pairs
    """

    try:
        geolocator = Nominatim()
        if (not kwargs["reverse"]) and kwargs["address"]:
            location = geolocator.geocode(kwargs["address"])
            return location.raw
        elif (kwargs["reverse"]) and (kwargs["lon"] and kwargs["lat"]):
            location = geolocator.reverse((kwargs["lat"], kwargs["lon"]))
            return location.raw
        else:
            return None
    except geopy.exc.GeopyError as e:
        print(str(e))
        return None
