from tkinter import *
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from ReadSorted import read_sorted
from tkinter import messagebox
from SortFiles import ReadnSort

class test_gui:
    def __init__(self, window):
        self.window = window
        self.RS = read_sorted()
        self.RnS = ReadnSort()
        self.buttonframe = Frame(self.window)
        self.graphframe = Frame(self.window)
        self.buttonframe.pack(side=TOP, anchor=NW)
        
        self.addButtons()
    
    def addButtons(self):
        file_button = Button(self.buttonframe, text="Pick Sorted", command=self.openFile)
        file_button.grid(row=1, column=1, rowspan=2)
        sort_button = Button(self.buttonframe, text="Sort Files", command=self.RnS.run)
        sort_button.grid(row=1, column=2, rowspan=2)

    def openFile(self):
        self.RS.open_file()
        self.RS.initial_run()
        self.text_box = StringVar(self.window, self.RS.get_input_str())
        self.show_graph()
    
    def show_graph(self):
        output_button = Button(self.buttonframe, text="Output Clicks", command=self.RS.output_file)
        output_button.grid(row=1, column=3, rowspan=2)
        self.graph = self.RS.get_graph()
        self.graphframe.pack(side=LEFT, anchor=W)
        self.canvas = FigureCanvasTkAgg(self.graph, master=self.graphframe)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=2, column=1)
        self.display()

    def display(self):
        description = Label(self.graphframe, text="LowCut, HighCut, Amplitude")
        self.perameters = Entry(self.graphframe, text=self.text_box, width=20)
        description.grid(row=3, column=1)
        self.perameters.grid(row=4, column=1)
        print(self.text_box.get())
        submit = Button(self.graphframe, text="submit", command=self.update)
        submit.grid(row=5, column=1)

    def update(self):
        self.graphframe.pack_forget()
        self.text_box = StringVar(self.graphframe, self.perameters.get())
        self.RS.submit(self.text_box.get())
        self.show_graph()
    
    def on_closing(self):
        if self.RS.output_bool == True:
            self.RS.close_file()
        exit(0)

if __name__=="__main__":
    root = Tk()
    gui = test_gui(root)
    
    root.protocol("WM_DELETE_WINDOW", gui.on_closing)
    root.mainloop()