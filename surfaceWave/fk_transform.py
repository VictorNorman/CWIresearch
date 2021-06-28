# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:48:15 2020

@author: Jim Clark
"""

import numpy as np

import matplotlib.pyplot as plt
from scipy import stats, fft
import nitime.algorithms as tsa
import cmath as cm

mypath="C:/SeismicSoftware/SurfaceWaves/"
#datafile=mypath+'MASW/maswMyformat.csv'
#datafile=mypath+'sineFileTest.csv
#datafile=mypath+'sineFileTest_By25out.csv'
#datafile=mypath+'AllWavessorted2.csv'
#datafile=mypath+'AllWavessorted2_By50out.csv'
#datafile=mypath+'sineFileTest2Modes.csv'
#datafile=mypath+'sineFileTest2Modes_By25out.csv'
datafile=mypath+'sineFileTest2Modes2F3.csv'
#datafile=mypath+'MASW/MASW4.csv'


f_desired=80
k_desired=3
ft2m=0.3048
#ft2m=1
my_input = np.loadtxt(datafile, delimiter=',')

original_rows,original_cols=my_input.shape
print('original_rows=  ', original_rows,'  original_ cols =  ', original_cols)

trace_data=np.array(my_input[1:,1:])
trace_data=trace_data/10000

rows,cols=trace_data.shape
#rows=int(0.8*rows+1)   #kluge to eliminate lst 20
print('rows cols',rows,cols)
num_traces=cols

x_data=np.array(my_input[0,1:]) #read the first line of distancees (in meters)

x=np.zeros((cols+1))        #"dimension the arrays"
#trace=np.zeros((rows+2,cols+2))
trace=np.zeros([rows+2,cols+1000])
#make the seismic data go from subscript 1 for trace and distance but  0 for time
for i in range(0,rows):
    for j in range(1,cols+1):
        trace[i][j]=trace_data[i][j-1]

for i in range(1,cols+1):
    x[i]=x_data[i-1]

print('distance=  ',x[1:cols+1])

newrows,newcols=trace.shape
print(newrows,newcols)
t=np.array(my_input[1:,0]/1000)
plt.figure(1)    #coonvert milliseconds to seconds
for m in range(0,cols):
    plt.plot(t,trace[0:rows,m])
plt.show()


t=t-t[0]
dt=t[2]-t[1]
print('dt is  ', dt)
print('t for 10 pts ', t[0:10])
t_length=len(t)

fkoriginal=fft.fft2(trace,axes=(0,1))
#fk = fft.fftshift(fkoriginal)
realfk=np.abs(fkoriginal)
print('realfk shape',realfk.shape)
realfkTranspose=np.transpose(realfk)

print(fkoriginal[1,1])
freq = fft.fftfreq(newrows, d=dt)
freq = np.array( [ num for num in freq if num > 0 ] )
f_desired_index=np.max(np.where(freq<f_desired)) 
dk=abs(x[2]-x[1])*ft2m
wavenumber=fft.fftfreq(newcols,d=dk)
wavenumber = np.array( [ num for num in wavenumber if num > 0 ] )
k_desired_index=np.max(np.where(wavenumber<k_desired)) 
print('desired index   ',f_desired_index,k_desired_index)
maxfreq=freq[f_desired_index]
maxwavenumber=wavenumber[k_desired_index]
print(maxfreq,maxwavenumber)
print('frequencies',freq[0:10], wavenumber[0:10])
print('realfk shape,rows and cols  ', realfk[0:f_desired_index,0:k_desired_index].shape)
#plt.imshow(realfkTranspose[0:f_desired_index, 0:k_desired_index],cmap='jet',interpolation='bilinear',\
plt.figure(2)
plt.imshow(realfk[0:f_desired_index, 0:3*k_desired_index],cmap='jet',\
           extent=[0,maxwavenumber,0,maxfreq],\
           aspect='auto',origin='lower')
    