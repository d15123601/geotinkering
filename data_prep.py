from tkinter import *
from tkinter import ttk
from collections import defaultdict
from tkinter import messagebox
import json
"""
pass the dict of geojson objects to this gui in order to do some preprocessing of the data.
specifically, we want the user to define the parameter that stores the name for each feature,
to make each feature more user friendly in downstream processes. Each dataset will have this
defined and then the GUI for manipulating the data will be opened.
"""
class data_prep:
    def __init__(self, parent, data):
        self.data = data
        self.parent = parent
        self.parent.title('Data Preparation')

        self.parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self.sv_dialog = StringVar()
        self.prop_list = StringVar()

        self.mainframe = ttk.Frame(self.parent)
        self.dialog = ttk.Label(self.mainframe,
                                textvariable = self.sv_dialog,
                                foreground = 'blue',
                                relief = 'sunken')
        self.sv_dialog.set('Please choose the best name for the features of each dataset')
        self.cb_dataset = ttk.Combobox(self.mainframe,)
        self.cb_dataset['values'] = [i for i in self.data.keys()]
        self.cb_dataset.bind("<<ComboboxSelected>>", self.cb_dataset_selection)

        self.lb_properties = Listbox(self.mainframe,
                                     exportselection = 0,
                                     bd = 5,
                                     width = 40,
                                     selectmode = SINGLE,
                                     listvariable = self.prop_list,
                                     state = 'disabled'
                                     )

        self.mainframe.grid(row =0, column = 0)
        self.dialog.grid(row = 0, sticky = 'ew')
        self.cb_dataset.grid(row = 1, column = 0, sticky = 'new')
        self.lb_properties.grid(row = 2, column = 0, sticky = 'sew')


    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()

    def cb_dataset_selection(self, event):
        owner = event.widget
        feature_props = self.data[owner.get()]['features'][0]['properties']
        self.prop_list.set(list(feature_props))
        self.lb_properties.configure(state = 'normal')



def main():
    root = Tk()
    with open("cso_counties.txt",'r') as f1:
        cty_str = f1.read()

    with open("geonames_pop.txt",'r') as f2:
        pop_str = f2.read()

    cty_polygons = json.loads(cty_str)
    places_pts = json.loads(pop_str)
    datasets = {}
    datasets['ctys'] = cty_polygons
    datasets['places'] = places_pts
    data_prep(root, datasets)
    root.mainloop()


if __name__ == '__main__':
    main()