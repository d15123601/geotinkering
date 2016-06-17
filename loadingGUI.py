from tkinter import *
from tkinter import ttk
from collections import defaultdict
from tkinter import messagebox


class loadingGUI():
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
        self.gis_stack_text = StringVar()
        self.info_text = StringVar()
        self.selected_item = StringVar()
        self.meta_list = StringVar()
        self.data_headings_list = StringVar()
        self.data_item = StringVar()
        self.data_dict = {}

        self.gis_stack = [] # out_stack to store items to send to GIS

        self.params_list = [self.param1,
                            self.param2,
                            self.param3,
                            self.param4,
                            self.param5,
                            self.param6,
                            self.param7] # list to allow iterative assignment and retrieval of
                                    # params

        self.gj_stack =  defaultdict(list) #out_stack to store geojson objects retrieved

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
                                          relief = 'sunken')
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
                                        command = self.county_polygons)
        self.button_Towns = ttk.Button(self.button_frame,
                                       text = 'Town Points',
                                       command = self.town_points)
        self.button_LargeTowns = ttk.Button(self.button_frame,
                                            text = 'Large Town Points',
                                            command = self.large_town_points)
        self.button_EDs = ttk.Button(self.button_frame,
                                     text = 'ED Polygons',
                                     command = self.ed_polygons)
        self.button_Provinces = ttk.Button(self.button_frame,
                                           text = 'Province Polygons',
                                           command = self.province_polygons)
        self.button_SAs = ttk.Button(self.button_frame,
                                     text = 'SA Polygons',
                                     command = self.sa_polygons)
        self.button_Fetch = ttk.Button(self.display_frame,
                                       text = '^ FETCH ^',
                                       command = self.fetch_geojson)

        self.geoj_cb = ttk.Combobox(self.geojson_nav_frame,
                                    state = 'disabled')
        self.button_gis_stack = ttk.Button(self.geojson_nav_frame,
                                          text = 'Add to GIS Stack',
                                          style = 'Go.TButton',
                                          command = self.add_to_stack)
        self.button_inspect_item = ttk.Button(self.geojson_nav_frame,
                                              text = 'Inspect Item',
                                              style = 'Wait.TButton',
                                              command = self.inspect_item)

        self.lbl_data1 = ttk.Label(self.geojson_nav_frame,
                                  foreground = 'blue',
                                  anchor = 'center',
                                  text = 'Top Level Properties')
        self.lbl_data2 = ttk.Label(self.geojson_nav_frame,
                                  foreground = 'blue',
                                  anchor = 'center',
                                  text = 'Feature Properties')
        self.frm_geoj_op = ttk.Frame(self.geojson_nav_frame)
        self.lbl_data_example = ttk.Label(self.frm_geoj_op,
                                          foreground = 'blue',
                                          anchor = 'center',
                                          text = 'Example Properties')
        self.meta_tb = Listbox(self.geojson_nav_frame,
                               exportselection = 0,
                               bd = 5,
                               width = 40,
                               selectmode = SINGLE,
                               listvariable = self.meta_list
                               )
        self.data_tb = Listbox(self.geojson_nav_frame,
                               exportselection = 0,
                               bd = 5,
                               width = 20,
                               selectmode = SINGLE,
                               listvariable = self.data_headings_list
                               )
        self.lbl_gis_stack = ttk.Label(self.frm_geoj_op,
                                       text = 'GIS Stack',
                                       foreground = 'blue')
        self.tb_data = ttk.Label(self.frm_geoj_op,
                                 textvariable = self.data_item,
                                 relief = 'sunken',
                                 background = 'white',
                                )
        self.tb_geoj_stack = ttk.Label(self.frm_geoj_op,
                                 textvariable = self.gis_stack_text,
                                 relief = 'sunken',
                                 background = 'white',
                                )
        self.info_label = Label(self.mainframe,
                                textvariable = self.info_text,
                                relief = 'sunken',
                                anchor = 'center')
        self.info_text.set('Use the dialog above to explore the datasets')

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
        self.button_Fetch.grid(row = 7, column = 0,
                               columnspan= 2,
                               sticky = 'ew')
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

        for child, i in zip(self.display_frame.winfo_children(), self.params_list):
            child.configure(text = i.get())

        self.button_frame.grid(row = 2, column = 2, sticky = 'ns')
        self.button_LargeTowns.grid(row = 0, sticky = 'ew')
        self.button_County.grid(row = 1, sticky = 'ew')
        self.button_EDs.grid(row = 2, sticky = 'ew')
        self.button_Provinces.grid(row = 3, sticky = 'ew')
        self.button_SAs.grid(row = 4, sticky = 'ew')
        self.button_Towns.grid(row = 5, sticky = 'ew')

        self.geojson_nav_frame.grid(row = 3, column = 0,
                                    columnspan = 4, sticky = 'ew')
        self.frm_geoj_op.grid(row = 2, column = 2, stick = 'n')
        self.geoj_cb.grid(row = 0, column = 0,
                          columnspan = 2, sticky = 'nw')
        self.button_inspect_item.grid(row = 0, column = 1)
        self.button_gis_stack.grid(row = 0, column = 2)
        self.lbl_data1.grid(row = 1, column = 0)
        self.lbl_data2.grid(row = 1, column = 1)
        self.meta_tb.grid(row = 2, column = 0)
        self.data_tb.grid(row = 2, column = 1)
        self.lbl_data_example.grid(row = 0, column = 0, sticky = 'new')
        self.tb_data.grid(row = 1, column = 0, sticky = 'new')
        self.lbl_gis_stack.grid(row = 2, column = 0, sticky ='new')
        self.tb_geoj_stack.grid(row = 3, column = 0, sticky = 'nsew')


        self.label2.grid(row = 1, column = 0, columnspan = 4, sticky = 'ew')
        self.info_label.grid(row = 4, column = 0, columnspan = 4, sticky = 'ew')



        #Event handling
        self.geoj_cb_value = self.geoj_cb.bind("<<ComboboxSelected>>", self.geoj_cb_selection)
        self.data_tb_value = self.data_tb.bind("<<ListboxSelect>>", self.item_selection)

    def geoj_cb_selection(self, event):
        #TODO function which blanks the display boxes when this changes
        owner = event.widget
        self.selected_item.set(owner.get())

    def item_selection(self, event):
        owner = event.widget
        line = owner.get(owner.curselection())
        item_str = str(self.data_dict[line])
        if len(item_str) > 30:
            item_str = "{}{}".format(item_str[:25],'....')
        self.data_item.set(item_str)


    def add_to_stack(self):
        new_item = self.selected_item.get()
        stack_contents = self.gis_stack_text.get()
        if new_item in stack_contents:
            self.info_text.set('You already have this item in the out_stack;\n' +
                               'Please choose anoher or proceed to GIS')
            pass
        else:
            self.gis_stack.append(self.gj_stack[new_item])
            self.gis_stack_text.set(stack_contents + new_item + '\n')

    def inspect_item(self):
        if self.selected_item.get() != "":
            item = self.gj_stack[self.selected_item.get()]
            meta, data_hdgs, data_dict = self.geoj_exploder(item)
            self.meta_list.set(meta)
            self.data_headings_list.set(data_hdgs)
            self.data_dict = data_dict
            self.info_text.set('Please select the name of the feature from the Feature Properties list')
        else:
            self.info_text.set('There is no item selected.')
            pass

    def geoj_exploder(self, gj_obj):
        l1 = [(k,v) for k,v in gj_obj.items()]
        i = gj_obj['features'][0]['properties']
        l2 = list(i.keys())
        d = i
        return [l1, l2, d]

    def send_to_gis(self):
        #TODO add check to see if feature name is highlighted
        #TODO add item to hold best name of feature
        if self.data_item.get() == '':
            self.info_text.set('Please highlight the feature name and send again:')
            pass
        else:
            item = self.gj_stack[self.selected_item.get()]
            self.gis_stack.append(item)

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
        self.update_geoj_cb(self.gj_stack)

    def update_geoj_cb(self, adict):
        self.geoj_cb['values'] = [i for i in adict.keys()]
        self.geoj_cb.state(['!disabled', 'readonly'])

    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.master.destroy()

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

def main():
    root = Tk()
    loadingGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()