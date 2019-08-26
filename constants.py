"""
Author: Roger Hatfull
Institution: University of Alberta
Date: 04/18/2018
Version 1.0.2


** Description:
   This is a useful file for converting units and using constants in Python scripts.
   Many of the Python postprocessing programs utilize this file. Use the file by
   simply importing it:

   from constants import *


** Changes:
   - Added Stefan-Boltzmann constant
   - Added Planck constant

"""

import numpy as np

#Constants
c = np.float64(29979245800) # Speed of light cm/s
a = np.float64(7.5657e-15) #Radiation constant [erg/cm^3/K^4]
k = np.float64(1.38064852e-16) #Boltzmann constant [erg/K]
h = np.float64(6.62607005e-27) #Planck constant [erg/s]
m_H = np.float64(1.6737236e-24) #Mass of hydrogen [g]
Na = np.float64(6.0221409e23) #Avagadro's number
sigma_T = np.float64(6.6524587158e-25) #Thomson scattering cross-section in cgs
pi = np.pi
gamma = 5./3. #Adiabatic index for ideal gas
sigma_SB = np.float64(c*a/4.) #Stefan-Boltzmann constant [erg/cm^2/s/K^4]

#Units
grams = np.float64(1./1000.) #kg
cm = np.float64(1./100.) #m
s = np.float64(1.)
J = np.float64(grams * cm**2. / s**2.) #Joules
G = np.float64(1./(6.67408e-8)) #Gravitational cosntant in cgs
Ms = np.float64(1./(1.9892e30 / grams)) #Mass of the sun in cgs (MESA)
Rs = np.float64(1./(6.9598e8 / cm)) #Radius of the sun in cgs (MESA)
Ls = np.float64(1./(3.8418e33)) #Ergs/second (MESA)
Ts = np.float64(1./(5777.)) #Kelvin
codeunits = np.float64(1./np.sqrt(G*Ms/Rs**3.)) #Code units to seconds
days = np.float64(1./86400.) #Seconds to days
ergs = np.float64(1./1e7) #Joules / erg
eunit = np.float64(G*Ms**2./Rs) #From the code
years = np.float64(1./31557600.) #Years to seconds
