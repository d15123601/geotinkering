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


def main():
    root = Tk()
    LoadingGUI(root)
    root.mainloop()


class MyShape():
    #todo add methods to reproject, perform geometric functions etc.
    def __init__(self, geojson_obj, feature_id):
        from shapely import geometry
        self.crs = geojson_obj['crs']
        self.bbox = geojson_obj['bbox']
        self.features = [(f['properties'][feature_id],
                          geometry.asShape(f['geometry']),
                          f['properties']) for f in geojson_obj['features']]


class GisGui():
    def __init__(self, master, input_datasets):
        # variables
        self.dataset_ref = ""
        self.ops_output = {}

        self.dialog_text = StringVar()
        self.dialog_text.set("Messages will display here")

        self.dataset_list = [keys for keys in input_datasets.keys()]
        self.dataset = input_datasets
        self.cb_list = ['No gj_stack loaded']

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
            self.my_gis = GisGui(self.new_window, op_dict)
            LoadingGUI.catch_destroy()

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