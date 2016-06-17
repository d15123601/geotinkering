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
    scriptDir = os.path.dirname(__file__)
    op_data = os.path.normpath(os.path.join(scriptDir, "op_data"))
    if not os.path.exists(op_data):
        os.mkdir(op_data)
    root = Tk()
    LoadingGUI(root)
    root.mainloop()


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


class MicksGis:
        """
        This class will construct the gis gui.
        We pass in the collection of MyShape objects.
        """
        def __init__(self, master, datasets):
            with open("provinces.txt",'r') as f2:
                prov_str = f2.read()
            prov_polygons = json.loads(prov_str)
            provs = []
            for f in prov_polygons['features']:
                provs.append(geometry.asShape(f['geometry']))
            self.bg = cascaded_union(provs)
            self.master = master
            self.datasets = datasets
            self.current_dataset = ""
            self.op_counter = 0
            self.op_stack = {}
            self.operation = 'N' # this holds a value to tell which operation is currently in progress
                                # M = Merge, I = Intermediate, G = Geocode, N = None
            self.master.title("SIMPLE GIS")

            # Set Button style
            s = ttk.Style()
            s.configure('Wait.TButton',foreground = 'red', state = 'disabled')
            s.configure('Go.TButton', foreground = 'green', state = 'active')

            # Declaring variables
            self.cb_datasets_source = []
            self.cb_datasets_source = [d for d in self.datasets]
            self.cb_op_data_source = []
            self.lb_features_source = StringVar()
            self.lb_feature_data_source = StringVar()
            self.dialog_text = StringVar()
            self.dialog_text.set('Messages will appear here.')

            # widget declarations
            self.frm_mainframe = ttk.Frame(self.master,
                                       )
            self.lbl_message = ttk.Label(self.master,
                                         font = ('Helvetica', 16),
                                         foreground = 'blue',
                                         textvariable = self.dialog_text)

            # Set up frames
            self.frm_data_pane_top = ttk.LabelFrame(self.frm_mainframe,
                                                    text = 'Dataset Explorer',
                                                    width = 40)
            self.frm_data_pane_middle = ttk.LabelFrame(self.frm_mainframe,
                                                       text = 'Feature Explorer',
                                                       width = 40)
            self.frm_data_pane_bottom = ttk.LabelFrame(self.frm_mainframe,
                                                       text = 'Feature Data',
                                                       width = 40)
            self.frm_functions = ttk.LabelFrame(self.frm_mainframe,
                                                text = 'Functions')

            #Set up widgets
                # Data selection and viewing
            self.lbl_ip_data = ttk.Label(self.frm_data_pane_top,
                                         text = 'Input Data:')
            self.cb_datasets = ttk.Combobox(self.frm_data_pane_top,
                                            height = 5,
                                            values = self.cb_datasets_source,
                                            width = 40)
            self.lbl_op_data = ttk.Label(self.frm_data_pane_top,
                                         text = 'Output Data:')
            self.cb_op_data = ttk.Combobox(self.frm_data_pane_top,
                                           height = 5,
                                           values = self.cb_op_data_source,
                                           width = 40,
                                           state = 'disabled')
            self.lb_features = Listbox(self.frm_data_pane_middle,
                                       height = 10,
                                       listvariable = self.lb_features_source,
                                       width = 40,
                                       state = 'disabled')
            self.lb_feature_data = Listbox(self.frm_data_pane_bottom,
                                           height = 10,
                                           listvariable = self.lb_feature_data_source,
                                           width = 40)
                # Functions
            self.btn_feature_display = ttk.Button(self.frm_data_pane_middle,
                                                  text = 'DISPLAY SELECTED',
                                                  style = 'Wait.TButton',
                                                  command = lambda: self.display(feature_name =
                                                                    self.lb_features.get(
                                                                    self.lb_features.curselection())))
            self.btn_confirm = ttk.Button(self.frm_data_pane_middle,
                                          text = 'CONFIRM SELECTED',
                                          style = 'Wait.TButton',
                                          state = 'disabled',
                                          command = lambda: self.confirm(self.lb_features.curselection()))
            self.btn_merge_polygons = ttk.Button(self.frm_functions,
                                                 width = 20,
                                                 cursor = 'hand1',
                                                 text = 'MERGE',
                                                 style = 'Wait.TButton',
                                                 command = self.merge_polys)
            self.btn_points_within_poly = ttk.Button(self.frm_functions,
                                                 width = 20,
                                                 cursor = 'hand1',
                                                 text = 'Ps in POLY',
                                                 style = 'Wait.TButton',
                                                 command = self.points_within_poly)
            self.btn_centroid = ttk.Button(self.frm_functions,
                                                 width = 20,
                                                 cursor = 'hand1',
                                                 text = 'CENTROID',
                                                 style = 'Wait.TButton',
                                                 command = self.centroid)
            self.btn_make_shp = ttk.Button(self.frm_functions,
                                                 width = 20,
                                                 cursor = 'hand1',
                                                 text = 'MAKE .SHP',
                                                 style = 'Wait.TButton',
                                                 command = self.make_shp)
            self.geocode = ttk.Button(self.frm_functions,
                                                 width = 20,
                                                 cursor = 'hand1',
                                                 text = 'GEOCODE',
                                                 style = 'Wait.TButton',
                                                 command = self.geocode)




            # widget placement
            self.lbl_message.grid(row = 0, column = 0)

            self.frm_mainframe.grid(row = 1, column = 0)
            self.frm_data_pane_top.grid(row = 0, column = 0, sticky = 'w')
            self.lbl_ip_data.grid(row = 0, column = 0, sticky = 'new')
            self.cb_datasets.grid(row = 0, column = 1, sticky = 'ew')
            self.lbl_op_data.grid(row = 0, column = 2, sticky = 'nw')
            self.cb_op_data.grid(row = 0, column = 3, sticky = 'new')

            self.frm_data_pane_middle.grid(row = 1, column = 0, sticky = 'ew')
            self.lb_features.grid(row = 0, column = 0, sticky = 'ew')
            self.btn_feature_display.grid(row = 1, column = 0, sticky = 'ew')
            self.btn_confirm.grid(row = 2, column = 0, sticky = 'ew')

            self.frm_data_pane_bottom.grid(row = 2, column = 0, sticky = 'ew')
            self.lb_feature_data.grid(row = 0, column = 0, sticky = 'ew')

            self.frm_functions.grid(row = 3, column = 0,
                                    columnspan = 1)
            self.btn_merge_polygons.grid(row = 0, column = 0)
            self.btn_points_within_poly.grid(row = 0, column = 1)
            self.btn_centroid.grid(row = 0, column = 2)
            self.btn_make_shp.grid(row = 0, column = 3)
            self.geocode.grid(row = 0, column = 4)

            # event handling
            _ = self.cb_datasets.bind("<<ComboboxSelected>>", self.dataset_cb_newselection)
            _ = self.lb_features.bind("<<ListboxSelect>>", self.feature_lb_newselection)
            _ = self.frm_functions.bind("<<Button1>>", self.check_op_stack)


            # functions
        def check_op_stack(self):
            if self.op_stack:
                self.cb_op_data.configure(state = 'normal')

        def display(self, feature_name = None, *args):
            # allows function to be used by multiple processes, first option (when a feature_name is passed)
            # is for viewing data, second option is for viewing created geometries
            if feature_name:
                geom = self.datasets[self.current_dataset].features[feature_name][0]
                if geom.geom_type != ('Polygon' or 'MultiPolygon'):
                    self.dialog_text.set('This geometry is invalid. Please use a different dataset')
                    pass
                geom = cascaded_union(geom) #to dissolve multipolygons
                geom_bdry = geom.boundary
                minx, miny, maxx, maxy = self.bg.bounds
                w, h = maxx - minx, maxy - miny
                fig = plt.figure(1, figsize = (5, 5), dpi = 180, frameon = False)
                ax = fig.add_subplot(111)
                ax.set_xlim(minx,maxx)
                ax.set_ylim(miny,maxy)
                for poly in self.bg:
                    bg_patch = PolygonPatch(poly, fc = 'lightsage', ec = 'k', alpha = 1)
                    ax.add_patch(bg_patch)

                if geom.geom_type == 'MultiPolygon':
                    for poly in geom:
                        patch = PolygonPatch(poly, fc= 'teal', ec='navy', alpha = 0.5)
                        ax.add_patch(patch)
                else:
                    patch = PolygonPatch(geom, fc='teal', ec='navy', alpha = 0.5)
                    ax.add_patch(patch)
                plt.show()
            else:
                geom = args[0]
                name = args[1]
                geom = cascaded_union(geom) #to dissolve multipolygons
                minx, miny, maxx, maxy = self.bg.bounds
                w, h = maxx - minx, maxy - miny
                fig = plt.figure(1, figsize = (5, 5), dpi = 180, frameon = False)
                ax = fig.add_subplot(111)
                ax.set_xlim(minx,maxx)
                ax.set_ylim(miny,maxy)
                for poly in self.bg:
                    bg_patch = PolygonPatch(poly, fc = 'lightsage', ec = 'k', alpha = 1)
                    ax.add_patch(bg_patch)
                if geom.geom_type == 'MultiPolygon':
                    for poly in geom:
                        patch = PolygonPatch(poly, fc= 'teal', ec='navy', alpha = 0.5)
                        ax.add_patch(patch)
                else:
                    patch = PolygonPatch(geom, fc='teal', ec='navy', alpha = 0.5)
                    ax.add_patch(patch)
                plt.title(name)
                plt.show()

        def dataset_cb_newselection(self, event):
            self.lb_feature_data_source.set([]) # wipe the feature data source
            self.current_dataset = event.widget.get()
            self.dialog_text.set("You have chosen - " + self.current_dataset.capitalize())
            self.update_feature_explorer(self.current_dataset)

        def update_feature_explorer(self, dataset_name):
            item_list = list(self.datasets[dataset_name].features.keys())
            self.lb_features_source.set(item_list)
            self.lb_features.configure(state = 'normal')

        def feature_lb_newselection(self, event):
            owner = event.widget
            if self.operation != 'N':
                pass
            else:
                self.value_of_combo = owner.get(owner.curselection())
                self.dialog_text.set("You have chosen - " + self.value_of_combo.capitalize())
                self.update_feature_data_explorer(self.value_of_combo)

        def update_feature_data_explorer(self, feature_name):
            properties = self.datasets[self.current_dataset].features[feature_name][1]
            op_list = ["{} : {}".format(k,v) for k, v in properties.items()]
            self.lb_feature_data_source.set(op_list)
            self.lb_feature_data.configure(state = 'normal')

        def confirm(self, data_lines): # this acts as a confirm for selection of data, and returns to
                                 # origin function with the data selected
            if self.operation == 'M':
                items = [self.lb_features.get(i) for i in data_lines]
                data = [self.datasets[self.current_dataset].features[feature_name][0]
                        for feature_name in items]
                self.merge_polys(data, items)
            #elif

        def merge_polys(self, data = None, *args):
            # allows the feature listbox to become enabled for multiple selections
            # and waits for items to be selected and confirmed
            if data == None:
                self.lb_feature_data_source.set([])
                self.btn_feature_display.configure(state = 'disabled')
                self.lb_features.configure(selectmode = 'multiple')
                self.operation = 'M'
                self.btn_confirm.configure(state = 'normal')
                self.dialog_text.set('Please confirm when you have selected your items')
                pass
            else: # this is the return from the confirm button
                merged_geom = cascaded_union(data)
                name = 'merged' + str(self.op_counter)
                self.display(None, merged_geom, name)
                self.make_merged_shp(merged_geom, name = args[0]) # this makes a shapefile
                self.btn_confirm.configure(state = 'disabled')
                self.lb_features.configure(selectmode = 'single')
                self.btn_feature_display.configure(state = 'normal')
                self.btn_confirm.configure(state = 'disabled')
                self.points_within_poly(merged_geom)
                self.centroid(merged_geom)


        def points_within_poly(self, poly):
            if 'dit:geonames_pop_5000' in self.datasets.keys():
                self.current_dataset = 'dit:geonames_pop_5000'
            elif 'dit:geonames_populated' in self.datasets.keys():
                self.current_dataset = 'towns'
            else:
                self.dialog_text.set('Please return to last GUI and pick a point dataset:')
                pass
            points = self.datasets[self.current_dataset].features
            print(len(points))
            contained_points = {}
            for k,v in points.items():
                if poly.contains(v[0]):
                    contained_points[k] = v
            # it works!!!

        def centroid(self, geom):
            pass

        def make_shp(self):
            pass


        def make_merged_shp(self, data, name, crs = None):
            self.op_counter += 1
            geom_type = data.geom_type
            a_schema = {'geometry': geom_type,
                        'properties': {'name':'str'}
                       }
            filename = 'merged' + str(self.op_counter) + ".shp"
            path = os.path.join('op_data',filename)
            obj_name = 'merged' + str(self.op_counter)
            if not crs:
                my_crs = self.datasets[self.current_dataset].crs
                crs = from_epsg(my_crs['properties']['code'])
            with fiona.open(path,
                            'w',
                            driver= 'ESRI Shapefile',
                            crs= crs,
                            schema= a_schema) as c:
                c.write({
                    'properties':{'name':obj_name},
                      'geometry':geometry.mapping(data)})



        def geocode(self):
            pass


