from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw()

base_file = askopenfilename(filetypes=[("csv files", "*.csv;*.CSV")])
compare_file = askopenfilename(filetypes=[("csv files", "*.csv;*.CSV")])

csvFile = open(base_file,"r") 
csvFile2 = open(compare_file,"r")

data1 = csvFile.readlines()
data2 = csvFile2.readlines()

if len(data1) == len(data2):
    for i in range(len(data1)):
        if data1[i] != data2[i]:
            raise Exception("not equal")
else:
    raise Exception("different lengths")