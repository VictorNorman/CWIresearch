# this code records seismic data, writes the files, and reads the files
#for later interpretation.

from matplotlib.widgets import Cursor, Button, Slider, CheckButtons,TextBox
import matplotlib.pyplot as plt

import pyaudio
# NOTE must use special pyaudio download from compiled sources
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
import sys
import scipy.signal as signal
from numpy import *
import pandas as pd
import tkinter as tk
import csv
#import time
global valuefloat
plt.style.use('classic')

plt.rcParams['agg.path.chunksize'] = 10000  # this allows plotting of large data sets

#chunk=1024
#chunk = 1
chunk=16
#chunk = 2
#BIGchunk=1024
FORMAT = pyaudio.paInt32
CHANNELS = 4
RATE = 96000
#RATE=48000
RECORD_SECONDS = 0.5
PRETRIG_SECONDS = 0.015

##delta=2.*1000.*(RECORD_SECONDS+PRETRIG_SECONDS)/RATE
##t=arange(0.,1000.*(RECORD_SECONDS+PRETRIG_SECONDS),delta)

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
fig = plt.figure(figsize=(14, 8))
#ax = fig.add_subplot(111, axisbg='#FFFFCC')
ax = fig.add_subplot(111, facecolor='#FFFFCC')

plt.subplots_adjust(bottom=0.2, left=0.05, right=.75, top=0.92)
#fig.suptitle('      Seismic Refraction')
plt.xlabel('      TIME in milliseconds')
plt.ylabel('Signal Amplitude')

location=''
textvariable=plt.annotate(location, xy=(0.5, 0.9), \
                        xycoords='axes fraction')

l0, = plt.plot(0,0)     # Trigger
l1, = plt.plot(0,0)     # Smooth 1
l2, = plt.plot(0,0)     # Smooth 2
l3, = plt.plot(0,0)     # Smooth 3
l4, = plt.plot(0,0)     # Stacked 1
l5, = plt.plot(0,0)     # Stacked 2
l6, = plt.plot(0,0)     # Stacked 3
l7, = plt.plot(0,0)     # Origianl 1
l8, = plt.plot(0,0)     # Original 2
l9, = plt.plot(0,0)     # Original 3
l10, = plt.plot(0,0)    # Scaled 1
l11, = plt.plot(0,0)    # Scaled 2
l12, = plt.plot(0,0)    # Scaled 3

rax = plt.axes([0.80, 0.2, 0.17, 0.75])
check = (CheckButtons(rax,('Trigger', 'Scaled 1', 'Scaled 2', 'Scaled 3',
            'Smoothed 1', 'Smoothed 2', 'Smoothed 3',
            'Stacked 1', 'Stacked 2', 'Stacked 3', 'Geophone 1', 'Geophone 2', 
            'Geophone 3',), (False, True, True, True, False, False, False, False,
             False, False, False, False, False)))

#Define colours for rectangles and set them
c = ['k','g', 'b', 'r','g', 'b', 'r','g', 'b', 'r', 'g', 'b', 'r']    
[rec.set_edgecolor(c[i]) for i, rec in enumerate(check.rectangles)]
[rec.set_linewidth(3.) for i, rec in enumerate(check.rectangles)]

iclicked=0
ilabel=0

def readAudio():
    # read a sound card input and write voltage to a file
    global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9,\
         l10, l11, l12, P, PR, PL, PCH1, PCH2, PCH3, PCH4,\
         PCH0butter, PCH1butter, PCH2butter, PCH3butter,\
         Pstack0, Pstack1, Pstack2, Pstack3, ax,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, deltaTrig

    p = pyaudio.PyAudio()

    print(p.get_default_input_device_info())
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)

    timelist=range(0, int(math.ceil((RATE / chunk) * RECORD_SECONDS)))
    pretriglist=range(0, int(math.ceil((RATE / chunk) * PRETRIG_SECONDS)))

    alldata = []
    pretrig = []
    counter=0
    TRIGGER=0
    #time.sleep(1)
    print("  Whack It!****************************************************  ")

