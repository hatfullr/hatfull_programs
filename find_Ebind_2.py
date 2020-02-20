import glob
import numpy as np
import sys
from scipy.integrate import simps

gravconst = 6.67390e-08
runit = 6.9598e10
munit = 1.9892e33

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
else:
    user_input = raw_input("Enter a file name(s) or pattern(s): ")

files = sorted(glob.glob(user_input))

for i in files:
    if i[:3] != "col":
        print "Files must be of type col*.sph"
        sys.exit()

fmt = " %-5s = %-15.7E"
for i in range(0,len(files)):
    print "Reading",files[i]
    data = np.loadtxt(files[i])

    # Organize particles by radius from the core first
    idx = np.where(data[:,14] == 0)[0]
    
    if len(idx) == 0: # No core particle, organize by radius
        r = data[:,0]
    else: # Organize by distance from the core particle
        x = data[:,10]
        y = data[:,11]
        z = data[:,12]
        r = np.sqrt((x-x[idx])**2. + (y-y[idx])**2. + (z-z[idx])**2.)
        
    data = data[np.argsort(r)]
    mencl = np.cumsum(data[:,5])
    
    # Omit the core
    idxs = np.where(data[:,14] > 0)[0]
    data = data[idxs]
    mencl = mencl[idxs]
    
    r = data[:,0]
    P = data[:,1]
    rho = data[:,2]
    u = data[:,14] # specific internal energy

    idx1 = np.where(mencl > mencl[-1]-0.1)[0]
    idx2 = np.where(mencl > mencl[-1]-1.0)[0]
    mencl1 = mencl[idx1]
    mencl2 = mencl[idx2]
    r1 = r[idx1]
    r2 = r[idx2]
    u1 = u[idx1]
    u2 = u[idx2]
    P1 = P[idx1]
    P2 = P[idx2]
    rho1 = rho[idx1]
    rho2 = rho[idx2]
    
    # Convert to cgs
    r1 = r1*runit
    r2 = r2*runit
    P1 = P1*gravconst/runit**4.*munit**2.
    P2 = P2*gravconst/runit**4.*munit**2.
    rho1 = rho1*munit/runit**3.
    rho2 = rho2*munit/runit**3.
    u1 = u1*gravconst*munit/runit
    u2 = u2*gravconst*munit/runit
    mencl1 = mencl1*munit
    mencl2 = mencl2*munit

    Ebind1 = simps(gravconst*mencl1/r1 - u1 - P1/rho1,x=mencl1)
    Ebind2 = simps(gravconst*mencl2/r2 - u2 - P2/rho2,x=mencl2)
    print(fmt % ("Ebind1",Ebind1))
    print(fmt % ("Ebind2",Ebind2))

