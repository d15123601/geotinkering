from tkinter import *
from tkinter import ttk


class loadingGUI():
    def __init__(self, master):
        self.master = master
        self.master.title("Dataset selection")


        # Initialise variables here
        base_params = {'host': "mf2.dit.ie:8080",
                       'layer': "cso:ctygeom",
                       'srs_code': 29902,
                       'properties': "countyname",
                       'geom_field': "",
                       'filter_property': "",
                       'filter_values': ""}


        fetch_params = base_params
        self.param1 = StringVar()
        self.param2 = StringVar()
        self.param3 = StringVar()
        self.param4 = StringVar()
        self.param5 = StringVar()
        self.param6 = StringVar()
        self.param7 = StringVar()

        # Initialise the widgets
        self.mainframe = ttk.Frame(self.master)

        self.label1 = ttk.Label(self.mainframe,
                                text = "Please use buttons to select datasets or enter custom\n"
                                + "parameters in the boxes to the left",
                                foreground = 'blue',
                                relief = 'sunken')
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

        self.param1.set(base_params['host'])
        self.param2.set(base_params['layer'])
        self.param3.set(base_params['srs_code'])
        self.param4.set(base_params['properties'])
        self.param5.set(base_params['geom_field'])
        self.param6.set(base_params['filter_property'])
        self.param7.set(base_params['filter_values'])

        self.display1 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  text = self.param1.get(),
                                  anchor = 'center')
        self.display2 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  text = self.param2.get(),
                                  anchor = 'center')
        self.display3 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  text = self.param3.get(),
                                  anchor = 'center')
        self.display4 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  text = self.param4.get(),
                                  anchor = 'center')
        self.display5 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  text = self.param5.get(),
                                  anchor = 'center')
        self.display6 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  text = self.param6.get(),
                                  anchor = 'center')
        self.display7 = ttk.Label(self.display_frame,
                                  foreground = 'red',
                                  text = self.param7.get(),
                                  anchor = 'center')

        self.button_County = ttk.Button(self.button_frame,
                                    text = 'County Polygons')
        self.button_Towns =  ttk.Button(self.button_frame,
                                    text = 'Town Points')
        self.button_LargeTowns =  ttk.Button(self.button_frame,
                                    text = 'Large Town Points')
        self.button_EDs = ttk.Button(self.button_frame,
                                    text = 'ED Polygons')
        self.button_Provinces = ttk.Button(self.button_frame,
                                    text = 'Province Polygons')
        self.button_SAs = ttk.Button(self.button_frame,
                                    text = 'SA Polygons')

        self.param1.set(base_params['host'])
        self.param2.set(base_params['layer'])
        self.param3.set(base_params['srs_code'])
        self.param4.set(base_params['properties'])
        self.param5.set(base_params['geom_field'])
        self.param6.set(base_params['filter_property'])
        self.param7.set(base_params['filter_values'])


        self.mainframe.grid(row=0, column = 0)
        self.label1.grid(row = 0, column = 0, columnspan = 3)

        self.entry_frame.grid(row = 1, column = 0, sticky = 'ns')
        self.entry1.grid(row = 0, sticky = 'ew')
        self.entry2.grid(row = 1, sticky = 'ew')
        self.entry3.grid(row = 2, sticky = 'ew')
        self.entry4.grid(row = 3, sticky = 'ew')
        self.entry5.grid(row = 4, sticky = 'ew')
        self.entry6.grid(row = 5, sticky = 'ew')
        self.entry7.grid(row = 6, sticky = 'ew')

        self.display_frame.grid(row = 1, column = 1, sticky = 'ns')
        self.display1.grid(row = 0, sticky = 'ew')
        self.display2.grid(row = 1, sticky = 'ew')
        self.display3.grid(row = 2, sticky = 'ew')
        self.display4.grid(row = 3, sticky = 'ew')
        self.display5.grid(row = 4, sticky = 'ew')
        self.display6.grid(row = 5, sticky = 'ew')
        self.display7.grid(row = 6, sticky = 'ew')

        self.button_frame.grid(row = 1, column = 2, sticky = 'ns')
        self.button_LargeTowns.grid(row = 0, sticky = 'ew')
        self.button_County.grid(row = 1, sticky = 'ew')
        self.button_EDs.grid(row = 2, sticky = 'ew')
        self.button_Provinces.grid(row = 3, sticky = 'ew')
        self.button_SAs.grid(row = 4, sticky = 'ew')
        self.button_Towns.grid(row = 5, sticky = 'ew')

def main():
    root = Tk()
    loadingGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()