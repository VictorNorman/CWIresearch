# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 13:53:15 2019

@author: Jim Clark
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from numbers import Real
import csv

class read_sorted:
    '''
    Takes in a sorted csv file and outputs a matplot graph
    '''
    def __init__(self):
        # Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        #    window=tk.Tk()
        self.amplitude_multiplier=2.    #useful if first arrival is needed for refraction

        self.lowcut=0.1
        self.initial_lowcut=0.1
        self.initial_highcut=600

        self.click_data_list=[]
        self.output_bool = False

        time1stBreak=[]
        strikePlate=[]
        self.start_index=0
        self.set_plot()
        #print(t_original[0])

        #convert time to start at 0 for pretrig instead of -15 and change from ms to s
        #t=(t_original-t_original[0])/1000. 

        #fig, ax = plt.subplots()
        #plt.subplots_adjust(bottom=0.2)

    def set_plot(self):
        # Creates the background and axes of the graph
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
        # Opens up a dialog graph and lets the user select a file to read
        self.seismicfilename = askopenfilename(filetypes=[("csv files", "*.csv;*.CSV")]) # show an "Open" dialog box and return the path to the selected file
        self.geophoneLocations=[]
        csvFile = open(self.seismicfilename,"r") 
        locations=csvFile.readline()
        locations=csvFile.readline()
        self.geophoneLocationsString=locations.split(',')

        glength=len(self.geophoneLocationsString)
        for j in range(1,glength,1):
            print(glength,j,self.geophoneLocationsString[j])
            x=float(self.geophoneLocationsString[j])
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

    def output_file(self):
        # Opens a dialog for user to name an output file
        self.output_bool = True
        self.click_file_name = asksaveasfilename()
        self.click_file = open(self.click_file_name + '.csv', "w", newline='')

    def plotit(self, my_data,lowcut,highcut):
        
        # Plots data from file

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
        # When User clicks on graph the point data is stored in a list to possibly be stored in an ouptut file

        # print( 'button=%d, x=%d, y=%d, time=%f, ydata=%f' \
        #        %(event.button, event.x,\
        #          event.y, event.xdata, event.ydata))
        if isinstance(event.x,Real) and isinstance(event.y,Real) \
            and isinstance(event.xdata,Real) and isinstance(event.ydata,Real):
            # click_data = (int(np.rint(event.ydata)),event.xdata)
            click_data = (self.geophoneLocationsString[int(np.rint(event.ydata))], event.xdata)
            self.click_data_list.append(click_data)
            self.textvar.remove()  
            myTime='Time is %7.4f ms' %(event.xdata)
            self.textvar=plt.annotate(myTime, xy=(0.01, 0.95), \
                                    xycoords='axes fraction')
            plt.draw()
        # strikePlate=strikePlate.append(np.rint(event.ydata))
        # time1stBreak=time1stBreak.append(event.xdata)
    def submit(self, text):
        # Updates the graph from new Lowcut, Highcut, and amplitude
        txt=text.split(',')
        self.lowcut=float(txt[0])
        self.highcut=float(txt[1])
        self.amplitude_multiplier=float(txt[2])
        plt.clf()
        
        for index in range(0,self.cols-1,1):
            line_delete = ""
            # line = [line for line in self.ax1.lines if line.get_label()==str(index)][0]  # What is this?
            for line in self.ax1.lines:
                if line.get_label()==str(index):
                    line_delete = line
            if line_delete != "":
                self.ax1.lines.remove(line_delete)

        self.ax1.collections.clear()
        self.__init__()
        self.plotit(self.my_data,self.lowcut,self.highcut)
        self.input_str = str(self.lowcut)+', '+str(self.highcut)+', '+\
                        str(self.amplitude_multiplier)
        self.run()
        return

    def scale_filter(self, my_data, trace, lowcut, highcut):
        pbuttertrace=[]
        #print(trace)
        rmax=(my_data[:,trace].max())/self.amplitude_multiplier
        #print(rmax)
        p=my_data[:,trace]/rmax   
        pbuttertrace=self.butter_bandpass_filter(p, lowcut, highcut, self.fs, order=2)
        return pbuttertrace
    
    def initial_run(self):
        self.plotit(self.my_data,self.initial_lowcut,self.initial_highcut)
        self.input_str = str(self.initial_lowcut)+', '+str(self.initial_highcut)+', '+\
                        str(self.amplitude_multiplier)
        self.run()

    def run(self):
        axtextbox = plt.axes([0.35, 0.05, 0.35, 0.055])
        # text_box = TextBox(axtextbox, 'LowCut, HighCut, Amplitude', \
        #                 initial=str(self.initial_lowcut)+', '+str(self.initial_highcut)+', '+\
        #                 str(self.amplitude_multiplier))
        # text_box.on_submit(self.submit)
        plt.axes(self.ax1)
        self.cid=self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        
    def display(self):
        plt.show()
# --------------Getters and Setters------------
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
# ---------------------------------------------

    def close_file(self):
        # writes to and closes output
        print(self.click_data_list)
        filewriter = csv.writer(self.click_file, delimiter=' ')
        header = csv.writer(self.click_file)
        header.writerow([self.input_str])
        header.writerow([self.seismicfilename + '\n'])
        for clicks in self.click_data_list:
            filewriter.writerow(clicks)
        self.click_file.close()

if __name__ == "__main__":
    RS = read_sorted()
    RS.run()