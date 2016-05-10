"""
This is a dummy to try and get a gis gui up and running
"""
from GUI_1 import MyShape
import json
from collections import defaultdict
from tkinter import *
from tkinter import ttk


def main():
    with open("cso_counties.txt", 'r') as f1:
        cty_str = f1.read()

    with open("geonames_pop.txt",'r') as f2:
        pop_str = f2.read()

    cty_polygons = json.loads(cty_str)
    places_pts = json.loads(pop_str)
    stack = []
    stack.append([cty_polygons, 'countyname', 'counties'])
    stack.append([places_pts, 'asciiname', 'towns'])

    gis_data = defaultdict()
    if stack:
        for obj in stack:
            gis_data[obj[2]] = MyShape(obj[0], obj[1])

    root = Tk()
    MicksGis(root, gis_data)
    root.mainloop()


class MicksGis:
    """
    This class will construct the gis gui.
    We pass in the collection of MyShape objects.
    """
    def __init__(self, master, datasets):
        self.master = master
        self.master.title("SIMPLE GIS")

        # Set Button style
        s = ttk.Style()
        s.configure('Wait.TButton',foreground = 'red', state = 'disabled')
        s.configure('Go.TButton', foreground = 'green', state = 'active')

        # Declaring variables
        self.cb_datasets_source = StringVar()
        self.lb_features_source = StringVar()
        self.lb_feature_data_source = StringVar()

        # widget declarations
        self.frm_mainframe = ttk.Frame(self.master,
                                   )
        self.lbl_message = ttk.Label(self.master,
                                     text = 'Messages will appear here.',
                                     font = ('Helvetica', 16),
                                     foreground = 'blue')

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
        self.frm_display = ttk.LabelFrame(self.frm_mainframe,
                                          text = 'Features Displayed Here',
                                          borderwidth = 5,
                                          relief = 'groove')
        
        #Set up widgets
            # Data selection and viewing
        self.cb_datasets = ttk.Combobox(self.frm_data_pane_top,
                                        height = 5,
                                        textvariable = self.cb_datasets_source,
                                        width = 40)
        self.lb_features = Listbox(self.frm_data_pane_middle,
                                   height = 10,
                                   listvariable = self.lb_features_source,
                                   width = 40)
        self.lb_feature_data = Listbox(self.frm_data_pane_bottom,
                                       height = 10,
                                       listvariable = self.lb_feature_data_source,
                                       width = 40)
            # Functions
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
        self.cb_datasets.grid(row = 0, column = 0, sticky = 'ew')

        self.frm_data_pane_middle.grid(row = 1, column = 0, sticky = 'w')
        self.lb_features.grid(row = 0, column = 0, sticky = 'ew')

        self.frm_data_pane_bottom.grid(row = 2, column = 0, sticky = 'w')
        self.lb_feature_data.grid(row = 0, column = 0, sticky = 'ew')

        self.frm_functions.grid(row = 3, column = 0,
                                columnspan = 5)
        self.btn_merge_polygons.grid(row = 0, column = 0)
        self.btn_points_within_poly.grid(row = 0, column = 1)
        self.btn_centroid.grid(row = 0, column = 2)
        self.btn_make_shp.grid(row = 0, column = 3)
        self.geocode.grid(row = 0, column = 4)
        self.frm_display.grid(row = 0, column = 2,
                              rowspan = 2,
                              columnspan = 2)

        # functions
    def merge_polys(self):
        pass
    def points_within_poly(self):
        pass
    def centroid(self):
        pass
    def make_shp(self):
        pass
    def geocode(self):
        pass


if __name__ == main():
    main()







