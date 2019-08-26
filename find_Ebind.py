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

    # Organize particles by radii first
    r = data[:,0]
    data = data[np.argsort(r)]

    mencl = np.cumsum(data[:,5])
    
    # Omit the core
    data = data[1:]
    mencl = mencl[1:]
    
    r = data[:,0]
    P = data[:,1]
    rho = data[:,2]
    u = data[:,14] # specific internal energy

    # Convert to cgs
    r = r*runit
    P = P*gravconst/runit**4.*munit**2.
    rho = rho*munit/runit**3.
    u = u*gravconst*munit/runit
    mencl = mencl*munit
    
    Ebind = simps(gravconst*mencl/r - u - P/rho,x=mencl)

    print(fmt % ("Ebind",Ebind))
    

