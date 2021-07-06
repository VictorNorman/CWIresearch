import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from scipy.signal import freqz
import matplotlib as mpl
from matplotlib import rcParams
from shutil import copyfile
from matplotlib.widgets import TextBox
from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from numbers import Real
import ReadSorted

class read_sorted_gui:
    def __init__(self, window):
        self.window = window
        self.read_sorted = ReadSorted.read_sorted()
        self.read_sorted.open_file()
        self.read_sorted.run()


if __name__=="__main__":
    window = Tk()
    rsg = read_sorted_gui(window)

    window.mainloop()