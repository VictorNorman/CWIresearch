# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 22:58:43 2017

@author: jclark

this surface wave dispersion code uses the cross spectral phase shift
between every 2 pairs of geophones to determine a best fit line for each frequency. 
the coherence determines how close in form the 2 waves are. If coherence is
less than 0.5 then the points for that frequency are not used.
Method2 uses the same points but constructs the "Park style" plot
method3 just uses the first offset points from the first trace - 
typically about 24 traces
"""
import numpy as np

import matplotlib.pyplot as plt
from scipy import stats
import nitime.algorithms as tsa
# see https://nipy.org/nitime/py-modindex.html
import cmath as cm

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
#    window=tk.Tk()

seismicfilename = askopenfilename(filetypes=[("csv files", "*.csv;*.CSV")]) # show an "Open" dialog box and return the path to the selected file
geophoneLocations=[]
csvFile = open(seismicfilename,"r") 

#THESE FILES WILL NOT WORK BECUASE THEY HAVE DIFFERENT HEADERS
#USE THEM WITH PY3_SEISSURFACEwAVEScROSSSPECTRAL3.PY
#mypath="C:/SeismicSoftware/SurfaceWaves/"
#datafile=mypath+'MASW/maswMyformat.csv'
#datafile=mypath+'sineFileTest.csv
#datafile=mypath+'sineFileTest_By25out.csv'
#datafile=mypath+'AllWavessorted2.csv'
#datafile=mypath+'AllWavessorted2_By50out.csv'
#datafile=mypath+'sineFileTest2Modes.csv'
#datafile=mypath+'sineFileTest2Modes_By25out.csv'

#datafile=mypath+'sineFileTest2Modes2F3.csv'
#datafile=mypath+'MASW/MASW4.csv'
datafile=csvFile

my_input = np.loadtxt(datafile, delimiter=',')
csvFile.close()

original_rows,original_cols=my_input.shape
print('original_rows=  ', original_rows,'  original_ cols =  ', original_cols)

trace_data=np.array(my_input[3:,1:])
rows,cols=trace_data.shape
#rows=int(0.8*rows+1)   #kluge to eliminate lst 20
num_traces=cols

x_data=np.array(my_input[2,1:]) #read the first line of distancees (in meters)

x=np.zeros((cols+1))        #"dimension the arrays"
trace=np.zeros((rows+2,cols+2))
#make the seismic data go from subscript 1 for trace and distance but  0 for time
for i in range(0,rows):
    for j in range(1,cols+1):
        trace[i][j]=trace_data[i][j-1]

for i in range(1,cols+1):
    x[i]=x_data[i-1]
print('distance=  ',x[1:cols+1])

t=np.array(my_input[3:,0]/1000.)    #coonvert milliseconds to seconds
t=t-t[0]
dt=t[2]-t[1]
print('dt is  ', dt)
print('t for 10 pts ', t[0:10])
t_length=len(t)

frq_desired=45     #maximum frequency desired in Hz
cmax=1500.      #maximum phase velocity in m/s
cmin=30.    #minimum phase velocity in m/s
min_coherence=0.5    #minimum coherence value for a pt to be included
start_index=100    #this eliminates the p a s wave "noise" by startinglater

def dB(x, out=None):
    if out is None:
        return 10 * np.log10(x)
    else:
        np.log10(x, out)
        np.multiply(out, 10, out)
def mtem(i, j, dt):
    """
    multitaper estimation method
    Input:
    i      first time series
    j      second time series

    Output:
    fki    power spectral density i
    fkj    power spectral density j
    cij    cross-spectral density ij
    coh    coherence
    ph     phase spectrum between ij at input freq
    
    """
    #print( 'i size', i.shape)
    #print( 'j size', j.shape)
    
    # apply multi taper cross spectral density from nitime module
    f, pcsd_est = tsa.multi_taper_csd(np.vstack([i,j]), Fs=1/dt, \
            low_bias=True, adaptive=True, sides='onesided')
    
    # output is MxMxN matrix, extract the psd and csd
    fki = pcsd_est.diagonal().T[0]
    fkj = pcsd_est.diagonal().T[1]
    cij = pcsd_est.diagonal(+1).T.ravel()
    
    # using complex argument of cxy extract phase component
    ph = np.angle(cij)
    
    # calculate coherence using csd and psd
    coh = np.abs(cij)**2 / (fki * fkj)   
    
    return f, fki, fkj, cij, ph, coh 

def mtem_unct(i_, j_, dt_, cf, mc_no=20):
    """
    Uncertainty function using Monte Carlo analysis
    Input:
    i_     timeseries i
    j_     timeseries j
    cf     coherence function between i and j
    mc_no  number of iterations default is 20, minimum is 3
    
    Output:
    phif   phase uncertainty bounded between 0 and pi
    """
    print( 'iteration no is', mc_no)
    
    data = np.vstack([i_,j_])
    # number of iterations
    # flip coherence and horizontal stack    
    cg = np.hstack((cf[:-1], np.flipud(cf[:-1])))
    
    # random time series fi
    mc_fi = np.random.standard_normal(size=(mc_no,len(data[0])))
    mc_fi = mc_fi / np.sum(abs(mc_fi),axis=1)[None].T
    
    # random time series fj
    mc_fj = np.random.standard_normal(size=(mc_no,len(data[0])))
    mc_fj = mc_fj / np.sum(abs(mc_fj),axis=1)[None].T
    
    # create semi random timeseries based on magnitude squared coherence
    # and inverse fourier transform for js
    js = np.real(np.fft.ifft(mc_fj * np.sqrt(1 - cg ** 2))) 
    js_ = js + np.real(np.fft.ifft(mc_fi *cg))
    
    # inverse fourier transform for xs
    is_ = np.real(np.fft.ifft(mc_fi))
    
    # spectral analysis
    f_s, pcsd_est = tsa.multi_taper_csd(np.vstack([is_,js_]), Fs=1/dt_, low_bias=True, adaptive=True, sides='onesided')
    cijx = pcsd_est.diagonal(+int(is_.shape[0])).T
    phi = np.angle(cijx)
    
    # sort and average the highest uncertianties
    pl = int(round(0.95*mc_no)+1)
    phi = np.sort(phi,axis=0)        
    phi = phi[((mc_no+1)-pl):pl]
    phi = np.array([phi[pl-2,:],-phi[pl-mc_no,:]])
    phi = phi.mean(axis=0)#
    phi = np.convolve(phi, np.array([1,1,1])/3)
    phif = phi[1:-1]
    return phif

#this just finds the number of frequencies to use
f1=np.zeros((rows))
f2=np.zeros((rows))

for q in range(0,rows): 
    f1[q]=trace[q][2]
    f2[q]=trace[q][3]

f,ps1,ps2,cij,ph,coh=mtem(f1,f2,dt)
print('f shape ', f.shape)

#find the index of the max frequency desired
frq_desired_index=np.max(np.where(f<frq_desired))   

#dimension numpy arrays so that subscripts can be used
distance=np.zeros(((num_traces-1)**2))
d=np.zeros(((num_traces-1)**2))
F=np.zeros((frq_desired_index,(num_traces-1)**2))
PS1=np.zeros((frq_desired_index,(num_traces-1)**2))
PS2=np.zeros((frq_desired_index,(num_traces-1)**2))
CIJ=np.zeros((frq_desired_index,(num_traces-1)**2))
PH=np.zeros((frq_desired_index,(num_traces-1)**2))
COH=np.zeros((frq_desired_index,(num_traces-1)**2))
s1=np.zeros((rows))
s2=np.zeros((rows))

#loop over all possible combinations of pairs of traces
sum_pts=0
for m in range(1,num_traces):
    for n in range(m+1, num_traces+1):
        #print(' m and n  ', m,n)
        sum_pts=sum_pts+1
        for q in range(0,rows): 
            s1[q]=trace[q][m]
            s2[q]=trace[q][n]
            
        f,ps1,ps2,cij,ph,coh=mtem(s1,s2,dt)
        distance[sum_pts]=x[n]-x[m]
        
        for r in range(0,frq_desired_index):
            F[r][sum_pts]=f[r]
            PS1[r][sum_pts]=ps1[r]
            PS2[r][sum_pts]=ps2[r]
            CIJ[r][sum_pts]=cij[r]
            PH[r][sum_pts]=ph[r]
            COH[r][sum_pts]=coh[r]

#Method 1: find the regression slope of phase shift each frequency wrt distance
plt.figure(1)
for jj in range(1,frq_desired_index,1):
    p=np.zeros(((num_traces-1)**2))
    sum_good_pts=0
    for kk in range(1,sum_pts+1):
        if COH[jj][kk]> min_coherence:    # check to see if coherence is > 0.5
            sum_good_pts=sum_good_pts+1
            p[sum_good_pts]=PH[jj][kk]
            d[sum_good_pts]=distance[kk]
            
    #sort based upon distance so the unwrapping can occur properly
    inds=d.argsort()
    p=p[inds]
    d=d[inds]
    p=np.unwrap(p)      #since p only goes from - pi to + pi unwrap it
    #print('frequency and sum_good_pts', F[jj][sum_pts], sum_good_pts)
    slope, intercept, r_value, p_value, std_err = stats.linregress(d[1:sum_good_pts],p[1:sum_good_pts])
    v=np.pi*2*F[jj][sum_pts]/slope
    print('lin reg ', F[jj][sum_pts],v,slope,p_value,r_value)
    #plt.plot(d[1:sum_good_pts],p[1:sum_good_pts],marker='o',linestyle='None')
    if p_value<0.01 and len(p)> 5:      #if the regression line is not significant don't use it
        plt.plot(F[jj][sum_pts],abs(v),marker='o',linestyle='None')
   # plt.show()

# Method 2: Use all possible phase shifts to generate a "Park-style" curve
c_list=np.arange(cmin,cmax,1)   #list of all trial c velocities in m/sec
c_length=len(c_list)
print(' first c values  ', c_list[0:10])

print('total possible good points is  ', (num_traces-1)*num_traces/2.)

VV=np.zeros((c_length,frq_desired_index))

for f_index in range(0,frq_desired_index,1):
    p=np.zeros(((num_traces-1)**2))
    sum_good_pts=0
    for kk in range(1,sum_pts+1):
        if COH[f_index][kk]>min_coherence:    # check to see if coherence is > 0.5
            sum_good_pts=sum_good_pts+1
            p[sum_good_pts]=PH[f_index][kk]
            d[sum_good_pts]=distance[kk]

    print('frequency and number good points', f[f_index],sum_good_pts)  
    
    #sort based upon distance so the unwrapping can occur properly
    inds=d.argsort()
    p=p[inds]
    d=d[inds]
    p=np.unwrap(p)      #since p only goes from - pi to + pi unwrap it
    
    for m in range(0,c_length):
        c=c_list[m]       
        z=np.zeros((sum_good_pts),dtype=np.complex_)

        for good_pt in range(1,sum_good_pts,1):
            arg=np.pi*2*f[f_index]*(d[good_pt])/c
            argphi=(0.-1.j)*arg

            UU=np.exp((0.+1.j)*p[good_pt])
            z[good_pt]=UU*np.exp(argphi)

        VV[m][f_index]=np.abs(sum(z))/sum_good_pts
        
plt.figure(2)
plt.imshow(VV,cmap='jet',interpolation='bilinear',\
           origin='lower',aspect='auto',extent=[0,f[frq_desired_index],0, \
           c_list[c_length-1]])
plt.show()

#Method 3: only phase shift from initial trace
U=np.zeros((num_traces,frq_desired_index),dtype=np.complex_)
for itrace in range(1,num_traces,1):  
    phases=np.unwrap(PH[0:frq_desired_index,itrace])
    U[itrace]=np.exp((0.+1.j)*phases)

print('U rows and cols =   ', U.shape)
V=np.zeros((c_length,frq_desired_index))
vplot=[]

for f_index in range(0,frq_desired_index,1):

    for m in range(0,c_length):
        c=c_list[m]     
        z=np.zeros((num_traces),dtype=np.complex_)

        for itrace in range(1,num_traces):
            arg=np.pi*2*f[f_index]*(x[itrace])/c
            argphi=(0.-1.j)*arg

            z[itrace]=U[itrace,f_index]*cm.exp(argphi)

        V[m][f_index]=np.abs(sum(z))/num_traces
        
print('V rows and cols  ', V.shape)

plt.figure(3)

c_index=np.max(np.where(c_list < 200))
for jjj in range(c_index-10,c_index,1):
    print('c_list  and jjj ', c_list[jjj],jjj)
    lab=str(c_list[jjj])
    vplot=V[jjj,0:400]
    plt.plot(f[0:frq_desired_index],vplot[0:frq_desired_index],label=lab)
plt.legend()
plt.show()   


plt.figure(4)

print(' length clist and frq', len(c_list), c_length,len(f[0:frq_desired_index]))

plt.imshow(V,cmap='jet',interpolation='bilinear',\
           origin='lower',aspect='auto',extent=[0,f[frq_desired_index],0, c_list[c_length-1]])

plt.show()