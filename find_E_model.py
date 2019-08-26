import numpy as np
import glob
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

fmt = " %-1s = %-15.7E ergs"
for i in range(0,len(files)):
    data = np.loadtxt(files[i],skiprows=6)
    coremass = np.sum(np.loadtxt(files[i],skiprows=2,max_rows=1)[-19:-14])
    data = data[np.where(data[:,2] > coremass)[0]]
    mass = data[:,2]*munit
    r = 10.**data[:,3]*runit
    energy = data[:,14]

    U = simps(energy[::-1],x=mass[::-1])
    W = -gravconst*simps(mass[::-1]/r[::-1],x=mass[::-1])
    
    print(fmt % ("E",W+U))