# (put this after the print statement)
    textvar=plt.figtext(0.3,0.6,'WHACK IT!', size=50)
    textvar.set_visible(True)
    #plt.pause(1)

    
    for i in pretriglist:
        data = stream.read(chunk)
        pretrig.append(data)

    while 1:
        d = stream.read(chunk)
        pretrig.append(d)
        pretrig.pop(0)
        #Y = fromstring(d,dtype='int32')
        Y=frombuffer(d,dtype='int32')
        #Y=fromstring(d,dtype='h')
        #TRIGGER=array(Y,dtype='d')/32768.0  #for 16 bit input
        TRIGGER = array(Y, dtype='int32')/8388608.0
        counter = counter + 1

        if (absolute(TRIGGER[0]) > 0.5) or (counter > 44000): break
    #axArmButton.text(-0.2, 1.0, r' ', fontsize=14)
    del axArmButton.texts[1]
    #plt.draw()
    print("Y values", Y, TRIGGER, TRIGGER[0], TRIGGER[1], TRIGGER[2],
          TRIGGER[3])
    for i in timelist:
        data = stream.read(chunk)
        alldata.append(data)

    print(" finished recording")

    stream.close()
    p.terminate()
    everything = pretrig + alldata

    #print(everything[0:10])

    # write data to file
    datastring = b''.join((everything))

    X = frombuffer(datastring, dtype='int32')

    CH0 = X[0::4]
    CH1 = X[1::4]
    CH2 = X[2::4]
    CH3 = X[3::4]
#    P=array(X,dtype='d')/32768.0
#    P=array(X,dtype='int32')/8388608.0
#    savetxt(OUTPUT_FILENAME,P,fmt='%12.6G')
#    PR=array(R,dtype='d')/32768.0
#    PR=array(R,dtype='int32')/8388608.0
#    savetxt(OUTPUT_FILENAME_RIGHT,PR,fmt='%12.6G')
#    PL=array(L,dtype='d')/32768.0
#    PL=array(L,dtype='int32')/8388608.0

    #All 4 channels
    PCH0 = array(CH0, dtype='int32')/8388608.0
    PCH1 = array(CH1, dtype='int32')/8388608.0
    PCH2 = array(CH2, dtype='int32')/8388608.0
    PCH3 = array(CH3, dtype='int32')/8388608.0

    PCH1butter = PCH1     #PCH1butter is original signal
    PCH2butter = PCH2
    PCH3butter = PCH3
    PCH0butter = PCH0

    low = -1000.*PRETRIG_SECONDS
    high = 1000.*RECORD_SECONDS
    length = high-low
    length_sec = length/1000.
    deltaTrig = length/len(PCH1)
    t = arange(low,high,deltaTrig)

    #do the butterworth filter
    Nyq = 0.5/(length_sec/(len(PCH1)))
    print("Nyquist=   ", Nyq)
    cornerfreq = 200.     # max unattenuated frequency
    stopfreq = 500.      # minimum highly attenuated frequency
    ws = cornerfreq/Nyq
    wp = stopfreq/Nyq
    #16 is min dB attenuation in the stopband
    #3 is max dB loss in passband (1/2 amplitude
    N, wn = signal.buttord(wp, ws, 3, 16)
    b, a = signal.butter(N, wn)
    PCH1 = signal.lfilter(b, a, PCH1butter)  #PCH1 is now the filtered signal
    PCH2 = signal.lfilter(b, a, PCH2butter)  #PCH2 is now the filtered signal
    PCH3 = signal.lfilter(b, a, PCH3butter)  #PCH3 is now the filtered signal
   # del axArmButton.texts[-1]
    #savetxt(OUTPUT_FILENAME_LEFT,PL,fmt='%12.6G')
        
    if numStack == 0:
       Pstack1 = 0.0*PCH1
       Pstack2 = 0.0*PCH2
       Pstack3 = 0.0*PCH3
    textvar.set_visible(False)
    sys.stdout.flush()

    return

def onclick(event):
   global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9,\
         l10, l11, l12, P, PR, PL, PCH1, PCH2, PCH3, PCH4,\
         PCH0butter, PCH1butter, PCH2butter, PCH3butter,\
         Pstack0, Pstack1, Pstack2, Pstack3, ax,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, numStack, deltaTrig
   #print( 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %(event.button, event.x,
   #        event.y, event.xdata, event.ydata))
   global location
   plt.axes(ax)
   #myTitle='Time is %5.2f ms  Stack Number is %i' %(event.xdata,numStack)
   myTitle='Time is %5.2f ms' %(event.xdata)
   plt.title(myTitle)
   plt.draw()
   #plt.pause(0.01)

