# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 13:53:15 2019

@author: Jim Clark
"""

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

class read_sorted:
    def __init__(self):
        # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        #    window=tk.Tk()
        self.amplitude_multiplier=2.    #useful if first arrival is needed for refraction

        self.lowcut=0.1
        self.initial_lowcut=0.1
        self.initial_highcut=600

        time1stBreak=[]
        strikePlate=[]
        self.start_index=0
        #print(t_original[0])

        #convert time to start at 0 for pretrig instead of -15 and change from ms to s
        #t=(t_original-t_original[0])/1000. 

        #fig, ax = plt.subplots()
        #plt.subplots_adjust(bottom=0.2)

        self.fig=plt.figure(figsize=(9,7))
        plt.subplot(111)
        plt.gcf().tight_layout()
        plt.subplots_adjust(bottom=0.2)
        self.ax1=self.fig.axes[0]
        print(self.fig.axes[0])
        plt.ylabel('Strike Plate Number')
        plt.xlabel('time (ms)')
        #plt.title('Filtered Data - lowcut= '+str(lowcut)+ \
        #          '  highcut=  '+str(highcut)+'  amplification=  '+ \
        #          str(amplitude_multiplier))
        plt.grid()
        self.textvar=plt.annotate(" ", xy=(0.01, 0.95), \
                                xycoords='axes fraction')
        my_data_scaled=[]
        shift=0.
        pbutter=[]

    def open_file(self):
        seismicfilename = askopenfilename(filetypes=[("csv files", "*.csv;*.CSV")]) # show an "Open" dialog box and return the path to the selected file
        self.geophoneLocations=[]
        csvFile = open(seismicfilename,"r") 
        locations=csvFile.readline()
        locations=csvFile.readline()
        geophoneLocationsString=locations.split(',')

        glength=len(geophoneLocationsString)
        for j in range(1,glength,1):
            print(glength,j,geophoneLocationsString[j])
            x=float(geophoneLocationsString[j])
            self.geophoneLocations.append(x)

        csvFile.seek(0)
        self.my_data = np.loadtxt(csvFile, delimiter=',',skiprows=3)

        rows,self.cols=self.my_data.shape
        print(rows,self.cols)
        t_original=self.my_data[self.start_index:,0]
        t_length=len(t_original)

        self.t=t_original/1000
        time_total=self.t[t_length-1] - self.t[0]

        k=np.arange(t_length)
        sample_rate=96000
        dt=time_total/t_length
        self.fs=1./dt

        print(dt,t_length,time_total,self.fs)

    def plotit(self, my_data,lowcut,highcut):
        #global lines1, fill1
        shift=1
    #    plt.subplot(111)
    #    plt.gcf().tight_layout()
        #cid1
        #i=self.scale_filter(my_data_scaled,lowcut,highcut)
        plt.axes(self.ax1)
        plt.title('Filtered Data - lowcut= '+str(lowcut)+ \
            '  highcut=  '+str(highcut)+'  amplification=  '+ \
            str(self.amplitude_multiplier))
        for trace in range(1,self.cols,1):
    #        rmax=(my_data[:,trace].max())/amplitude_multiplier
    #        my_data_scaled=my_data[:,trace]/rmax                 
            i=self.scale_filter(my_data,trace,lowcut,highcut) 
            plt.plot(self.t*1000,i+shift, lw=0.6, color='black', label=str(shift)) 
            plt.annotate(self.geophoneLocations[shift-1],xy=(self.t[0]*1000,shift),ha="right")
            plt.fill_between(self.t*1000,i+shift,shift,where=i>0.0,facecolor=str(0.9),interpolate=True)   
            shift=shift+1
        
    def butter_bandpass(self, lowcut, highcut, fs, order=5):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        if high >= 1:
            highcut=0.95*nyq
            high=highcut/nyq
            self.initial_highcut=highcut
            print('Highcut reduced because of nyquist  ', highcut)
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order=5):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        y = lfilter(b, a, data)
        return y

    def onclick(self, event):

        # print( 'button=%d, x=%d, y=%d, time=%f, ydata=%f' \
        #        %(event.button, event.x,\
        #          event.y, event.xdata, event.ydata))
        if isinstance(event.x,Real) and isinstance(event.y,Real) \
            and isinstance(event.xdata,Real) and isinstance(event.ydata,Real):
            print(int(np.rint(event.ydata)),event.xdata)
            self.textvar.remove()  
            myTime='Time is %7.4f ms' %(event.xdata)
            self.textvar=plt.annotate(myTime, xy=(0.01, 0.95), \
                                    xycoords='axes fraction')
            plt.draw()
        # strikePlate=strikePlate.append(np.rint(event.ydata))
        # time1stBreak=time1stBreak.append(event.xdata)
    def submit(self, text):
        txt=text.split(',')
        #print('new text is  ', text)
        self.lowcut=float(txt[0])
        self.highcut=float(txt[1])
        self.amplitude_multiplier=float(txt[2])
        print(txt)
        plt.clf()
        
        # for index in range(0,self.cols-1,1):
        #     line_delete = ""
        #     print(self.ax1.lines)
        #     # line = [line for line in self.ax1.lines if line.get_label()==str(index)][0]  # What is this?
        #     for line in self.ax1.lines:
        #         if line.get_label()==str(index):
        #             line_delete = line
        #     print(line_delete)
        #     if line_delete != "":
        #         self.ax1.lines.remove(line_delete)
        #     print('index',index)

        self.ax1.collections.clear()
        self.plotit(self.my_data,self.lowcut,self.highcut)
        return

    def scale_filter(self, my_data, trace, lowcut, highcut):
        pbuttertrace=[]
        #print(trace)
        rmax=(my_data[:,trace].max())/self.amplitude_multiplier
        #print(rmax)
        p=my_data[:,trace]/rmax   
        pbuttertrace=self.butter_bandpass_filter(p, lowcut, highcut, self.fs, order=2)
        return pbuttertrace
    
    def run(self):
        self.plotit(self.my_data,self.initial_lowcut,self.initial_highcut)
        
        axtextbox = plt.axes([0.35, 0.05, 0.35, 0.055])
        # text_box = TextBox(axtextbox, 'LowCut, HighCut, Amplitude', \
        #                 initial=str(self.initial_lowcut)+', '+str(self.initial_highcut)+', '+\
        #                 str(self.amplitude_multiplier))
        # text_box.on_submit(self.submit)
        self.input_str = str(self.initial_lowcut)+', '+str(self.initial_highcut)+', '+\
                        str(self.amplitude_multiplier)
        plt.axes(self.ax1)
        self.cid=self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        
    def display(self):
        plt.show()
    
    def get_initial_lowcut(self):
        return self.initial_lowcut
    def get_initial_highcut(self):
        return self.initial_highcut
    def get_amplitude(self):
        return self.amplitude_multiplier
    def get_graph(self):
        return self.fig
    def get_input_str(self):
        return self.input_str

if __name__ == "__main__":
    RS = read_sorted()
    RS.run()