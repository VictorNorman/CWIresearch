from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilenames

Tk().withdraw()

rf = askopenfilenames(filetypes=[("csv files", "*.csv;*.CSV")])
tf = askopenfilenames(filetypes=[("csv files", "*.csv;*.CSV")])
reference_file1 = open(rf[0],"r")
reference_file2 = open(rf[1],"r") 
reference_file3 = open(rf[2],"r") 
test_file1 = open(tf[0],"r")
test_file2 = open(tf[1],"r")
test_file3 = open(tf[2],"r")

reference_data1 = reference_file1.readlines()
reference_data2 = reference_file2.readlines()
reference_data3 = reference_file3.readlines()
test_data1 = test_file1.readlines()
test_data2 = test_file2.readlines()
test_data3 = test_file3.readlines()


if len(reference_data1) == len(test_data1):
    for i in range(len(reference_data1)):
        if reference_data1[i] != test_data1[i]:
            raise Exception("not equal")
else:
    raise Exception("different lengths")

if len(reference_data2) == len(test_data2):
    for i in range(len(reference_data2)):
        if reference_data2[i] != test_data2[i]:
            raise Exception("not equal")
else:
    raise Exception("different lengths")

if len(reference_data3) == len(test_data3):
    for i in range(len(reference_data3)):
        if reference_data3[i] != test_data3[i]:
            raise Exception("not equal")
else:
    raise Exception("different lengths")