axArmButton = plt.axes([0.4, 0.05, 0.1, 0.075])
bArm=Button(axArmButton,label='ARM')
plt.title(' ')

axPlotButton = plt.axes([0.25, 0.05, 0.1, 0.075])
bPlot=Button(axPlotButton,label='PLOT CURVES')
plt.title(' ')

axWriteFileButton=plt.axes([0.15,0.05,0.1,0.075])
bWriteFile=Button(axWriteFileButton,label='Write File?')

axReadFileButton=plt.axes([0.05,0.05,0.1,0.075])
bReadFile=Button(axReadFileButton,label='Read File?')

plt.figtext(.58,.12,'STACK?')
axYesStackButton = plt.axes([0.55, 0.05, 0.05, 0.05])
bYesStack=Button(axYesStackButton,label='YES')

axNoStackButton = plt.axes([0.62, 0.05, 0.05, 0.05])
bNoStack=Button(axNoStackButton,label='NO')

axClearStackButton = plt.axes([0.72, 0.05, 0.1, 0.075])
bClearStack=Button(axClearStackButton,label='CLEAR STACK')

axResetButton=plt.axes([0.85, 0.05, 0.1, 0.075])
bResetButton=Button(axResetButton,label='AUTOSCALE')

cid=fig.canvas.mpl_connect('button_press_event', onclick)

# set useblit = True on gtkagg for enhanced performance
cursor = Cursor(ax, useblit=True,color='blue', linewidth=1 )

