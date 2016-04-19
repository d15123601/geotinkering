from tkinter import *
from tkinter import ttk


class myGUI:
    def __init__(self, parent):
        self.parent = parent


        self.cb_box = ttk.Labelframe(parent, text = 'Object Picker',
                                width = 250, height = 500, borderwidth = 5,
                                relief = 'sunken').grid(row = 1, column = 0)

        ttk.Label(self.cb_box, text = 'Please choose an item from the list:',
                             foreground = 'red', justify = 'left').grid(row = 1, column = 0,sticky = 'n')

        self.op_box = ttk.Labelframe(parent, text = 'Operations',
                                    height = 50,
                                    borderwidth = 5,
                                    relief = 'sunken').grid(row = 0, column = 0, columnspan = 3)

        self.btn_add = ttk.Button(self.op_box, width = 50, text = 'Add', command = self.choose_selected)
        self.btn_add.grid(row = 0, column = 1)

        self.display_box = ttk.Labelframe(parent, text = 'Object Display',
                                width = 500, height = 500, borderwidth = 5,
                                relief = 'sunken').grid(row = 1, column = 2)

    def choose_selected(self):
        pass

root = Tk()
myGUI(root)
root.mainloop()