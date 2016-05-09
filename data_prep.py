from tkinter import *
from tkinter import ttk
from collections import defaultdict
from tkinter import messagebox
import json
"""
pass the dict of geojson objects to this gui in order to do some preprocessing of the gj_stack.
specifically, we want the user to define the parameter that stores the name for each feature,
to make each feature more user friendly in downstream processes. Each dataset will have this
defined and then the GUI for manipulating the gj_stack will be opened.
"""
class data_prep:
    def __init__(self, parent, data):
        self.data = data
        self.parent = parent
        self.parent.title('Data Preparation')

        self.parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self.sv_dialog = StringVar()
        self.prop_list = StringVar()
        self.prop_sample = StringVar()
        self.prop_sample.set('Data values will appear here')
        self.feature_property = StringVar()
        self.stack = []
        self.stack_text = []
        self.lv_stack = StringVar()

        self.mainframe = ttk.Frame(self.parent)
        self.l_frame = ttk.LabelFrame(self.mainframe,
                                      text = 'Pick dataset and choose feature identifier')
        self.r_frame = ttk.LabelFrame(self.mainframe,
                                      text= 'View stack here, and send to GIS')
        self.dialog = ttk.Label(self.mainframe,
                                textvariable = self.sv_dialog,
                                foreground = 'blue',
                                relief = 'sunken')
        self.sv_dialog.set('Please choose the best name for the features of each dataset')
        self.cb_dataset = ttk.Combobox(self.l_frame)
        self.cb_dataset['values'] = [i for i in self.data.keys()]
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
        self.btn_confirm_send = ttk.Button(self.l_frame,
                                           text = 'Confirm and Add to Stack',
                                           command = self.confirm,
                                           )
        self.btn_clear_stack = ttk.Button(self.r_frame,
                                          text = 'Clear Stack',
                                          command = self.clear_stack)
        self.btn_gis_open = ttk.Button(self.r_frame,
                                       text = 'Open GIS with selected gj_stack',
                                       command = self.open_gis)

        self.mainframe.grid(row =0, column = 0, sticky = 'nsew')
        self.l_frame.grid(row = 1, column = 0, sticky = 'new')
        self.r_frame.grid(row = 1, column = 1, sticky = 'new')
        self.dialog.grid(row = 0, columnspan = 2, sticky = 'new')
        self.cb_dataset.grid(row = 1, sticky = 'ew')
        self.lbl_properties.grid(row = 2)
        self.lb_properties.grid(row = 3, sticky = 'sew')
        self.btn_confirm_send.grid(row = 4, column = 0, sticky ='ew')
        self.lbl_example.grid(row = 3, column = 0, sticky = 'sew')
        self.lb_stack.grid(row = 1, column = 0, sticky = 'nw')
        self.btn_gis_open.grid(row = 2, column = 0,
                               sticky = 'sew')
        self.btn_clear_stack.grid(row = 3, column = 0,
                               sticky = 'sew')

        # Event Management
        self.cb_dataset.bind("<<ComboboxSelected>>", self.cb_dataset_selection)
        self.lb_properties.bind("<<ListboxSelect>>", self.item_selection)


    def clear_stack(self):
        self.stack = []
        self.stack_text = []
        self.lv_stack.set('')

    def item_selection(self, event):
        owner = event.widget
        item = owner.get(owner.curselection())
        current_dataset = self.data[self.cb_dataset.get()]
        item_str = str(current_dataset['features'][0]['properties'][item])
        if len(item_str) > 30:
            item_str = "{}{}".format(item_str[:25],'....')
        self.feature_property.set(item_str)


    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()

    def cb_dataset_selection(self, event):
        owner = event.widget
        feature_props = self.data[owner.get()]['features'][0]['properties']
        self.prop_list.set(list(feature_props))
        self.lb_properties.configure(state = 'normal')

    def confirm(self):
        ds_name = self.cb_dataset.get()
        current_dataset = self.data[ds_name]
        if ds_name in [i[2] for i in self.stack]:
            messagebox.showerror('Info','The dataset is already in the stack')
            pass
        else:
            feature_name = self.lb_properties.get(self.lb_properties.curselection())
            self.stack.append([current_dataset, feature_name, ds_name])
            #todo format the below string to align nicely
            self.stack_text.append('Dataset: {} --\t\t Feature Name: {}'.format(ds_name,feature_name))
            self.lv_stack.set(self.stack_text)

    def open_gis(self):
        pass


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