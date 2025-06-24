# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 12:43:43 2025

@author: Philip_comet_lab

This uses the simplified Penman-Monteith Equation to calculate evapotranspiration.
"""

import numpy as np
import xarray as xr
import os
from wrf_precip_plotting_functions import plotting #My general plotting function that can be found "https://github.com/cjoh513/LSU-COMET-Lab/blob/main/Python/wrfout_plotting_functions.py"


# Constants
lambda_v = 2.45        # MJ/kg, latent heat of vaporization
cp       = 1.013e-3    # MJ/kg°C, specific heat of air
epsilon  = 0.622       # Ratio of molecular weights
P_std    = 101.3       # kPa, standard pressure at sea level
contour_range = [0,10.5,0.5] #For the Plotting function


for year in range(1995,1996):
    ET_list = []
    outer_path = r"H:/MSD_"+str(year)
    file_list = [item for item in os.listdir(outer_path)]
    for item in file_list:
        ds = xr.open_dataset(os.path.join(outer_path,item))
        
        
        
        
        # Extract variables
        T2     = ds['T2'] - 273.15                # Convert to °C
        Q2     = ds['Q2']                         # kg/kg
        PSFC   = ds['PSFC'] / 1000                # Convert Pa to kPa
        U10    = ds['U10']
        V10    = ds['V10']
        SWDOWN = ds['SWDOWN']
        SWUP   = ds['SWUPB']
        LWDOWN = ds['GLW'] if 'GLW' in ds else ds['LWDOWN']
        LWUP   = ds['LWUPB']
        GRDFLX = ds['GRDFLX']
        lats   = ds['XLAT'][0,:,:]
        lons   = ds['XLONG'][0,:,:]
    



        # Time-averaging for daily values (axis=0 is usually time)
        T = T2.mean(dim='Time')
        Q = Q2.mean(dim='Time')
        P = PSFC.mean(dim='Time')
        U = np.sqrt(U10**2 + V10**2).mean(dim='Time')
        Rn = ((SWDOWN - SWUP) + (LWDOWN - LWUP)).mean(dim='Time') * 86400 / 1e6  # W/m2 to MJ/m2/day
        G = GRDFLX.mean(dim='Time') * 86400 / 1e6  # W/m2 to MJ/m2/day
        
        
        # Saturation vapor pressure (es) and slope (Delta)
        es = 0.6108 * np.exp((17.27 * T) / (T + 237.3))
        Delta = (4098 * es) / ((T + 237.3)**2)
        # Actual vapor pressure (ea)
        ea = (Q * P) / (epsilon + (1 - epsilon) * Q)
        # Vapor pressure deficit
        VPD = es - ea
        
        
        # Psychrometric constant (gamma)
        gamma = (cp * P) / (epsilon * lambda_v)
        
        # Wind speed at 2 m (u2)
        #u2 = U * 0.748  # Approximate adjustment from 10 m to 2 m
        u2 = U * (4.87/np.log(67.8*10-5.42))
        
        
        # Penman-Monteith Equation
        numerator = 0.408 * Delta * (Rn - G) + gamma * (900 / (T + 273)) * u2 * VPD
        denominator = Delta + gamma * (1 + 0.34 * u2)
        ET0 = numerator / denominator  # mm/day
        
        ET_list.append(ET0)
    
    ET_avg = np.mean(np.asarray(ET_list),axis=0)
    
    print(np.max(ET_avg),np.min(ET_avg))
    
    
    plotting(lons=lons,
             lats=lats,
             plotted=ET_avg,
             contour_range=contour_range,
             tick_range=contour_range,
             title=str(year)+" Average Daily Evapotranspiration (mm/day)"
             )
        
        
        
        
        
        