class ButtonClass:
   def Arm(self, event):
     global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9,\
         l10, l11, l12, P, PR, PL, PCH1, PCH2, PCH3, PCH4,\
         PCH0butter, PCH1butter, PCH2butter, PCH3butter,\
         Pstack0, Pstack1, Pstack2, Pstack3, ax,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, isStackClicked, Ymin, Ymax, deltaTrig
     global location
     location=''
     plt.axes(ax)

     axArmButton.text(-0.1, 1.0, r'', fontsize=14)

     isStackClicked=False

     l0.set_visible(False)      # Trigger
     l1.set_visible(False)      # Smooth 1
     l2.set_visible(False)      # Smooth 2
     l3.set_visible(False)      # Smooth 3
     l4.set_visible(False)      # Stacked 1
     l5.set_visible(False)      # Stacked 2
     l6.set_visible(False)      # Stacked 3
     l7.set_visible(False)      # Original 1
     l8.set_visible(False)      # Original 2
     l9.set_visible(False)      # Original 3
     l10.set_visible(False)     # Scaled 1
     l11.set_visible(False)     # Scaled 2
     l12.set_visible(False)     # Sacled 3

     for iloop in range(0,13):
         check.lines[iloop][0].set_visible(False)
         check.lines[iloop][1].set_visible(False)

     plt.draw()
     plt.pause(1.)

     readAudio()

     #Get min and max
     PCH1max=amax(PCH1)
     PCH1min=amin(PCH1)
     PCH2max=amax(PCH2)
     PCH2min=amin(PCH2)
     PCH3max=amax(PCH3)
     PCH3min=amin(PCH3)
     
     superMax = max([PCH1max,PCH2max,PCH3max])
     PCH1mult = superMax/PCH1max
     PCH2mult = superMax/PCH2max
     PCH3mult = superMax/PCH3max

     #my_new_list = [i * 5 for i in my_list]
     PCH1Scaled = [i * PCH1mult for i in PCH1]
     PCH2Scaled = [i * PCH2mult for i in PCH2]
     PCH3Scaled = [i * PCH3mult for i in PCH3]

     l1, = ax.plot(t,PCH1, visible=False, color = 'green')
     l2, = ax.plot(t,PCH2, visible=False, color = 'blue')
     l3, = ax.plot(t,PCH3, visible=False, color = 'red')
     l4, = ax.plot(t,Pstack1, visible=False, color = 'green', linestyle='--')
     l5, = ax.plot(t,Pstack2, visible=False, color = 'blue',linestyle='--')
     l6, = ax.plot(t,Pstack3, visible=False, color = 'red', linestyle = '--')

     l7, = ax.plot(t,PCH1butter, visible=False, color = 'green')
     l8, = ax.plot(t,PCH2butter, visible=False, color = 'blue')
     l9, = ax.plot(t,PCH3butter, visible=False, color = 'red')
     l10, = ax.plot(t,PCH1Scaled, visible=True, color = 'green')
     l11, = ax.plot(t,PCH2Scaled, visible=True, color = 'blue')
     l12, = ax.plot(t,PCH3Scaled, visible=True, color = 'red')

     #ax.autoscale(None)
     l0, = ax.plot(t,PCH0butter,visible=False, color = 'black')

     for iloop in range(1,4):
         check.lines[iloop][0].set_visible(True)
         check.lines[iloop][1].set_visible(True)
     #l7, = ax.plot(t,Pstack1, visible=False, color = 'green', linestyle='--')
     #l8, = ax.plot(t,Pstack2, visible=False, color = 'blue',linestyle='--')
     #l9, = ax.plot(t,Pstack3, visible=False, color = 'red', linestyle = '--')

    
     tempMax=0
     tempMin=0
     y=0

     for x in [PCH0butter, PCH1Scaled, PCH2Scaled, PCH3Scaled, PCH1butter, \
                   PCH2butter, PCH3butter, Pstack1, Pstack2, Pstack3]:
        if check.lines[y][0].get_visible():
            tempMax = max(x)
            tempMin = min(x)
            if tempMax > Ymax:
                Ymax = tempMax
            if tempMin < Ymin:
                Ymin = tempMin
        y = y + 1

     plt.ylim(Ymin, Ymax)


     plt.xlim(xmax=myXmax)
     plt.xlim(xmin=t[0])
     plt.xlabel('      TIME in milliseconds')
     plt.ylabel('Signal Amplitude')
     plt.draw()
     #plt.pause(0.01)
    # plt.axes(axArmButton)
    # plt.draw()
     return

   def PlotCurves(self, event):
     global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9,\
         l10, l11, l12, P, PR, PL, PCH1, PCH2, PCH3, PCH4,\
         PCH0butter, PCH1butter, PCH2butter, PCH3butter,\
         Pstack0, Pstack1, Pstack2, Pstack3, ax,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, isStackClicked, Ymin, Ymax, deltaTrig
     global location,locations,textvariable

     plt.axes(ax)

     lc=locations.split(',')
     location='Sledge ' + lc[0] +  \
         '  Geophones:  ' + lc[1] + ', ' +lc[2] +',  '+ lc[3]

     textvariable.remove()  
     textvariable=plt.annotate(location, xy=(0.5, 0.9), \
                        xycoords='axes fraction')
     
     axArmButton.text(-0.1, 1.0, r'', fontsize=14)

     isStackClicked=False

     l0.set_visible(False)      # Trigger
     l1.set_visible(False)      # Smooth 1
     l2.set_visible(False)      # Smooth 2
     l3.set_visible(False)      # Smooth 3
     l4.set_visible(False)      # Stacked 1
     l5.set_visible(False)      # Stacked 2
     l6.set_visible(False)      # Stacked 3
     l7.set_visible(False)      # Original 1
     l8.set_visible(False)      # Original 2
     l9.set_visible(False)      # Original 3
     l10.set_visible(False)     # Scaled 1
     l11.set_visible(False)     # Scaled 2
     l12.set_visible(False)     # Sacled 3

     for iloop in range(0,13):
         check.lines[iloop][0].set_visible(False)
         check.lines[iloop][1].set_visible(False)

     plt.draw()
     plt.pause(1.)

     #Get min and max
     PCH1max=amax(PCH1)
     PCH1min=amin(PCH1)
     PCH2max=amax(PCH2)
     PCH2min=amin(PCH2)
     PCH3max=amax(PCH3)
     PCH3min=amin(PCH3)
     
     superMax = max([PCH1max,PCH2max,PCH3max])
     PCH1mult = superMax/PCH1max
     PCH2mult = superMax/PCH2max
     PCH3mult = superMax/PCH3max

     PCH1Scaled = [i * PCH1mult for i in PCH1]
     PCH2Scaled = [i * PCH2mult for i in PCH2]
     PCH3Scaled = [i * PCH3mult for i in PCH3]

     l1, = ax.plot(t,PCH1, visible=False, color = 'green')
     l2, = ax.plot(t,PCH2, visible=False, color = 'blue')
     l3, = ax.plot(t,PCH3, visible=False, color = 'red')
     l4, = ax.plot(t,Pstack1, visible=False, color = 'green', linestyle='--')
     l5, = ax.plot(t,Pstack2, visible=False, color = 'blue',linestyle='--')
     l6, = ax.plot(t,Pstack3, visible=False, color = 'red', linestyle = '--')

     l7, = ax.plot(t,PCH1butter, visible=False, color = 'green')
     l8, = ax.plot(t,PCH2butter, visible=False, color = 'blue')
     l9, = ax.plot(t,PCH3butter, visible=False, color = 'red')
     l10, = ax.plot(t,PCH1Scaled, visible=True, color = 'green')
     l11, = ax.plot(t,PCH2Scaled, visible=True, color = 'blue')
     l12, = ax.plot(t,PCH3Scaled, visible=True, color = 'red')

     #ax.autoscale(None)
     l0, = ax.plot(t,PCH0butter,visible=False, color = 'black')

     for iloop in range(1,4):
         check.lines[iloop][0].set_visible(True)
         check.lines[iloop][1].set_visible(True)
   
     tempMax=0
     tempMin=0
     y=0
     for x in [PCH0butter, PCH1Scaled, PCH2Scaled, PCH3Scaled, PCH1butter,\
                 PCH2butter, PCH3butter, Pstack1, Pstack2, Pstack3]:
        if check.lines[y][0].get_visible():
            tempMax = max(x)
            tempMin = min(x)
            if tempMax > Ymax:
                Ymax = tempMax
            if tempMin < Ymin:
                Ymin = tempMin
        y = y + 1

     plt.ylim(Ymin, Ymax)

     plt.xlim(xmax=myXmax)
     plt.xlim(xmin=t[0])
     plt.xlabel('      TIME in milliseconds')
     plt.ylabel('Signal Amplitude')
     plt.draw()

     return

   def YesStack(self,event):
     global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9,\
         l10, l11, l12, P, PR, PL, PCH1, PCH2, PCH3, PCH4,\
         PCH0butter, PCH1butter,PCH2butter, PCH3butter,\
         Pstack0, Pstack1, Pstack2, Pstack3, ax,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, isStackClicked,\
         numStack, textvar, textvar1, deltaTrig
     if isStackClicked:
         return
     
     textvar=plt.figtext(0.55,0.10,'Stacked')
     textvar.set_visible(True)
     plt.pause(1)
     textvar.set_visible(False)
     
     isStackClicked=True

     if numStack==0:
        Pstack1=0.0*PCH1
        Pstack2=0.0*PCH2
        Pstack3=0.0*PCH3

     numStack=numStack+1
     Pstack1=((numStack-1)*Pstack1 + PCH1)/numStack
     Pstack2=((numStack-1)*Pstack2 + PCH2)/numStack
     Pstack3=((numStack-1)*Pstack3 + PCH3)/numStack
     plt.axes(ax)

     l4.set_visible(False)
     l5.set_visible(False)
     l6.set_visible(False)

     l4, = ax.plot(t,Pstack1, visible=True, color = 'green', linestyle = '--')
     l5, = ax.plot(t,Pstack2, visible=True, color = 'blue', linestyle = '--')
     l6, = ax.plot(t,Pstack3, visible=True, color = 'red', linestyle = '--')

     for iloop in range(7,10):
         check.lines[iloop][0].set_visible(True)
         check.lines[iloop][1].set_visible(True)

     if textvar1 != 0:
         plt.gcf().texts.remove(textvar1)
         plt.draw()
     textvar1 = plt.figtext(0.7,0.95,'Stack Number is %i' %(numStack),fontsize=16)
     textvar1.set_visible(True)
     plt.pause(0.05)

     plt.xlim(xmax=myXmax)
     plt.xlabel('      TIME in milliseconds')
     plt.ylabel('Signal Amplitude')

     plt.draw()
     return

   def NoStack(self,event):
     global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12,\
         P, PR, PL, PCH1, PCH2, PCH3, PCH4, PCH0butter, PCH1butter,\
         PCH2butter, PCH3butter, Pstack0, Pstack1, Pstack2, Pstack3, ax,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, numStack, deltaTrig
     textvar=plt.figtext(0.62,0.10,'Not Stacked')
     textvar.set_visible(True)
     plt.pause(1)
     textvar.set_visible(False)
     
     if numStack==0:
        #del axArmButton.texts[1]
        return
      
     plt.axes(ax)
     plt.xlim(xmax=myXmax)
     plt.xlabel('      TIME in milliseconds')
     plt.ylabel('Signal Amplitude')
     #del axArmButton.texts[1]
     plt.draw()
     return

   def ClearStack(self,event):
      global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9,l10, l11, l12,\
         P, PR, PL, PCH1, PCH2, PCH3, PCH4, PCH0butter, PCH1butter,\
         PCH2butter, PCH3butter, Pstack0, Pstack1, Pstack2, Pstack3, ax,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, numStack, textvar1, isStackClicked,deltaTrig

      isStackClicked=False
      numStack=0

      if textvar1 != 0:
         plt.gcf().texts.remove(textvar1)
         plt.draw()
      #textvar1 = plt.figtext(0.7,0.95,'Stack Number is %i' %(numStack),fontsize=16)
      textvar1.set_visible(False)
      plt.pause(0.05)
      textvar1 = 0

      l0.set_visible(False)      # Trigger
      l1.set_visible(False)      # Smooth 1
      l2.set_visible(False)      # Smooth 2
      l3.set_visible(False)      # Smooth 3
      l4.set_visible(False)      # Stacked 1
      l5.set_visible(False)      # Stacked 2
      l6.set_visible(False)      # Stacked 3
      l7.set_visible(False)      # Original 1
      l8.set_visible(False)      # Original 2
      l9.set_visible(False)      # Original 3
      l10.set_visible(False)     # Scaled 1
      l11.set_visible(False)     # Scaled 2
      l12.set_visible(False)     # Sacled 3

      for iloop in range(0,13):
         check.lines[iloop][0].set_visible(False)
         check.lines[iloop][1].set_visible(False)

      plt.draw()
      plt.pause(1.)

      Pstack1 = 0.0*Pstack1
      Pstack2 = 0.0*Pstack2
      Pstack3 = 0.0*Pstack3
      PCH1 = 0.0*PCH1
      PCH2 = 0.0*PCH2
      PCH3 = 0.0*PCH3
      PCH1Scaled = PCH1
      PCH2Scaled = PCH2
      PCH3Scaled = PCH3
      PCH1butter = 0.0*PCH1butter
      PCH2butter = 0.0*PCH2butter
      PCH3butter = 0.0*PCH3butter
      PCH0butter = 0.0*PCH0butter

      plt.axes(ax)
      plt.cla()

      return

   def Reset(self,event):
       global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12,\
         P, PR, PL, PCH1, PCH2, PCH3, PCH4, PCH0butter, PCH1butter,\
         PCH2butter, PCH3butter, Pstack0, Pstack1, Pstack2, Pstack3,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, Ymax, Ymin, ax, deltaTrig
         
       Xmax = int(PRETRIG_SECONDS*1000/deltaTrig + sliderXmax.val/deltaTrig) 
       print("Xmax:",Xmax)

       tempMax=0
       tempMin=0
       Ymax=0
       Ymin=0
       y=0
       for x in [PCH0butter[0:Xmax], PCH1Scaled[0:Xmax], PCH2Scaled[0:Xmax],\
                PCH3Scaled[0:Xmax],PCH1[0:Xmax], PCH2[0:Xmax], PCH3[0:Xmax],\
                Pstack1[0:Xmax], Pstack2[0:Xmax], Pstack3[0:Xmax],\
                PCH1butter[0:Xmax], PCH2butter[0:Xmax], PCH3butter[0:Xmax]]:

           if check.lines[y][0].get_visible():

              tempMax = max(x)

              tempMin = min(x)
              if tempMax > Ymax:
                  Ymax = tempMax

              if tempMin < Ymin:
                  Ymin = tempMin

           y = y + 1

       plt.ylim(Ymin, Ymax)
       plt.xlim(xmax=myXmax)
       plt.xlim(xmin=t[0])
       plt.draw()

       return
   
   def ReadFile(self,event):
        global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12,\
         P, PR, PL, PCH1, PCH2, PCH3, PCH4, PCH0butter, PCH1butter,\
         PCH2butter, PCH3butter, Pstack0, Pstack1, Pstack2, Pstack3,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, Ymax, Ymin, ax,deltaTrig
        global locations
        from tkinter import Tk     # from tkinter import Tk for Python 3.x
        from tkinter.filedialog import askopenfilename

        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        seismicfilename = askopenfilename(filetypes=[("csv files", "*.csv;*.CSV")]) # show an "Open" dialog box and return the path to the selected file
        print(seismicfilename) 
        print("i am reading a file now")
        
        textvar=plt.figtext(0.2,0.13,'Reading File')        
        textvar.set_visible(True)
        plt.pause(0.1)
        
        csvFile = open(seismicfilename,"r") 
        print(" i opened the file")
        
        locations=csvFile.readline()

        csvFile.seek(0)  # rewind file to the top again
        df=pd.read_csv(csvFile,header=1)
        
        t=df["aTime"].values
        PCH0butter=df["bTrigger"]
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
        textvar.set_visible(False)
        plt.pause(0.1)
  
     
   def WriteFile(self,event):
        global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12,\
         P, PR, PL, PCH1, PCH2, PCH3, PCH4, PCH0butter, PCH1butter,\
         PCH2butter, PCH3butter, Pstack0, Pstack1, Pstack2, Pstack3,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, Ymax, Ymin, ax,deltaTrig
        global valuefloat,formerValue
        
        from tkinter import Tk     # from tkinter import Tk for Python 3.x
        from tkinter.filedialog import asksaveasfilename

        fields = 'Sledge', 'Geophone 1', 'Geophone 2', 'Geophone 3'
        #valuefloat=[]
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        seismicfilename = asksaveasfilename() # show an "Open" dialog box and return the path to the selected file
        print(seismicfilename)          
        print("i am writing a file now")
        
        textvar=plt.figtext(0.2,0.13,'Writing File')        
        textvar.set_visible(True)
        plt.pause(0.1)
        
        csvFile = open(seismicfilename, "w",newline='') 
        
        if keepOldValue == 0:    #to paste previous values into location window
            formerValue=['0','0','0','0']
        else:
            formerValue=value
            
        def fetch(entries):
            global valuefloat, keepOldValue, value
            value=[]
            valuefloat=[]
        
            for entry in entries:
                #field = entry[0]
                text  = entry[1].get()
                value.append(text)
            
            keepOldValue=1
            
            for x in value:
                valuefloat.append(float(x))
            print(valuefloat)
            return valuefloat
        
        def makeform(window, fields):
            global valuefloat
            entries = []
            index=0
            for field in fields:
            
                row = tk.Frame(window)
        
                lab = tk.Label(row, width=10, text=field, anchor='w')
                ent = tk.Entry(row,width=5)
                row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
                lab.pack(side=tk.LEFT)
                ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
                ent.insert(0,formerValue[index])
                entries.append((field, ent))
                index += 1
            return entries          
        
        window = tk.Tk()
        greeting = tk.Label(window, text="POSITIONS (m)")
        greeting.pack()
        ents = makeform(window, fields)
        window.bind('<Return>', (lambda event, e=ents: fetch(e)))  
        
        window.protocol("WM_DELETE_WINDOW", window.quit)   #so that clicking on 'X' will not cause an error
        
        b1 = tk.Button(window, text='Write to File',
                      command=(lambda e=ents: fetch(e)))
        b1.pack(side=tk.LEFT, padx=5, pady=5)
        b2 = tk.Button(window, text='Quit', command=window.quit)
        b2.pack(side=tk.LEFT, padx=5, pady=5)
    
        window.lift
     
        window.mainloop()
        window.destroy()         


        print('float',valuefloat)
        positions = csv.writer(csvFile) 
        positions.writerow(valuefloat)

        df = pd.DataFrame({"aTime" : t, "bTrigger" : PCH0butter,\
                "cSmoothCH1" : PCH1,"dSmoothCH2" : \
                PCH2,"eSmoothCH3" : PCH3,"fStackCH1" : Pstack1,"gStackCH2" : \
                Pstack2,"hStackCH3" : Pstack3,"iRawCH1" : PCH1butter,"jRawCH2" : \
                PCH2butter,"kRawCH3" : PCH3butter})
        df.to_csv(csvFile, index=False,line_terminator='\n')
        
        csvFile.close()
        print("I finished writing the file")
        textvar.set_visible(False)
        plt.pause(0.1)
        
   def func1(self,label):
       global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12,\
         P, PR, PL, PCH1, PCH2, PCH3, PCH4, PCH0butter, PCH1butter,\
         PCH2butter, PCH3butter, Pstack0, Pstack1, Pstack2, Pstack3,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled, Ymax, Ymin, ax,deltaTrig

       Ymax = 0.0
       Ymin = 0.0

       
       if label == 'Trigger':
           l0.set_visible(check.lines[0][0].get_visible())
       elif label == 'Smoothed 1':
           #print(check.lines[1][0].get_visible())
           l1.set_visible(check.lines[4][0].get_visible())
           #l1, = ax.plot(t,PCH1, visible=l1.get_visible(), color = 'green')
       elif label == 'Smoothed 2':
           l2.set_visible(check.lines[5][0].get_visible())
           #l2, = ax.plot(t,PCH2, visible=l2.get_visible(), color = 'blue')
       elif label == 'Smoothed 3':
           l3.set_visible(check.lines[6][0].get_visible())
           #l3, = ax.plot(t,PCH3, visible=l3.get_visible(), color = 'red')
       elif label == 'Stacked 1':
           l4.set_visible(check.lines[7][0].get_visible())
       elif label == 'Stacked 2':
           l5.set_visible(check.lines[8][0].get_visible())
       elif label == 'Stacked 3':
           l6.set_visible(check.lines[9][0].get_visible())
       elif label == 'Geophone 1':
           l7.set_visible(check.lines[10][0].get_visible())
       elif label == 'Geophone 2':
           l8.set_visible(check.lines[11][0].get_visible())
       elif label == 'Geophone 3':
           l9.set_visible(check.lines[12][0].get_visible())
       elif label == 'Scaled 1':
           l10.set_visible(check.lines[1][0].get_visible())
       elif label == 'Scaled 2':
           l11.set_visible(check.lines[2][0].get_visible())
       elif label == 'Scaled 3':
           l12.set_visible(check.lines[3][0].get_visible())
       plt.draw()
       return

