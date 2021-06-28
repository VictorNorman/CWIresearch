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

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
#    window=tk.Tk()

seismicfilename = askopenfilename(filetypes=[("csv files", "*.csv;*.CSV")]) # show an "Open" dialog box and return the path to the selected file
geophoneLocations=[]
csvFile = open(seismicfilename,"r") 
locations=csvFile.readline()
locations=csvFile.readline()
geophoneLocationsString=locations.split(',')

glength=len(geophoneLocationsString)
for j in range(1,glength,1):
    print(glength,j,geophoneLocationsString[j])
    x=float(geophoneLocationsString[j])
    geophoneLocations.append(x)

csvFile.seek(0)
start_index=0
my_data = np.loadtxt(csvFile, delimiter=',',skiprows=3)
amplitude_multiplier=2.    #useful if first arrival is needed for refraction

lowcut=0.1
initial_lowcut=0.1
initial_highcut=600

time1stBreak=[]
strikePlate=[]

rows,cols=my_data.shape
print(rows,cols)
t_original=my_data[start_index:,0]
t_length=len(t_original)
#print(t_original[0])

#convert time to start at 0 for pretrig instead of -15 and change from ms to s
#t=(t_original-t_original[0])/1000. 
t=t_original/1000
time_total=t[t_length-1] - t[0]

k=np.arange(t_length)
sample_rate=96000
dt=time_total/t_length
fs=1./dt

print(dt,t_length,time_total,fs)

#fig, ax = plt.subplots()
#plt.subplots_adjust(bottom=0.2)

fig=plt.figure(figsize=(9,7))
plt.subplot(111)
plt.gcf().tight_layout()
plt.subplots_adjust(bottom=0.2)
ax1=fig.axes[0]
print(fig.axes[0])
plt.ylabel('Strike Plate Number')
plt.xlabel('time (ms)')
#plt.title('Filtered Data - lowcut= '+str(lowcut)+ \
#          '  highcut=  '+str(highcut)+'  amplification=  '+ \
#          str(amplitude_multiplier))
plt.grid()
textvar=plt.annotate(" ", xy=(0.01, 0.95), \
                        xycoords='axes fraction')
my_data_scaled=[]
shift=0.
pbutter=[]

def plotit(my_data,lowcut,highcut):
    #global lines1, fill1
    global line
    shift=1
#    plt.subplot(111)
#    plt.gcf().tight_layout()
    #cid1
    #i=scale_filter(my_data_scaled,lowcut,highcut)
    plt.axes(ax1)
    plt.title('Filtered Data - lowcut= '+str(lowcut)+ \
          '  highcut=  '+str(highcut)+'  amplification=  '+ \
          str(amplitude_multiplier))
    for trace in range(1,cols,1):
#        rmax=(my_data[:,trace].max())/amplitude_multiplier
#        print(rmax)
#        my_data_scaled=my_data[:,trace]/rmax                 
        i=scale_filter(my_data,trace,lowcut,highcut) 
        plt.plot(t*1000,i+shift, 'r', lw=0.6, color='black', label=str(shift)) 
        plt.annotate(geophoneLocations[shift-1],xy=(t[0]*1000,shift),ha="right")
        plt.fill_between(t*1000,i+shift,shift,where=i>0.0,facecolor=str(0.9),interpolate=True)   
        shift=shift+1
    
def butter_bandpass(lowcut, highcut, fs, order=5):
    global initial_highcut
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    if high >= 1:
        highcut=0.95*nyq
        high=highcut/nyq
        initial_highcut=highcut
        print('Highcut reduced because of nyquist  ', highcut)
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def onclick(event):
   global textvar

   # print( 'button=%d, x=%d, y=%d, time=%f, ydata=%f' \
   #        %(event.button, event.x,\
   #          event.y, event.xdata, event.ydata))
   if isinstance(event.x,Real) and isinstance(event.y,Real) \
     and isinstance(event.xdata,Real) and isinstance(event.ydata,Real):
       print(int(np.rint(event.ydata)),event.xdata)
       textvar.remove()  
       myTime='Time is %7.4f ms' %(event.xdata)
       textvar=plt.annotate(myTime, xy=(0.01, 0.95), \
                            xycoords='axes fraction')
       plt.draw()
   # strikePlate=strikePlate.append(np.rint(event.ydata))
   # time1stBreak=time1stBreak.append(event.xdata)
def submit(text):
    global lowcut,highcut,lines1,fill1, amplitude_multiplier
    txt=text.split(',')
    #print('new text is  ', text)
    lowcut=float(txt[0])
    highcut=float(txt[1])
    amplitude_multiplier=float(txt[2])

    for index in range(0,cols-1,1):
        line = [line for line in ax1.lines if line.get_label()==str(index)][0]
        ax1.lines.remove(line)
        #print('index',index)

    ax1.collections.clear()
    plotit(my_data,lowcut,highcut)
    return

def scale_filter(my_data,trace, lowcut, highcut):
    pbuttertrace=[]
    #print(trace)
    rmax=(my_data[:,trace].max())/amplitude_multiplier
    #print(rmax)
    p=my_data[:,trace]/rmax   
    pbuttertrace=butter_bandpass_filter(p, lowcut, highcut, fs, order=2)
    return pbuttertrace
 
plotit(my_data,initial_lowcut,initial_highcut)
   
axtextbox = plt.axes([0.35, 0.05, 0.35, 0.055])
text_box = TextBox(axtextbox, 'LowCut, HighCut, Amplitude', \
                   initial=str(initial_lowcut)+', '+str(initial_highcut)+', '+\
                   str(amplitude_multiplier))
text_box.on_submit(submit)
plt.axes(ax1)
cid=fig.canvas.mpl_connect('button_press_event', onclick)
