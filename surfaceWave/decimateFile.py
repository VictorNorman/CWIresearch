# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 20:17:18 2018

@author: Jim Clark
"""

import numpy as np
import matplotlib.pyplot as plt
from sys import exit
import cmath as cm
from scipy import stats
#import nitime.algorithms as tsa

mypath="C:/SeismicSoftware/SurfaceWaves/"
#datafile=mypath+'MASW/maswMyformat.csv'
#datafile=mypath+'sineFileTest.csv'
#datafile=mypath+'AllWavessorted2.csv'
datafile=mypath+'sineFileTest2Modes.csv'
#datafile=mypath+'sineFileTest2Modes2F3.csv'
#datafile=mypath+'MASW/MASW4.csv'
decimateBy=25
with open(datafile) as fin:
    lines = fin.readlines()
fin.close()
#desired_lines = lines[start:end:step]

desired_lines = lines[0::decimateBy]

f=datafile[:-4] + '_'+'By'+str(decimateBy)+'out.csv'
print(f)
with open(f,"w") as fout:
    fout.writelines(desired_lines)
fout.close()
