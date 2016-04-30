from tkinter import *
from tkinter import ttk


class loadingGUI():
    def __init__(self, master):
        self.master = master
        self.master.title(text = "Dataset selection")

        self.mainframe = ttk.Frame(self.master)


        self.label1 = ttk.Label(self.mainframe,
                                text = "Please use buttons to select datasets or enter custom\n"
                                + "parameters in the boxes to the right",
                                foreground = 'blue',
                                relief = 'sunken',)


        self.mainframe.grid(row=0, column = 0)
        self.label1.grid(row = 0, sticky = 'ew')


def main():
    root = Tk()
    loadingGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()