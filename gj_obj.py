import json

with open("cso_counties.txt",'r') as f1:
        cty_str = f1.read()

with open("geonames_pop.txt",'r') as f2:
    pop_str = f2.read()

cty_polygons = json.loads(cty_str)
places_pts = json.loads(pop_str)

def geoj_exploder(gj_obj):
    l1 = [(k,v) for k,v in gj_obj.items()]
    i = gj_obj['features'][0]
    p = i['properties']
    l2 = list(p.keys())

    return [l1, l2]


tree1 = geoj_exploder(places_pts)
tree2 = geoj_exploder(cty_polygons)
print(tree1)







