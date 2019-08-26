import read_sph_data as rsd
import glob
import numpy as np
import sys
from scipy.integrate import simps

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")

munit = 1.9891e33
runit = 6.9599e10
    
files = sorted(glob.glob(user_input))
dat = np.ndarray(shape=(len(files),2))
fmt = " %-13s = %-15.7E Rsun"

for i in range(0,len(files)):
    print "Reading",files[i]
    data = rsd.read(files[i])

    # Radii quantities come from arxiv.org/pdf/1311.6522.pdf

    # Furthest particle
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]
    r = np.sqrt(x**2. + y**2. + z**2.)
    print(fmt % ("R_RG",np.max(r)))

    # "Effective radius"
    h = data[:,4]
    print(fmt % ("R_RG + h_out",np.max(r+h)))
    
    # Furthest smoothing length
    print(fmt % ("R_RG + 2h_out",np.max(r+2.*h)))

    # "Volume-equivalent radius"
    m = data[:,3]
    rho = data[:,5]
    #RV = (3. * np.sum(m/rho) / (4*np.pi))**(1./3.)
    idx = np.argsort(r)
    m = m[idx]
    rho = rho[idx]
    mencl = np.cumsum(m)
    RV = (3./(4.*np.pi) * simps(1./(rho),x=mencl))**(1./3.)
    print(fmt % ("R_V",RV))

    # Average outer particle smoothing length
    # Average over the outer 10% of envelope by radius
    # Sort the data
    data = data[np.argsort(r)]
    mencl = np.cumsum(data[:,3])
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]
    r = np.sqrt(x**2. + y**2. + z**2.)
    h = data[:,4]
    #idx = np.where(r > 0.9*np.max(r+2.*h))[0]
    idx = np.where(mencl >= 1.42)[0]
    print(fmt % ("<2h_s>",np.mean(2.*h[idx])))
