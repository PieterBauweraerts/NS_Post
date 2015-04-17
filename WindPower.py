# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:30:10 2015

@author: u0098627
"""
import os
import numpy as np

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
class WindFarm(object):
    def __init__(self,datadir):
        data            = np.loadtxt(datadir, skiprows = 1)
        self.t          = data[:][1]
        self.turbines   = []
        self.layout     = 'Aligned'
        self.rows       = 14
        self.columns    = 10
        
        for i in range((np.shape(data)[1]-1)/2):
            self.turbines.append(self.addTurbine(power = data[:,2*i+2]))
        
#    def addTurbine(self,position = None, D = None, power = None): 
#        return WindTurbine(position = position, D = D, power = power)
        
    def meanPowerFarm(self):
        return np.mean([turbine.powerMean for turbine in self.turbines])   
        
    def meanPowerRows(self):
        for turbine in self.turbines:
            
        return 
        
    def meanPowerColumns(self,region = 'farm'):
        return np.mean([turbine.powerMean for turbine in self.turbines]) 
        
        
class WindTurbine(object):
    def __init__(self, position = None, row = None, col = None,\
                 D = None, power = None):
        self.position   = position
        self.D          = D
        self.power      = power
        self.row        = row
        self.col        = col
        self.powerMean  = np.mean(power)
                
                
                
datadir = 'C:/Users/u0098627/Documents/Doctoraat/Supercluster/Simulaties/'\
            'BL_sim_finite_M576x256x128_WT14x10startupPowerDataV2/Aligned/'\
            'Windpower1.dat'
Aligned1 = WindFarm(datadir)
print Aligned1.meanPower()

