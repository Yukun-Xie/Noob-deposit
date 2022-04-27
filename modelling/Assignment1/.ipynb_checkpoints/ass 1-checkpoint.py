# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# group 8 work 1
#Water Balance of the Wieringermeer Landfill
#-Assignment 1 for course CIE4365
#@author: Yiman Liu      5456703
#         Yuwei Huang    5555566
#         Yukun Xie
#         Mingkai Wei

import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
#%matplotlib inline

def tic():
    #Homemade version of matlab tic and toc functions
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()

def toc():
    import time
    if 'startTime_for_tictoc' in globals():
        print ("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print ("Toc: start time not set")

import pandas as pd
data1 = pd.read_excel('WieringermeerData_Meteo.xlsx', sheet_name=None, index_col=0, parse_dates=[0])
data2 = pd.read_excel('WieringermeerData_LeachateProduction.xlsx', sheet_name=None,index_col=0, parse_dates=[0])
J = data1.iloc[:, 0]
EV = data1.iloc[:, 1]
T = data1.iloc[:, 2]
L = data2.iloc[:, 0]       

# Definition of parameters
Ac = 28355       #m^2, surface area of waste body
Aw = 9100        #m^2, surface area of cover layer
beta0 = 0.8      #range 0-2.5
p = 0.4          #Soil porosity
a = 0.2          #10*(-1) - 10**4 [m/day]
bcl = 8.2        #dimensionless empirical parameter
bwb = 20         #dimensionless empirical parameter
Vcl = Ac * 1.5   #m^3, volume 
Vwb = Aw * 12    #m^3, volume
sclmin=0.5       #m, minimum storage in the cover layer
swbmin=0.5       #m, minimum storage in the waste body
sclmax=1.5 * p   #m, maximum storage in the cover layer 
swbmax=12 * p    #m, maximum storage in the waste body
semin=EV.min()
semax=EV.max()
Cf = 0.7         #crop factor
pcl = 0.6
pwb = 0.4
Q = np.zeros(len(J))

Y0 = np.array([0.6,1.5])
Y0t = np.array([1.2,12])
    
# Definition of Rate Equation
# Value correction
def dYdt(t, Y):
    if Y[0] < sclmin:
        fred = 0
    elif semin <= Y[0] <= semax:
        fred = (Y[0] - semin) / (semax - semin)
    elif Y[0] > semax:
        fred = 1

    et = EV[int(t)] * Cf * fred
    beta = beta0 * ((Y[0] - sclmin) / (sclmax -sclmin))
    lcl = a * ((Y[0] - sclmin) / (sclmax -sclmin)) ** bcl   
    lwb = a * ((Y[1] - swbmin) / (swbmax -swbmin)) ** bwb
    return np.array([J[int(t)] - lcl - et, (1 - beta) * lcl - lwb])

# Definition of output times 
tOut = np.linspace(0, len(J), len(J))  
nOut = np.shape(tOut)[0]

import scipy.integrate as spint

tic()
t_span = [tOut[0], tOut[-1]]
YODE = spint.solve_ivp(dYdt, t_span, Y0, t_eval=tOut, vectorized=True,
                      method='RK45', rtol=1e-5)
# infodict['message']                     # >>> 'Integration successful.'
ScODE = YODE.y[0,:]
SwODE = YODE.y[1,:]

toc()

plt.figure()
plt.plot(tOut, SwODE, 'r-', label='sw')
plt.plot(tOut, ScODE  , 'b-', label='sc')

plt.grid()
plt.legend(loc='best')
plt.xlabel('time')
plt.ylabel('water storage[m]')
plt.title('Water storage of the cover layer and the waste body')