
def get_data_from_postgres(conn, qry):
    """
    A one-line definition of what the function does
    More detail as necessary
    :param conn: The database connection string
    :param qry: The SQL query which gets the data
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