# -*- coding: utf-8 -*-
"""
Script to convert pressure values into flow rate by interpolating a baseline

@author: devon
"""


import numpy as np
import pandas as pd
    
def Pythonbaselinetracker(pressure, calibration_factor):
    m = len(pressure)
    baseline = np.zeros(int(np.floor(m/600)))#Preallocate baseline values
    flow = np.zeros(m) #Preallocate flow values
    
    #Get a point for a baseline every 600 data points
    for j in range(m-1,599,-600):
        temp = (pressure.iloc[j-600:j])
        temp = temp.reset_index(drop=True)
        baseline[int(np.floor(j/600))-1] = np.percentile(temp,25)
    
    #Interpolate to get a full baseline
    index_end = m
    index_start = m-(600*len(baseline))
    baseline_index = list(range(index_start,index_end,600))
    baseline_interp = np.interp(list(range(m)),baseline_index,baseline)
    
    #Convert pressure to flow 
    flow = np.subtract(pressure.iloc[:,0],baseline_interp)
    flow = flow*4.11
    flow = np.divide(flow,600)
    flowsign = np.sign(flow)
    flow = np.abs(flow)
    flow = np.sqrt(flow)
    flow = np.multiply(flow,calibration_factor)
    flow = np.multiply(flow,flowsign)
    
    #Get rid of likely noise
    flow[flow < 5] = 0
    
    return(flow,baseline_interp)
    
if __name__ == '__main__':
    pressure = pd.read_csv('sampledata.csv') #sample file with a pressure signal
    calibration_factor = 4.11 #device specific
    [flow,baseline_interp] = Pythonbaselinetracker(pressure,calibration_factor)