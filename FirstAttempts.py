from osgeo import ogr, osr
import pyproj
import psycopg2
import os.path
import osgeo.ogr

connection = psycopg2.connect(database='SSPL9075', user='postgres',
                              password='dragon', host = 'localhost', port = '5432')
cursor = connection.cursor()

# convert counties to ITM95
sql1 = 'CREATE TABLE itm_95_places AS SELECT gid, ST_Transform(geom, 2157) AS geom, placename, population ' \
      'FROM places WHERE population IS NOT NULL'

cursor.execute(sql1)

sql = 'SELECT * FROM itm_95_places'
cursor.execute(sql)
for row in cursor.fetchall():
    print(row)


sql2 = 'SELECT ST_UNION(cg1.geom, cg2.geom) FROM ' \
      'ctygeom cg1, ctygeom cg2 WHERE ' \
      'cg1.countyname = (%s) AND cg2.countyname = (%s);'

params2 = ("Cork County", "Cork City", )

cursor.execute(sql2, params2)
cork_geom = cursor.fetchone()
print(cork_geom[0])

sql3 = 'SELECT placename, population, geom FROM itm_95_places' \
       ' WHERE ST_CONTAINS(%s, geom);'

params3 = (cork_geom[0], )

cursor.execute(sql3, params3)
print(cursor.rowcount)
for record in cursor:
    print(record)







