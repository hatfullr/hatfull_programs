"""
Author: Roger Hatfull
Institution: University of Alberta
Date: 01/16/2018
Version 1.0.1


** Description:
   This is a useful file for converting units and using constants in Python scripts.
   Many of the Python postprocessing programs utilize this file. Use the file by
   simply importing it:

   from constants import *


** Changes:

"""

import numpy as np

#Constants
c = np.float64(29979245800) # Speed of light cm/s
a = np.float64(7.5657e-15) #Radiation constant [#erg/cm^3/K^4]
k = np.float64(1.38064852e-16) #Boltzmann constant [erg/K]
m_H = np.float64(1.6737236e-24) #Mass of hydrogen [g]
Na = np.float64(6.0221409e23) #Avagadro's number
sigma_T = np.float64(6.6524587158e-25) #Thomson scattering cross-section in cgs
pi = np.pi
gamma = 5./3. #Adiabatic index for ideal gas

#Units
g = np.float64(1./1000.) #kg
cm = np.float64(1./100.) #m
s = np.float64(1.)
J = np.float64(g * cm**2. / s**2.) #Joules
G = np.float64(1./(6.67408e-11 / cm**3. * g * s**2.)) #Gravitational cosntant in cgs
Ms = np.float64(1./(1.9891e30 / g)) #Mass of the sun in cgs
Rs = np.float64(1./(6.9599e8 / cm)) #Radius of the sun in cgs
Ls = np.float64(1./(3.828e33)) #Ergs/second
Ts = np.float64(1./(5777.)) #Kelvin
codeunits = np.sqrt(Rs**3. / G / Ms) #Code units to seconds
days = np.float64(1./86400.) #Seconds to days
ergs = np.float64(1./1e7) #Joules / erg
eunit = np.float64(G*Ms**2./Rs / 1.e-48) #From the code
years = np.float64(1./31557600) #Years to seconds
