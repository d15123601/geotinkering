from tkinter import *
from tkinter import ttk


class myGUI:
    def __init__(self, master):
        # variables
        self.dataset_ref = ""
        self.ops_output = {}

        self.dialog_text = StringVar()
        self.dialog_text.set("Messages will display here")

        self.cb_list = ['Tipperary', 'Mayo']
        self.dataset_list = ['Counties', 'Towns']

        self.ops_subject = StringVar()
        self.ops_subject.set('Tipperary\n Mayo')

        # GUI creation
        self.master = master

        self.main_frame = ttk.Frame(self.master)
        self.main_frame.grid(column = 0, row = 0, sticky = (N, S, E, W))

        self.dialog = ttk.Label(self.main_frame, textvariable = self.dialog_text,
                                foreground = 'cyan',
                                background = 'blue', anchor = 'center')
        self.dialog.grid(row = 0, column = 0, columnspan = 3)

        self.selection_box = ttk.Labelframe(self.main_frame, text = 'Object Picker',
                                width = 250, height = 500, borderwidth = 5,
                                relief = 'sunken')
        self.selection_box.grid(row = 1, column = 0, sticky = 'ns')

        self.dataset_box = ttk.Labelframe(self.selection_box, text = 'Dataset Picker',
                                width = 250, height = 100, borderwidth = 5,
                                relief = 'sunken')
        self.dataset_box.grid(row = 0, column = 0, sticky = 'ns')
        ttk.Label(self.dataset_box, text = 'Please choose a dataset from the list:',
                  foreground = 'red', justify = 'left').grid(row = 0, column = 0)
        self.datacb = ttk.Combobox(self.dataset_box, values= self.dataset_list, state='readonly')
        self.datacb.current(1)
        self.datacb.grid(row = 1, column = 0, sticky = 'nsew')
        # set the selection event
        self.datacb.bind("<<ComboboxSelected>>", self.newselection)

        self.cb_box = ttk.Labelframe(self.selection_box, text = 'Item Picker',
                                width = 250, height = 400, borderwidth = 5,
                                relief = 'sunken')
        self.cb_box.grid(sticky = 'nsew')
        ttk.Label(self.cb_box, text = 'Please choose an item from the list:',
                  foreground = 'red', justify = 'left').grid(row = 0, column = 0)
        self.itemcb = ttk.Combobox(self.cb_box, values= self.cb_list, state='readonly')
        self.itemcb.current(1)
        self.itemcb.grid(row = 1, column = 0, sticky = 'nsew')
        # set the selection event
        self.itemcb.bind("<<ComboboxSelected>>", self.newselection)

        self.op_box = ttk.Labelframe(self.main_frame, text = 'Operations',
                                    width = 250, height = 500,
                                    borderwidth = 5,
                                    relief = 'sunken')
        self.op_box.grid(row = 1, column = 1, sticky = 'ns')

        self.btn_add = ttk.Button(self.op_box, width = 50, text = 'Add', command = self.choose_selected)
        self.btn_add.grid(row = 0, column = 0)

        self.btn_merge = ttk.Button(self.op_box, width = 50, text = 'Merge',
                                    command = self.merge_chosen, state = 'disabled')
        self.btn_merge.grid(row = 1, column = 0)

        self.btn_geocode = ttk.Button(self.op_box, width = 50, text = 'Geocode',
                                    command = self.geocode_chosen, state = 'disabled')
        self.btn_geocode.grid(row = 2, column = 0)

        self.btn_centroid = ttk.Button(self.op_box, width = 50, text = 'Centroid',
                                    command = self.centroid_chosen, state = 'disabled')
        self.btn_centroid.grid(row = 3, column = 0)

        self.btn_convexhull = ttk.Button(self.op_box, width = 50, text = 'Make Convex Hull',
                                    command = self.convex_hull, state = 'disabled')
        self.btn_convexhull.grid(row = 4, column = 0)

        self.btn_line_join = ttk.Button(self.op_box, width = 50, text = 'Join with line',
                                    command = self.line_join, state = 'disabled')
        self.btn_line_join.grid(row = 5, column = 0)

        self.ops_frame = ttk.Labelframe(self.op_box, text = 'Items selected:',
                                        relief = 'sunken')
        self.ops_frame.grid(sticky = 'nsew')
        self.subject_list = ttk.Label(self.ops_frame, textvariable = self.ops_subject,
                                      anchor = 'w')
        self.subject_list.grid(sticky = 'nsew')


        self.display_box = ttk.Labelframe(self.main_frame, text = 'Object Display',
                                width = 500, height = 500, borderwidth = 5,
                                relief = 'sunken')
        self.display_box.grid(row = 1, column = 2, sticky = 'ns')

    def newselection(self, event):
        self.value_of_combo = self.cb.get()
        self.dialog_text.set("You have chosen " + self.value_of_combo)
        return self.value_of_combo


    def add_cb_value(self):
        self.cty = str(self.newselection)
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

root = Tk()
myGUI(root)
root.mainloop()