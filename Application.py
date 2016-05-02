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

# class shapes(geojson_obj):
#     def __init__(self):
#         pass



class myGUI:
    def __init__(self, master, input_datasets):
        # variables
        self.dataset_ref = ""
        self.ops_output = {}

        self.dialog_text = StringVar()
        self.dialog_text.set("Messages will display here")

        self.dataset_list = [keys for keys in input_datasets.keys()]
        self.dataset = input_datasets
        self.cb_list = ['No data loaded']

        self.ops_subject = StringVar()
        self.ops_subject.set('')

        # GUI creation
        self.master = master

        # Initialise all the widgets.
        self.main_frame = ttk.Frame(self.master)

        self.dialog = ttk.Label(self.main_frame, textvariable = self.dialog_text,
                                foreground = 'cyan',
                                background = 'blue', anchor = 'center')
        self.selection_box = ttk.Labelframe(self.main_frame, text = 'Object Picker',
                                width = 250, height = 500, borderwidth = 5,
                                relief = 'sunken')
        self.dataset_box = ttk.Labelframe(self.selection_box, text = 'Dataset Picker',
                                width = 250, height = 100, borderwidth = 5,
                                relief = 'sunken')
        ttk.Label(self.dataset_box, text = 'Please choose a dataset from the list:',
                  foreground = 'red', justify = 'left').grid(row = 0, column = 0)
        self.datacb = ttk.Combobox(self.dataset_box, values= self.dataset_list, state='readonly')

        self.datacb.current(1)
        # set the selection event
        self.cb_box = ttk.Labelframe(self.selection_box, text = 'Item Picker',
                                width = 250, height = 400, borderwidth = 5,
                                relief = 'sunken')
        ttk.Label(self.cb_box, text = 'Please choose an item from the list:',
                  foreground = 'red', justify = 'left').grid(row = 0, column = 0)
        self.itemcb = ttk.Combobox(self.cb_box, values= self.cb_list, state='disabled')
        self.itemcb.current(0)
        # set the selection event
        self.op_box = ttk.Labelframe(self.main_frame, text = 'Operations',
                                    width = 250, height = 500,
                                    borderwidth = 5,
                                    relief = 'sunken')
        self.btn_add = ttk.Button(self.op_box, width = 50, text = 'Add', command = self.choose_selected)
        self.btn_merge = ttk.Button(self.op_box, width = 50, text = 'Merge',
                                    command = self.merge_chosen, state = 'disabled')
        self.btn_geocode = ttk.Button(self.op_box, width = 50, text = 'Geocode',
                                    command = self.geocode_chosen, state = 'disabled')
        self.btn_centroid = ttk.Button(self.op_box, width = 50, text = 'Centroid',
                                    command = self.centroid_chosen, state = 'disabled')
        self.btn_convexhull = ttk.Button(self.op_box, width = 50, text = 'Make Convex Hull',
                                    command = self.convex_hull, state = 'disabled')
        self.btn_line_join = ttk.Button(self.op_box, width = 50, text = 'Join with line',
                                    command = self.line_join, state = 'disabled')
        self.ops_frame = ttk.Labelframe(self.op_box, text = 'Items selected:',
                                        relief = 'sunken')
        self.subject_list = ttk.Label(self.ops_frame, textvariable = self.ops_subject,
                                      anchor = 'w')
        self.display_box = ttk.Labelframe(self.main_frame, text = 'Object Display',
                                width = 500, height = 500, borderwidth = 5,
                                relief = 'sunken')


        #Lay out all the widgets
        self.main_frame.grid(column = 0, row = 0, sticky = (N, S, E, W))
        self.dialog.grid(row = 0, column = 0, columnspan = 3)
        self.selection_box.grid(row = 1, column = 0, sticky = 'ns')
        self.dataset_box.grid(row = 0, column = 0, sticky = 'ns')
        self.datacb.grid(row = 1, column = 0, sticky = 'nsew')
        self.cb_box.grid(sticky = 'nsew')
        self.itemcb.grid(row = 1, column = 0, sticky = 'nsew')
        self.op_box.grid(row = 1, column = 1, sticky = 'ns')
        self.btn_add.grid(row = 0, column = 0)
        self.btn_merge.grid(row = 1, column = 0)
        self.btn_geocode.grid(row = 2, column = 0)
        self.btn_centroid.grid(row = 3, column = 0)
        self.btn_convexhull.grid(row = 4, column = 0)
        self.btn_line_join.grid(row = 5, column = 0)
        self.ops_frame.grid(sticky = 'nsew')
        self.subject_list.grid(sticky = 'nsew')
        self.display_box.grid(row = 1, column = 2, sticky = 'ns')

        # Event handling
        self.datacb_value = self.datacb.bind("<<ComboboxSelected>>", self.dataset_cb_newselection)
        self.itemcb_value = self.itemcb.bind("<<ComboboxSelected>>", self.itemcb_newselection)

    def dataset_cb_newselection(self, event):
        print(event.widget)
        owner = event.widget
        self.value_of_combo = owner.get()
        self.dialog_text.set("You have chosen - " + self.value_of_combo)
        self.update_itemcb(self.value_of_combo)

    def itemcb_newselection(self, event):
        print(event.widget)
        owner = event.widget
        self.geo_item = owner.get()

    def update_itemcb(self, dataset_name):
        item_list = [i[0] for i in self.dataset[dataset_name]]
        self.cb_list = 'Please select from below'
        self.itemcb['values'] = item_list
        self.itemcb.state(['!disabled', 'readonly'])

    def add_cb_value(self):
        self.cty = str(self.dataset_cb_newselection)
        self.cty_stack.append(self.cty)

    def choose_selected(self):
        pass

    def merge_chosen(self):
        #TODO ensure >1 argument to this function
        pass


    def geocode_chosen(self):
        #TODO ensure only 1 argument to this function
        pass

    def centroid_chosen(self):
        pass


    def convex_hull(self):
        pass


    def line_join(self):
        pass

def main():

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

    root = Tk()
    county_names = [(c[1]['countyname'],c[0]) for c in counties['features']]
    town_names = [(t[1]['name'],t[0]) for t in towns['features']]
    datasets = {'Counties':county_names, 'Towns':town_names}
    myGUI(root, datasets)
    root.mainloop()











if __name__ == '__main__':
    main()