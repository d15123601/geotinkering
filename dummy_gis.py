"""
This is a dummy to try and get a gis gui up and running
"""
from GUI_1 import MyShape
import json
from collections import defaultdict
from tkinter import *
from tkinter import ttk


def main():
    with open("cso_counties.txt",'r') as f1:
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


class MicksGis():
    """
    This class will construct the gis gui.
    We pass in the collection of MyShape objects.
    """
    def __init__(self, master, datasets):
        self.master = master

        # Declaring variables


        # widget declarations
        self.frm_mainframe = ttk.Frame(self.master,
                                   )
        self.lbl_message = ttk.Label(self.frm_mainframe,
                                     text = 'This is the GIS App')


        # widget placement
        self.frm_mainframe.grid(row = 0, column = 0)
        self.lbl_message.grid(row = 0, column = 0)




if __name__ == main():
    main()







