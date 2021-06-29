from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw()

reference_file1 = open("Reference_data1.csv","r")
reference_file2 = open("Reference_data2.csv","r") 
reference_file3 = open("Reference_data3.csv","r") 
test_file1 = open("Test_data1.csv","r")
test_file2 = open("Test_data2.csv","r")
test_file3 = open("Test_data3.csv","r")

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