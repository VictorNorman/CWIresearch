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
from tkinter.filedialog import askopenfilenames
from tkinter.filedialog import asksaveasfilename

class ReadnSort:
    def __init__(self, debug=False):

        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

        self.DEBUG = debug

        self.time=[]
        self.deltaTrig = 0.

        self.PCH0=[]
        self.PCH1=[]
        self.PCH2=[]
        self.PCH3=[]

        self.PCH1max=0.
        self.PCH1min=0.
        self.PCH2max=0.
        self.PCH2min=0.
        self.PCH3max=0.
        self.PCH3min=0.

        self.PCH1mult=1.
        self.PCH2mult=1.
        self.PCH3mult=1.

        self.PCH1Scaled=[]
        self.PCH2Scaled=[]
        self.PCH3Scaled=[]

        self.PCH0butter = []
        self.PCH1butter = []
        self.PCH2butter = []
        self.PCH3butter = []

        self.all1=[]
        self.all2=[]
        self.all3=[]

    def ReadFile(self):

        
    #    window=tk.Tk()

        seismicfilenames = askopenfilenames(filetypes=[("csv files", "*.csv;*.CSV")]) # show an "Open" dialog box and return the path to the selected file
    #    window.lift()
        for file in seismicfilenames:
            if self.DEBUG:
                print(file) 
                print("i am reading a file now")
            
            csvFile = open(file,"r") 
            if self.DEBUG:
                print(" i opened the file")
            
            locations=csvFile.readline()

            geophoneLocationsString=locations.split(',')
            self.sledge=float(geophoneLocationsString[0])
            self.geophone1Loc=float(geophoneLocationsString[1])
            self.geophone2Loc=float(geophoneLocationsString[2])
            self.geophone3Loc=float(geophoneLocationsString[3])
            if self.DEBUG:
                print(geophoneLocationsString[0])
                print(geophoneLocationsString)
                print(self.sledge, self.geophone1Loc,self.geophone2Loc,self.geophone3Loc)
            csvFile.seek(0)  # rewind file to the top again
            df=pd.read_csv(csvFile,header=1)

            self.time=df["aTime"].values
            self.PCH0butter=df["bTrigger"].values
            self.PCH1=df["cSmoothCH1"].values
            self.PCH2=df["dSmoothCH2"].values
            self.PCH3=df["eSmoothCH3"].values
            self.PCH1butter=df["iRawCH1"].values
            self.PCH2butter=df["jRawCH2"].values
            self.PCH3butter=df["kRawCH3"].values

            self.deltaTrig=(self.time[-1]-self.time[0])/len(self.PCH1)
            
            csvFile.close()
            if self.DEBUG:
                print("t=", self.time[0])
                print("I finished reading the file")

            # Maybe should put VVV into a seperate function to keep functions small

            distance1=self.geophone1Loc-self.sledge
            distance2=self.geophone2Loc-self.sledge
            distance3=self.geophone3Loc-self.sledge

            con1=np.concatenate((self.geophone1Loc,self.sledge,distance1,self.PCH1),axis=None)
            con2=np.concatenate((self.geophone2Loc,self.sledge,distance2,self.PCH2),axis=None)
            con3=np.concatenate((self.geophone3Loc,self.sledge,distance3,self.PCH3),axis=None)
            if(self.all1 == []):
                self.timeColumn=np.concatenate((0,0,0,self.time),axis=None)
                self.all1 = con1
                self.all2 = con2
                self.all3 = con3
            else:
                self.all1=np.c_[self.all1,con1]
                self.all2=np.c_[self.all2,con2]
                self.all3=np.c_[self.all3,con3]

        
    
    def WriteFile(self):
        seismicfilename = asksaveasfilename() # show an "Open" dialog box and return the path to the selected file
        if self.DEBUG:
            print(seismicfilename)          
            print("i am writing a file now")
        
        if seismicfilename[-4]=='.':
            seismicfilename=seismicfilename[:-4]
        
        if self.DEBUG:    
            print(seismicfilename) 
            print('out stuff', self.outputData1[0:5,:])
        
        csvFile = open(seismicfilename + '1.csv', "w") 
        df = pd.DataFrame(self.outputData1)
        df.to_csv(csvFile,index=False,header=False,line_terminator='\n')
        csvFile.close()
        
        csvFile = open(seismicfilename + '2.csv', "w") 
        df = pd.DataFrame(self.outputData2)
        df.to_csv(csvFile,index=False,header=False,line_terminator='\n')
        csvFile.close()
        
        csvFile = open(seismicfilename + '3.csv', "w") 
        df = pd.DataFrame(self.outputData3)
        df.to_csv(csvFile,index=False,header=False,line_terminator='\n')
        csvFile.close()

    def sort_data(self):
        all1Sorted = self.all1 [ :, self.all1[1].argsort()]
        all2Sorted = self.all2 [ :, self.all2[1].argsort()]
        all3Sorted = self.all3 [ :, self.all3[1].argsort()]
        self.outputData1=np.c_[self.timeColumn,all1Sorted]
        self.outputData2=np.c_[self.timeColumn,all2Sorted]
        self.outputData3=np.c_[self.timeColumn,all3Sorted]
        if self.DEBUG:
            print('now lets sort these files')
            print(self.outputData1[0:10,:])

    def run(self):
        self.ReadFile()
        self.sort_data()
        self.WriteFile()

if __name__=='__main__':
    rns = ReadnSort()
    rns.run()