# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:30:10 2015

@author: u0098627
"""
import os
import numpy as np
import matplotlib.pyplot as plt


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
class WindFarm(object):
    def __init__(self, **kwargs):
        self.turbines   = []
        self.datadir    = kwargs.get('datadir', None)
        self.layout     = kwargs.get('layout', None)
        self.nRow       = kwargs.get('nRow', None)
        self.nCol       = kwargs.get('nCol', None)
        self.nTurb      = kwargs.get('nTurb', None)
        self.t          = kwargs.get('t', None)

        if self.datadir is not None:     
            data            = np.loadtxt(self.datadir, skiprows = 1)
            self.nTurb      = (np.shape(data)[1]-1)/2
            self.t          = data[:,0]
            print self.nTurb
            for i in range(self.nTurb):
                row = i/self.nCol
                self.turbines.append(WindTurb(power = -data[:,2*i+2], row = row))
            
    def __add__(self,other):
        sumWindFarm = WindFarm(layout = self.layout, nRow = self.nRow,
                               nCol = self.nCol, nTurb = self.nTurb, t = self.t)
        for turbArg1, turbArg2   in zip(self.turbines, other.turbines):
            sumWindFarm.turbines.append(turbArg1+turbArg2)
        return sumWindFarm
        
    def __sub__(self,other):
        subWindFarm = WindFarm(layout = self.layout, nRow = self.nRow,
                               nCol = self.nCol, nTurb = self.nTurb, t = self.t)
        for turbArg1, turbArg2   in zip(self.turbines, other.turbines):
            subWindFarm.turbines.append(turbArg1-turbArg2)
        return subWindFarm                       
        
    def __mul__(self,other):
        mulWindFarm = WindFarm(layout = self.layout, nRow = self.nRow,
                               nCol = self.nCol, nTurb = self.nTurb, t = self.t)
        if isinstance(other,int) or isinstance(other,float):
            for turbArg1   in self.turbines:
                mulWindFarm.turbines.append(other*turbArg1)
        elif isinstance(other,WindFarm):
            for turbArg1, turbArg2  in zip(self.turbines, other.turbines):
                mulWindFarm.turbines.append(turbArg1*turbArg2)
        return mulWindFarm 
        
    def __rmul__(self,other):
        return self.__mul__(other) 
        
    def __div__(self,other):
        print 'test'
        print other
        return self.__mul__(1/float(other))
        
#    def addTurbine(self,position = None, D = None, power = None): 
#        return WindTurb(position = position, D = D, power = power)
        
    def meanPowerFarm(self):
        return np.mean([turbine.powerMean for turbine in self.turbines])   
    
    def meanPowerRows(self):
        meanPowerRows = np.zeros(self.nRow)
        for turbine in self.turbines:
            meanPowerRows[turbine.row-1] += turbine.powerMean
        meanPowerRows /= self.nCol   
        return meanPowerRows
        
    def powerFarm(self):
        powerFarm = np.zeros(np.size(self.t))
        for turbine in self.turbines:
            powerFarm += turbine.power
        powerFarm /= self.nTurb 
        return powerFarm
        
    def powerRows(self):
        powerRows = np.zeros((np.size(self.t),self.nRow))
        for turbine in self.turbines:
            powerRows[:,turbine.row-1] += turbine.power
        powerRows /= self.nCol        
        return powerRows         
        
class WindTurb(object):
    def __init__(self, position = None, row = None, D = None, power = None):              
        self.position   = position
        self.D          = D
        self.power      = power
        self.row        = row
        self.powerMean  = np.mean(power)
        
    def __add__(self,other):
        return WindTurb(self.position, self.row, self.D, 
                        self.power + other.power)
                        
    def __sub__(self,other):
        return WindTurb(self.position, self.row, self.D, 
                        self.power - other.power)                  
                        
    def __mul__(self,other):
        if isinstance(other,int) or isinstance(other,float):
            mulWindTurb = WindTurb(self.position, self.row, self.D, 
                        other*self.power)
        elif isinstance(other,WindTurb):
            mulWindTurb = WindTurb(self.position, self.row, self.D, 
                        self.power*other.power)   
        return mulWindTurb
           
    def __rmul__(self,other):    
        return self.__mul__(other)
                
datadir1 = 'C:/Users/u0098627/Documents/Doctoraat/Supercluster/Simulaties/'\
            'BL_sim_finite_M576x256x128_WT14x10startupPowerDataV2/Aligned/'\
            'Windpower1.dat'
aligned1 = WindFarm(datadir = datadir1, nCol = 10, nRow = 14)

datadir2 = 'C:/Users/u0098627/Documents/Doctoraat/Supercluster/Simulaties/'\
            'BL_sim_finite_M576x256x128_WT14x10startupPowerDataV2/Aligned/'\
            'Windpower3.dat'
aligned2 = WindFarm(datadir = datadir2, nCol = 10, nRow = 14)
#print aligned1

#meanAligned = aligned1 + aligned2
print aligned1.meanPowerRows()
print aligned2.meanPowerRows()

print aligned1.meanPowerFarm()
print aligned2.meanPowerFarm()

print aligned1.powerFarm()
print aligned2.powerFarm()

meanAligned  = (aligned1 + aligned2)*0.5
meanAligned2 = (aligned1 + aligned2)/2

multAligned = aligned1*aligned2
test = meanAligned - meanAligned2

print meanAligned
print meanAligned2
plt.close('all')
plt.figure()
plt.plot(aligned1.t,multAligned.powerFarm())
plt.figure()
plt.plot(aligned1.t,aligned1.powerFarm(),aligned2.t,aligned2.powerFarm(),\
         meanAligned.t, meanAligned.powerFarm(),meanAligned2.t, meanAligned2.powerFarm())
plt.figure()
plt.plot(meanAligned2.t,meanAligned.powerFarm())
plt.figure()
plt.plot(meanAligned2.t,meanAligned2.powerFarm())
plt.figure()
plt.plot(meanAligned2.t,test.powerFarm())