def update(val):
   global myXmax, t, l0, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12,\
         P, PR, PL, PCH1, PCH2, PCH3, PCH4, PCH0butter, PCH1butter,\
         PCH2butter, PCH3butter, Pstack0, Pstack1, Pstack2, Pstack3, ax,\
         PCH1Scaled, PCH2Scaled, PCH3Scaled,deltaTrig
   myXmax = sliderXmax.val
   plt.axes(ax)
   plt.xlim(xmax = myXmax)
   plt.xlabel('      TIME in milliseconds')
   plt.ylabel('Signal Amplitude')
   plt.draw()
   return

callback = ButtonClass()
bArm.on_clicked(callback.Arm)
bPlot.on_clicked(callback.PlotCurves)
bYesStack.on_clicked(callback.YesStack)
bNoStack.on_clicked(callback.NoStack)
bClearStack.on_clicked(callback.ClearStack)
bResetButton.on_clicked(callback.Reset)
bWriteFile.on_clicked(callback.WriteFile)
bReadFile.on_clicked(callback.ReadFile)
check.on_clicked(callback.func1)

axcolor = 'lightgoldenrodyellow'
axXmax = plt.axes([0.25, 0.01, 0.65, 0.02], facecolor=axcolor)
sliderSize = RECORD_SECONDS*1000.
sliderXmax = plt.Slider(axXmax, 'Maximum Time', 1.0, sliderSize, valinit=150.)

sliderXmax.on_changed(update)
plt.show()
plt.draw()


