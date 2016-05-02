from tkinter import *
from tkinter import ttk


class loadingGUI():
    def __init__(self, master):
        self.master = master
        self.master.title("Dataset selection")


        # Initialise variables here
        self.base_params = {'host': "mf2.dit.ie:8080",
                       'layer': "cso:ctygeom",
                       'srs_code': 29902,
                       'properties': "",
                       'geom_field': "",
                       'filter_property': "",
                       'filter_values': ""}

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
                       self.param7]

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
                                + "parameters in the boxes to the left",
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

        self.param1.set(self.base_params['host'])
        self.param2.set(self.base_params['layer'])
        self.param3.set(self.base_params['srs_code'])
        self.param4.set(self.base_params['properties'])
        self.param5.set(self.base_params['geom_field'])
        self.param6.set(self.base_params['filter_property'])
        self.param7.set(self.base_params['filter_values'])

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
        self.button_Towns =  ttk.Button(self.button_frame,
                                        text = 'Town Points',
                                        command = self.town_points)
        self.button_LargeTowns =  ttk.Button(self.button_frame,
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

        self.mainframe.grid(row=0, column = 0)
        self.label1.grid(row = 0, column = 0, columnspan = 4, sticky = 'ew')
        self.label2.grid(row = 3, column = 0, columnspan = 4, sticky = 'ew')
        self.entry_frame.grid(row = 1, column = 0, sticky = 'ns')
        self.lbl_p1.grid(row = 0, column = 0)
        self.lbl_p2.grid(row = 1, column = 0)
        self.lbl_p3.grid(row = 2, column = 0)
        self.lbl_p4.grid(row = 3, column = 0)
        self.lbl_p5.grid(row = 4, column = 0)
        self.lbl_p6.grid(row = 5, column = 0)
        self.lbl_p7.grid(row = 6, column = 0)
        self.button_Fetch.grid(row = 7, column = 0)
        self.entry1.grid(row = 0, column = 1, sticky = 'ew')
        self.entry2.grid(row = 1, column = 1, sticky = 'ew')
        self.entry3.grid(row = 2, column = 1, sticky = 'ew')
        self.entry4.grid(row = 3, column = 1, sticky = 'ew')
        self.entry5.grid(row = 4, column = 1, sticky = 'ew')
        self.entry6.grid(row = 5, column = 1, sticky = 'ew')
        self.entry7.grid(row = 6, column = 1, sticky = 'ew')
        self.button_load_params.grid(row = 7, column = 1, sticky = 'ew')

        self.display_frame.grid(row = 1, column = 1, sticky = 'ns')
        self.display1.grid(row = 0, sticky = 'ew')
        self.display2.grid(row = 1, sticky = 'ew')
        self.display3.grid(row = 2, sticky = 'ew')
        self.display4.grid(row = 3, sticky = 'ew')
        self.display5.grid(row = 4, sticky = 'ew')
        self.display6.grid(row = 5, sticky = 'ew')
        self.display7.grid(row = 6, sticky = 'ew')

        for child, i in zip(self.display_frame.winfo_children(), self.params_list):
            child.configure(text = i.get())

        self.button_frame.grid(row = 1, column = 2, sticky = 'ns')
        self.button_LargeTowns.grid(row = 0, sticky = 'ew')
        self.button_County.grid(row = 1, sticky = 'ew')
        self.button_EDs.grid(row = 2, sticky = 'ew')
        self.button_Provinces.grid(row = 3, sticky = 'ew')
        self.button_SAs.grid(row = 4, sticky = 'ew')
        self.button_Towns.grid(row = 5, sticky = 'ew')
        
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
        self.base_params['host'] = self.params_list[0].get()
        self.base_params['layer'] = self.params_list[1].get()
        self.base_params['srs_code'] = self.params_list[2].get()
        self.base_params['properties'] = self.params_list[3].get()
        self.base_params['geom_field'] = self.params_list[4].get()
        self.base_params['filter_property'] = self.params_list[5].get()
        self.base_params['filter_values'] = self.params_list[6].get()
        #for i in self.base_params.values(): print(i)
        gj = self.get_geojson(self.base_params)
        print('hi')

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
            # Geoserver only sends valid data in the requested format, in our case GeoJSON, so if we get a response back in
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