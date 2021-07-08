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

class test_gui:
    def __init__(self, window):
        self.window = window
        self.RS = read_sorted()
        self.addButtons()
    
    def addButtons(self):
        file_button = Button(self.window, text="Pick File", command=self.openFile)
        file_button.grid(row=1, column=1, rowspan=2)
    def openFile(self):
        self.RS.open_file()
        self.RS.run()
        self.graph = self.RS.get_graph()

        canvas = FigureCanvasTkAgg(self.graph, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().grid(row=2, column=1)
        self.display()
    def display(self):
        description = Label(self.window, text="LowCut, HighCut, Amplitude")
        
        lowcut = self.RS.get_initial_lowcut()
        highcut = self.RS.get_initial_highcut()
        amplitude = self.RS.get_amplitude()
        text_box = StringVar(self.window, self.RS.get_input_str())
        perameters = Entry(self.window, text=text_box, width=20)
        description.grid(row=3, column=1)
        perameters.grid(row=3, column=2)
        print(text_box.get())
        submit = Button(self.window, text="submit", command=self.RS.submit(text_box.get()))
        submit.grid(row=4, column=2)



if __name__=="__main__":
    root = Tk()
    gui = test_gui(root)
    def on_closing():
        exit(0)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()