# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 22:32:40 2020

@author: Jim Clark
"""

#this code reads selected seismic files, sorts them by geophone location and 
#writes a file with them all assembled in increasing order

import numpy as np
import pandas as pd
from tkinter import Tk     # from tkinter import Tk for Python 3.x
global valuefloat

P=[]
PR=[]
PL=[]
t=[]
deltaTrig = 0.

PCH0=[]
PCH1=[]
PCH2=[]
PCH3=[]

PCH1max=0.
PCH1min=0.
PCH2max=0.
PCH2min=0.
PCH3max=0.
PCH3min=0.

PCH1mult=1.
PCH2mult=1.
PCH3mult=1.

PCH1Scaled=[]
PCH2Scaled=[]
PCH3Scaled=[]

Pstack0=[]
Pstack1=[]
Pstack2=[]
Pstack3=[]

PCH0butter = []
PCH1butter = []
PCH2butter = []
PCH3butter = []

all1=[]
all2=[]
all3=[]

isStackClicked=False
keepOldValue=0
numStack=0
textvar=0
textvar1=0
myXmax=150.
Ymax=0.0
Ymin=0.0

iterate=0
cid=0

iclicked=0
ilabel=0

def ReadFile():
    global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12,\
     P, PR, PL, PCH1, PCH2, PCH3, PCH4, PCH0butter, PCH1butter,\
     PCH2butter, PCH3butter, Pstack0, Pstack1, Pstack2, Pstack3,\
     PCH1Scaled, PCH2Scaled, PCH3Scaled, Ymax, Ymin, ax,deltaTrig
    global locations, sledge, geophone1Loc, geophone2Loc, geophone3Loc

    from tkinter.filedialog import askopenfilename

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
#    window=tk.Tk()

    seismicfilename = askopenfilename(filetypes=[("csv files", "*.csv;*.CSV")]) # show an "Open" dialog box and return the path to the selected file
#    window.lift()
    if seismicfilename=='': 
        print('this is the end')
        return 'stop'
    print(seismicfilename) 
    print("i am reading a file now")
    
    csvFile = open(seismicfilename,"r") 
    print(" i opened the file")
    
    locations=csvFile.readline()

    geophoneLocationsString=locations.split(',')
    print(geophoneLocationsString[0])
    sledge=float(geophoneLocationsString[0])
    geophone1Loc=float(geophoneLocationsString[1])
    geophone2Loc=float(geophoneLocationsString[2])
    geophone3Loc=float(geophoneLocationsString[3])
    print(geophoneLocationsString)
    print(sledge, geophone1Loc,geophone2Loc,geophone3Loc)
    csvFile.seek(0)  # rewind file to the top again
    df=pd.read_csv(csvFile,header=1)
    
    t=df["aTime"].values
    PCH0butter=df["bTrigger"].values
    PCH1=df["cSmoothCH1"].values
    PCH2=df["dSmoothCH2"].values
    PCH3=df["eSmoothCH3"].values
    Pstack1=df["fStackCH1"].values
    Pstack2=df["gStackCH2"].values
    Pstack3=df["hStackCH3"].values
    PCH1butter=df["iRawCH1"].values
    PCH2butter=df["jRawCH2"].values
    PCH3butter=df["kRawCH3"].values

    deltaTrig=(t[-1]-t[0])/len(PCH1)

    print("t=", t[0])
    csvFile.close()
    print("I finished reading the file")

    return 'keepgoing'
    
 
def WriteFile():
    global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12,\
     P, PR, PL, PCH1, PCH2, PCH3, PCH4, PCH0butter, PCH1butter,\
     PCH2butter, PCH3butter, Pstack0, Pstack1, Pstack2, Pstack3,\
     PCH1Scaled, PCH2Scaled, PCH3Scaled, Ymax, Ymin, ax,deltaTrig
    global valuefloat,formerValue, outputData1,outputData2,outputData3
    
    from tkinter.filedialog import asksaveasfilename

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    seismicfilename = asksaveasfilename() # show an "Open" dialog box and return the path to the selected file
    print(seismicfilename)          
    print("i am writing a file now")
    
    if seismicfilename[-4]=='.':
        seismicfilename=seismicfilename[:-4]
        
    print(seismicfilename) 

    print('out stuff', outputData1[0:5,:])
    csvFile = open(seismicfilename + '1.csv', "w") 
    df = pd.DataFrame(outputData1)
    df.to_csv(csvFile,index=False,header=False,line_terminator='\n')
    csvFile.close()
    
    csvFile = open(seismicfilename + '2.csv', "w") 
    df = pd.DataFrame(outputData2)
    df.to_csv(csvFile,index=False,header=False,line_terminator='\n')
    csvFile.close()
    
    csvFile = open(seismicfilename + '3.csv', "w") 
    df = pd.DataFrame(outputData3)
    df.to_csv(csvFile,index=False,header=False,line_terminator='\n')
    csvFile.close()

    
loop=ReadFile()
timeColumn=np.concatenate((0,0,0,t),axis=None)
distance1=geophone1Loc-sledge
distance2=geophone2Loc-sledge
distance3=geophone3Loc-sledge

all1=np.concatenate((geophone1Loc,sledge,distance1,PCH1),axis=None)
all2=np.concatenate((geophone2Loc,sledge,distance2,PCH2),axis=None)
all3=np.concatenate((geophone3Loc,sledge,distance3,PCH3),axis=None)
#print ('all1=   ',all1[0:5,:])

while loop=="keepgoing":
    loop=ReadFile()
    if loop=="keepgoing":
        distance1=geophone1Loc-sledge
        distance2=geophone2Loc-sledge
        distance3=geophone3Loc-sledge
        
        con1=np.concatenate((geophone1Loc,sledge,distance1,PCH1),axis=None)
        con2=np.concatenate((geophone2Loc,sledge,distance2,PCH2),axis=None)
        con3=np.concatenate((geophone3Loc,sledge,distance3,PCH3),axis=None)
        all1=np.c_[all1,con1]
        all2=np.c_[all2,con2]
        all3=np.c_[all3,con3]
        print ('all1=   ',all1[0:10,:])

print('now lets sort these files')

all1Sorted = all1 [ :, all1[1].argsort()]
all2Sorted = all2 [ :, all2[1].argsort()]
all3Sorted = all3 [ :, all3[1].argsort()]
outputData1=np.c_[timeColumn,all1Sorted]
outputData2=np.c_[timeColumn,all2Sorted]
outputData3=np.c_[timeColumn,all3Sorted]
print(outputData1[0:10,:])

WriteFile()
