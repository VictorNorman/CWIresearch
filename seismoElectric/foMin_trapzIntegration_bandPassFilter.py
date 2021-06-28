# -*- coding: utf-8 -*-

# this program does sinusoid subtraction (butler and Russell 1993)
# It removes the periodic noise fom the seismoelectric signal
# It uses a trapezoidal integration on the data values
# It also finds the dominant harmonic frequency


import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from scipy.signal import freqz

#plt.style.use('ggplot')
mypath="C:/SeismicSoftware/BenSeismoelectric/"
#mypath="C:/SeismicSoftware/telShimronSeismoelectric/"
datafile=mypath+'seismoelectric10-4-trial4-20hits-8m.csv'

my_data = np.loadtxt(datafile, delimiter=',',usecols=(0,5,7),skiprows=1)

my_data_scaled=my_data

t_original=my_data[:,0]
t_length=len(t_original)
#print(t_original[0])

#convert time to start at 0 for pretrig instead of -15 and change from ms to s
t=(t_original-t_original[0])/1000. 
time_total=t[t_length-1] - t[0]

k=np.arange(t_length)
sample_rate=96000
sample_rate=192000
T=t_length/sample_rate
frq=k/T
intN=int(t_length/2)
frq=frq[range(intN)]

rmax1=max(my_data[:,1])
rmax2=max(my_data[:,2])

print(rmax1,rmax2)

my_data_scaled[:,1]=my_data[:,1]/rmax1
my_data_scaled[:,2]=my_data[:,2]/rmax2             
 
#r=my_data_scaled[:,1]
#r=my_data[:,2]
#r=my_data_scaled[:,1]+my_data_scaled[:,2]
r=my_data[:,1]+my_data[:,2]
#to use late times for 'no signal' times - reverse the values
#r_up=my_data[:,1]
#r=np.flipud(r_up) 

rf=(np.abs(np.fft.rfft(r)))
plt.figure(9)
plt.plot(frq[0:500],rf[0:500])
plt.yscale('log')
plt.xlabel('Frequency ( Hz)') 
plt.ylabel('Fourrier Amplitude')
plt.title('fourrier analysis of raw data')
Fo=50.00        #fundamental frequency in Hz
DF=0.03         #Fo +- this value
df=0.0001       # increment


Fo = float(input("enter the fundamental frequency:  \n"))
DF=float(input("enter the differential range in the freq:  \n"))
df=float(input("enter the frequency increment betwee the range:  \n"))

num_harmonics=60    #number of harmonics to use

fomin=Fo-DF
fomax=Fo+DF
oldssq=1.e10
    
for fo in np.arange(fomin,fomax,df):
    tau=8./fo     # cycles of fundamental freq for sample

    for m in range(0,t_length-1):
        if t[m] >= tau:
            break
    tau_index=m   # index for even cycles
    #print("tau_index is  ", tau_index, t[tau_index])

    wo=2*np.pi*fo   # wave number
    # sample record without signal
    r_slice=r[0:tau_index]
    t_slice=t[0:tau_index]
    
    plt.figure(1)
    plt.plot(t_slice,r_slice,'-')
    plt.title('pretrigger periodic noise')
    plt.figure(2)
    plt.plot(t,r,'-')
    plt.title('raw signal')
    
    # amplitudes for best fitting harmonics
    an=[0]
    bn=[0]
    
    for n in range(1,num_harmonics,1):
    
        alpha1=(tau/2.) + (np.sin(2*n*wo*tau)/(4*n*wo))
        alpha2=(1-np.cos(2*n*wo*tau))/(4*n*wo)
        alpha3=(tau/2.)-(np.sin(2*n*wo*tau)/(4*n*wo))
        beta=1/(alpha1*alpha3-alpha2*alpha2)
                
        integrandA=r_slice*((alpha3*np.cos(n*wo*t_slice))-(alpha2*np.sin(n*wo*t_slice)))
        integralA=beta*np.trapz(integrandA,t_slice)
        an.append(integralA)
        integrandB=r_slice*((alpha1*np.sin(n*wo*t_slice))-(alpha2*np.cos(n*wo*t_slice)))
        integralB=beta*np.trapz(integrandB,t_slice)
        bn.append(integralB)
  
    p=[0]   # best esimate for hamonic part of record
    p_n=[0]
    
    for kk in range(1,num_harmonics,1):  
        p_n=(an[kk]*np.cos(kk*wo*t)+bn[kk]*np.sin(kk*wo*t))
        p=np.add(p,p_n)
        #print(kk,an[kk],bn[kk])
    
    diff=r-p    #the answer after subtracting harmonic noise
    
    ssq=np.sum(diff**2)     # sum of squares for signal
    
    # check if recent diff is smaller than previous small value
    if ssq <= oldssq:
        oldssq=ssq
        newfo=fo
        newdiff=diff
        new_an=an
        new_bn=bn
        
    print(fo,newfo,ssq,oldssq)  #print ssq for recent and smallest
    
cn=[0]      #amplitude for frequency n
freq=[0]
for nth in range(1,num_harmonics-1,1):
    cn.append(np.sqrt(new_an[nth]**2 + new_bn[nth]**2))
    freq.append(newfo*nth)

print(freq)  
fs = 1./(time_total/(len(newdiff)))
    
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y

lowcut = 100.0
#lowcut=500.0
highcut = 500.

# Plot the frequency response for a few different orders.
plt.figure(7)
#plt.clf()
for order in [1,2,3]:
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    w, h = freqz(b, a, worN=200000)
    x=(fs * 0.5 / np.pi) * w
    y=abs(h)
    plt.xlim(0,1000)
    plt.plot(x,y,label="order = %d" % order)
    #plt.plot((fs * 0.5 / np.pi) * w[0:200], abs(h[0:200]), label="order = %d" % order)

plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
         '--', label='sqrt(0.5)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.title('butterworth filter range')
plt.grid(True)
plt.legend(loc='best')
plt.show()

   
plt.figure(3)
plt.plot(t,p,'-')
plt.title('periodic noise that is removed from the data')
plt.figure(4)
plt.plot(t,newdiff,'-')
plt.title('with periodic noise removed')
plt.figure(5)
plt.yscale('log')
plt.xscale('log')
plt.title('spectrum of periodic noise removed')
plt.bar(freq[1::],cn[1::], width=10.)
plt.show()

plt.figure(8)
pbutter = butter_bandpass_filter(newdiff, lowcut, highcut, fs, order=3)
xs=str(lowcut)+'  -  ' + str(highcut) + '  Hz ' +'Order = ' + str(order)
plt.plot(t, pbutter,label='Bandpass Filtered signal %s' % xs)
plt.xlabel('time (seconds)')
#plt.hlines([-a, a], 0, T, linestyles='--')

plt.grid(True)
plt.axis('tight')
plt.legend(loc='upper left')

plt.show()