class LoadingGUI():
    def __init__(self, master):
        self.master = master
        self.master.title("Dataset selection")

        master.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        # Set Button style
        s = ttk.Style()
        s.configure('Wait.TButton',foreground = 'red', state = 'disabled')
        s.configure('Go.TButton', foreground = 'green', state = 'active')

        # Initialise variables here
        self.base_params = {'host': "mf2.dit.ie:8080",
                            'layer': "cso:ctygeom",
                            'srs_code': 29902,
                            'properties': "",
                            'geom_field': "",
                            'filter_property': "",
                            'filter_values': ""} # dict to store the  fetch params

        self.param1 = StringVar()
        self.param2 = StringVar()
        self.param3 = StringVar()
        self.param4 = StringVar()
        self.param5 = StringVar()
        self.param6 = StringVar()
        self.param7 = StringVar()

        self.params_list = [self.param1,
                            self.param2,
                            self.param3,
                            self.param4,
                            self.param5,
                            self.param6,
                            self.param7] # list to allow iterative assignment and retrieval of
        # params

        self.gj_stack =  defaultdict(list) #out_stack to store geojson objects retrieved
        self.prop_list = StringVar()
        self.prop_sample = StringVar()
        self.prop_sample.set('Data values will appear here')
        self.feature_property = StringVar()
        self.out_stack = []
        self.stack_text = []
        self.lv_stack = StringVar()

        # Initialise the widgets
        self.mainframe = ttk.Frame(self.master)
        self.label1 = ttk.Label(self.mainframe,
                                text = "THIS GUI SUPPORTS INTERACTION WITH\n"+
                                       "A GEOSERVER.",
                                foreground = 'black',
                                relief = 'sunken',
                                font =('Helvetica', '12'),
                                justify = 'center',
                                anchor = 'center')
        self.label2 = ttk.Label(self.mainframe,
                                text = "Please use buttons to select datasets or enter custom\n"
                                       + "parameters using the boxes on the left",
                                foreground = 'blue',
                                relief = 'sunken',
                                anchor = 'center')
        self.entry_frame = ttk.LabelFrame(self.mainframe,
                                          text = 'Enter parameters here:',
                                          relief = 'sunken')
        self.display_frame = ttk.LabelFrame(self.mainframe,
                                            text = 'Current Parameters:',
                                            relief = 'sunken',
                                            width = 30)
        self.button_frame = ttk.LabelFrame(self.mainframe,
                                           text = 'Select one of the datasets\n' +
                                                  'by clicking the button',
                                           relief = 'sunken')
        self.geojson_nav_frame = ttk.LabelFrame(self.mainframe,
                                                text = 'Please explore the gj_stack here',
                                                relief = 'sunken')

        self.entry1 = ttk.Entry(self.entry_frame,
                                textvariable = self.param1)
        self.entry2 = ttk.Entry(self.entry_frame,
                                textvariable = self.param2)
        self.entry3 = ttk.Entry(self.entry_frame,
                                textvariable = self.param3)
        self.entry4 = ttk.Entry(self.entry_frame,
                                textvariable = self.param4)
        self.entry5 = ttk.Entry(self.entry_frame,
                                textvariable = self.param5)
        self.entry6 = ttk.Entry(self.entry_frame,
                                textvariable = self.param6)
        self.entry7 = ttk.Entry(self.entry_frame,
                                textvariable = self.param7)
        self.lbl_p1 = ttk.Label(self.entry_frame,
                                foreground = 'green',
                                text = 'host:')
        self.lbl_p2 = ttk.Label(self.entry_frame,
                                foreground = 'green',
                                text = 'layer')
        self.lbl_p3 = ttk.Label(self.entry_frame,
                                foreground = 'green',
                                text = 'spatial ref:')
        self.lbl_p4 = ttk.Label(self.entry_frame,
                                foreground = 'green',
                                text = 'properties:')
        self.lbl_p5 = ttk.Label(self.entry_frame,
                                foreground = 'green',
                                text = 'geom field:')
        self.lbl_p6 = ttk.Label(self.entry_frame,
                                foreground = 'green',
                                text = 'filter field:')
        self.lbl_p7 = ttk.Label(self.entry_frame,
                                foreground = 'green',
                                text = 'filter criteria:')

        self.button_load_params = ttk.Button(self.entry_frame,
                                             text = "^ Load ^",
                                             command = self.load_params)

        self.display1 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  anchor = 'center',
                                  padding = 1)
        self.display2 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  anchor = 'center',
                                  padding = 1)
        self.display3 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  anchor = 'center',
                                  padding = 1)
        self.display4 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  anchor = 'center',
                                  padding = 1)
        self.display5 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  anchor = 'center',
                                  padding = 1)
        self.display6 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  anchor = 'center',
                                  padding = 1)
        self.display7 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  anchor = 'center',
                                  padding = 1)

        self.button_County = ttk.Button(self.button_frame,
                                        text = 'County Polygons',
                                        command = self.county_polygons,
                                        width = 30)
        self.button_Towns = ttk.Button(self.button_frame,
                                       text = 'Town Points',
                                       command = self.town_points,
                                       width = 30)
        self.button_LargeTowns = ttk.Button(self.button_frame,
                                            text = 'Large Town Points',
                                            command = self.large_town_points,
                                            width = 30)
        self.button_EDs = ttk.Button(self.button_frame,
                                     text = 'ED Polygons',
                                     command = self.ed_polygons,
                                     width = 30)
        self.button_Provinces = ttk.Button(self.button_frame,
                                           text = 'Province Polygons',
                                           command = self.province_polygons,
                                           width = 30)
        self.button_SAs = ttk.Button(self.button_frame,
                                     text = 'SA Polygons',
                                     command = self.sa_polygons,
                                     width = 30)
        self.button_Fetch = ttk.Button(self.display_frame,
                                       text = '^ FETCH ^',
                                       width = 40,
                                       command = self.fetch_geojson)

        # Bottom half of GUI

        self.l_frame = ttk.LabelFrame(self.mainframe,
                                      text = 'Pick dataset and choose feature identifier')
        self.r_frame = ttk.LabelFrame(self.mainframe,
                                      text= 'View out_stack here, and send to GIS')
        #todo add a labelframe to display the geojson obj metadata
        self.cb_dataset = ttk.Combobox(self.l_frame)
        self.lbl_properties = ttk.Label(self.l_frame,
                                        text = 'Feature properties')
        self.lb_properties = Listbox(self.l_frame,
                                     exportselection = 0,
                                     bd = 5,
                                     width = 40,
                                     selectmode = SINGLE,
                                     listvariable = self.prop_list,
                                     state = 'disabled'
                                     )
        self.lbl_example = ttk.Label(self.l_frame,
                                     textvariable = self.feature_property,
                                     foreground = 'red',
                                     background = 'white',
                                     relief = 'sunken',
                                     anchor = 'center',
                                     font =('Helvetica', '12'))
        self.lb_stack = Listbox(self.r_frame,
                                exportselection = 0,
                                bd = 5,
                                width = 40,
                                selectmode = SINGLE,
                                state = 'disabled',
                                listvariable = self.lv_stack
                                )
        self.button_confirm_send = ttk.Button(self.l_frame,
                                              text = 'Confirm and Add to Stack',
                                              command = self.confirm,
                                              )
        self.button_clear_stack = ttk.Button(self.r_frame,
                                             text = 'Clear Stack',
                                             command = self.clear_stack)
        self.button_gis_open = ttk.Button(self.r_frame,
                                          text = 'Open GIS with current Stack',
                                          command = lambda: self.open_gis(self.out_stack))
        self.info_text = ttk.Label(self.mainframe,
                                   text = 'Information messages will appear here',
                                   foreground = 'blue')

        # Layout the GUI

        self.mainframe.grid(row=0, column = 0)
        self.label1.grid(row = 0, column = 0, columnspan = 4, sticky = 'ew')
        self.entry_frame.grid(row = 2, column = 0, sticky = 'ns')
        self.lbl_p1.grid(row = 0, column = 0, sticky = 'ew')
        self.lbl_p2.grid(row = 1, column = 0, sticky = 'ew')
        self.lbl_p3.grid(row = 2, column = 0, sticky = 'ew')
        self.lbl_p4.grid(row = 3, column = 0, sticky = 'ew')
        self.lbl_p5.grid(row = 4, column = 0, sticky = 'ew')
        self.lbl_p6.grid(row = 5, column = 0, sticky = 'ew')
        self.lbl_p7.grid(row = 6, column = 0, sticky = 'ew')
        self.entry1.grid(row = 0, column = 1, sticky = 'ew')
        self.entry2.grid(row = 1, column = 1, sticky = 'ew')
        self.entry3.grid(row = 2, column = 1, sticky = 'ew')
        self.entry4.grid(row = 3, column = 1, sticky = 'ew')
        self.entry5.grid(row = 4, column = 1, sticky = 'ew')
        self.entry6.grid(row = 5, column = 1, sticky = 'ew')
        self.entry7.grid(row = 6, column = 1, sticky = 'ew')
        self.button_load_params.grid(row = 7, column = 1, sticky = 'ew')

        self.display_frame.grid(row = 2, column = 1, sticky = 'ns')
        self.display1.grid(row = 0, sticky = 'ew')
        self.display2.grid(row = 1, sticky = 'ew')
        self.display3.grid(row = 2, sticky = 'ew')
        self.display4.grid(row = 3, sticky = 'ew')
        self.display5.grid(row = 4, sticky = 'ew')
        self.display6.grid(row = 5, sticky = 'ew')
        self.display7.grid(row = 6, sticky = 'ew')
        self.button_Fetch.grid(row = 7, column = 0,
                               sticky = 'ew',
                               columnspan = 2)

        for child, i in zip(self.display_frame.winfo_children(), self.params_list):
            child.configure(text = i.get())

        self.button_frame.grid(row = 2, column = 2, sticky = 'ns')
        self.button_LargeTowns.grid(row = 0, sticky = 'ew')
        self.button_County.grid(row = 1, sticky = 'ew')
        self.button_EDs.grid(row = 2, sticky = 'ew')
        self.button_Provinces.grid(row = 3, sticky = 'ew')
        self.button_SAs.grid(row = 4, sticky = 'ew')
        self.button_Towns.grid(row = 5, sticky = 'ew')
        self.l_frame.grid(row = 3, column = 0, sticky = 'ew')
        self.r_frame.grid(row = 3, column = 1,
                          sticky = 'ew',
                          columnspan = 2)
        self.cb_dataset.grid(row = 1, sticky = 'ew')
        self.lbl_properties.grid(row = 2)
        self.lb_properties.grid(row = 3, sticky = 'sew')
        self.button_confirm_send.grid(row = 4, column = 0, sticky ='ew')
        self.lbl_example.grid(row = 3, column = 0, sticky = 'sew')
        self.lb_stack.grid(row = 1, column = 0, sticky = 'sw')
        self.button_gis_open.grid(row = 2, column = 0,
                                  sticky = 'sew')
        self.button_clear_stack.grid(row = 3, column = 0,
                                     sticky = 'sew')
        self.info_text.grid(row = 4, columnspan = 4)

        # Event Management
        self.cb_dataset.bind("<<ComboboxSelected>>", self.cb_dataset_selection)
        self.lb_properties.bind("<<ListboxSelect>>", self.item_selection)


    def clear_stack(self):
        self.out_stack = []
        self.stack_text = []
        self.lv_stack.set('')

    def item_selection(self, event):
        owner = event.widget
        item = owner.get(owner.curselection())
        current_dataset = self.gj_stack[self.cb_dataset.get()]
        item_str = str(current_dataset['features'][0]['properties'][item])
        if len(item_str) > 30:
            item_str = "{}{}".format(item_str[:25],'....')
        self.feature_property.set(item_str)


    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.master.destroy()

    def cb_dataset_selection(self, event):
        owner = event.widget
        feature_props = self.gj_stack[owner.get()]['features'][0]['properties']
        self.prop_list.set(list(feature_props))
        self.lb_properties.configure(state = 'normal')

    def confirm(self):
        #todo add exception handling for no item selected
        ds_name = self.cb_dataset.get()
        current_dataset = self.gj_stack[ds_name]
        if ds_name in [i[2] for i in self.out_stack]:
            messagebox.showerror('Info','The dataset is already in the out_stack')
            pass
        else:
            try:
                feature_name = self.lb_properties.get(self.lb_properties.curselection())
                self.out_stack.append([current_dataset, feature_name, ds_name])
                #todo format the below string to align nicely
                self.stack_text.append('Dataset: {} --\t\t Feature Name: {}'.format(ds_name,feature_name))
                self.lv_stack.set(self.stack_text)
                self.info_text.configure(text = 'Please examine the item.')
            except TclError:
                self.info_text.configure(text = 'There is no item selected.')


    def open_gis(self, stack):
        op_dict = defaultdict()
        if stack:
            for obj in stack:
                op_dict[obj[2]] = MyShape(obj[0],obj[1])
            self.new_window = Toplevel(self.master)
            self.my_gis = MicksGis(self.new_window, op_dict)


        else:
            self.info_text.set('Please highlight the feature name and send again:')
            pass


    def load_params(self):
        for child, i in zip(self.display_frame.winfo_children(), self.params_list):
            child.configure(text = i.get())

    def county_polygons(self):
        self.params_list[1].set('cso:ctygeom')
        self.load_params()

    def town_points(self):
        self.params_list[1].set('dit:geonames_populated')
        self.load_params()

    def sa_polygons(self):
        self.params_list[1].set('cso:sageom')
        self.load_params()

    def large_town_points(self):
        self.params_list[1].set('dit:geonames_pop_5000')
        self.load_params()

    def province_polygons(self):
        self.params_list[1].set('cso:prgeom')
        self.load_params()

    def ed_polygons(self):
        self.params_list[1].set('cso:edgeom')
        self.load_params()

    def fetch_geojson(self):

        #TODO Set styles to show when gj_stack is loading
        try:
            self.info_text.configure(text = 'LOADING DATA....',
                                 foreground = 'red')
            self.mainframe.update_idletasks()
            btn = self.button_Fetch
            btn.configure(style = 'Wait.TButton')
            self.param1.set(self.base_params['host'])
            self.param3.set(self.base_params['srs_code'])
            self.param4.set(self.base_params['properties'])
            self.param5.set(self.base_params['geom_field'])
            self.param6.set(self.base_params['filter_property'])
            self.param7.set(self.base_params['filter_values'])
            self.base_params['host'] = self.param1.get()
            self.base_params['layer'] = self.param2.get()
            self.base_params['srs_code'] = self.param3.get()
            self.base_params['properties'] = self.param4.get()
            self.base_params['geom_field'] = self.param5.get()
            self.base_params['filter_property'] = self.param6.get()
            self.base_params['filter_values'] = self.param7.get()
            gj = self.get_geojson(self.base_params)
            # create a out_stack of the geojson objects, only storing each one once
            self.gj_stack[self.base_params['layer']] = gj
            self.info_text.configure(text = 'Request Executed Successfully',
                                     foreground = 'green')
            self.cb_dataset['values'] = [i for i in self.gj_stack.keys()]
        except Exception:
            self.info_text.configure(text = 'Error With Request Parameters: Please Try Again',
                                     foreground = 'red')


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


if __name__ == '__main__':
    main()