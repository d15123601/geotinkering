from osgeo import ogr, osr
import pyproj


def get_layer_spatialref(src):
    layer = src.GetLayer(0)
    spatialRef = layer.GetSpatialRef()
    return spatialRef


def shapefile_loader(filename):
    shapefile = ogr.Open(filename)
    print(shapefile)
    layer = shapefile.GetLayer(0)
    spatialRef = layer.GetSpatialRef()
    featurecount = layer.GetFeatureCount()
    is_projected = spatialRef.IsProjected()
    if is_projected:
        spatialRef.GetWellKnownSpatialReference()
    opstr = str.format('This shapefile has spatial reference {}\n'
                       'Is Projected: {}\n'
                       'and has {} features.', spatialRef, is_projected, featurecount)
    print(opstr)
    return shapefile


"""The below function intakes a shapefile and projects it to the
   specified destination projection. The 'dst_proj' is an EPSG
   code.
"""


#TODO finish this code
def reproj_shapefile(sf, dst_proj):
    print(sf)
    layer = sf.GetLayer(0)
    spatialRef = layer.GetSpatialRef()
    if spatialRef == None:
        print("Shapefile has no spatial reference")
        spatialRef = osr.SpatialReference()
        spatialRef.SetWellKnownGeogCS('WGS84')

    srcproj = spatialRef
    dstproj = osr.SpatialReference()
    dstproj.ImportFromEPSG(dst_proj)
    transform = osr.CoordinateTransformation(srcproj, dstproj)
    projected_features = [doProjection(feature, transform) for feature in layer]
    print[projected_features]
    #TODO i need to build a function to create a shapefile from the above list


def doProjection(feature, transform):
    pt = feature.GetGeometryRef()
    pt.Transform(transform)
    return [pt.GetPoint()[i] for i in [1,0]]

def get_line_segments_from_geom(geometry):
    segments = []
    if geometry.GetPointCount() > 0:
        segment = []
        for i in range(geometry.GetPointCount()):
            segment.append(geometry.GetPoint_2D(i))
        segments.append(segment)
    for i in range(geometry.GetGeometryCount()):
        subGeometry = geometry.GetGeometryRef(i)
        segments.extend(get_line_segments_from_geom(subGeometry))
    return segments

def main():
    pass


if __name__ == '__main__':
    main()


