import numpy as np
from scipy.integrate import simps
import sys
import glob

munit = 1.9891e33
runit = 6.9599e10
gravconst = 6.67408e-8

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")

files = sorted(glob.glob(user_input))
dat = np.ndarray(shape=(len(files),2))
fmt = " %-13s = %-15.7E Rsun"

for i in range(0,len(files)):
    print "Reading",files[i]
    data = np.loadtxt(files[i],skiprows=6)[::-1]
    headerdata = np.loadtxt(files[i],skiprows=2,max_rows=1)
    # all in cgs
    m = data[:,2] * munit
    r = 10.**data[:,3] * runit
    rho = 10.**data[:,5]
    P = 10.**data[:,6]
    energy = data[:,14]
    
    
    # Maximum radius
    print(fmt % ("R",r[-1]/runit))
    
    # "Volume-equivalent radius"
    RV = (3./(4.*np.pi) * simps(1./rho,x=m))**(1./3.) / runit
    print(fmt % ("R_V",RV))

    # Core quantities
    coremass = np.sum(headerdata[26:31]*munit)
    print(fmt % ("M_c", coremass/munit))
    coreidx = find_nearest(m,coremass)
    print(fmt % ("R_c",r[coreidx]/runit))
    print(fmt % ("rho_c", np.mean(rho[:coreidx])))

    # Envelope quantities
    U = simps(energy[coreidx:],x=m[coreidx:]) 
    print(fmt % ("U", U))

    W = -gravconst * simps(m[coreidx:]/(r[coreidx:]),x=m[coreidx:])
    print(fmt % ("W", W))

    enthalpy = energy + P/rho
    Ebind = simps((gravconst * m[coreidx:]/r[coreidx:]) - enthalpy[coreidx:],x=m[coreidx:])
    print(fmt % ("Ebind", Ebind))

    print(fmt % ("Teff", headerdata[6]))
    
