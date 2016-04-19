from tkinter import *
from tkinter import ttk as ttk
from tkinter import messagebox

# Variables
stack = []


class GUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Simple GIS")

        cb_list = ['Mayo', 'Tipperary', 'Cork', 'Galway']

        parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        self.container1 = ttk.Frame(parent, padding = 5, border = 1)

        cb_panel_label = LabelFrame(self.container1, text = 'yayaya')
        cb_panel = Frame(self.container1)
        cb_panel.pack(side=TOP, fill=BOTH, expand=Y)

        cbp = ttk.Labelframe(cb_panel, text='Pre-defined List')
        cb = ttk.Combobox(cb_panel, values=cb_list, state='readonly')
        cb.current(1)  # set selection
        cb.pack(pady=5, padx=10)

        # position and display
        cbp.pack(in_=cb_panel, side=TOP, pady=5, padx=10, fill = 'y')

        # set the selection event
        cb.bind("<<ComboboxSelected>>", self.newselection)

        self.container2 = ttk.Frame(self.container1, padding = 5, border = 1)
        self.container2.pack(side=TOP, fill=BOTH, expand = Y)
        self.pick_btn = ttk.Button(self.container2, text = 'Add Selected', command = self.add_cb_value)
        self.pick_btn.grid(row = 0, column = 0)
        self.merge_btn = ttk.Button(self.container2, text = 'Merge Selected', command = self.merge_selected)
        self.merge_btn.grid(row = 0, column = 1)

    def add_cb_value(self):
        cty = str(self.newselection)
        stack.append(cty)



    def newselection(self, event):
        self.value_of_combo = self.box.get()
        return self.value_of_combo


    def merge_selected(self):
        pass



        cb_panel = Frame(self.parent)
        cb_panel.pack(side=TOP, fill=BOTH, expand=Y)

        cbp = ttk.Labelframe(cb_panel, text='Pre-defined List')
        cb = ttk.Combobox(self.parent, values=cb_list, state='readonly')
        cb.current(1)  # set selection
        cb.pack(pady=5, padx=10)

        # position and display
        cbp.pack(in_=cb_panel, side=TOP, pady=5, padx=10, fill = 'y')

        # set the selection event
        cb.bind("<<ComboboxSelected>>", self.newselection)


    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()


# Contain top level window usually called root
root = Tk()

# Create an instance of the class that defines the GUI and associate it with the top level window..
GUI(root)

# Keep listening for events until destroy event occurs.
root.mainloop()